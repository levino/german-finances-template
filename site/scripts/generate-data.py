#!/usr/bin/env python3
"""Erzeugt die JSON-Datenbasis für das Cockpit aus Ledger und Arbeitsmappe.

Liest `ledger/main.beancount`, `belege/**` und `steuer/<jahr>/*.md` und schreibt
nach `site/src/data/`. Kein zweiter Datenbestand: die Website rechnet nichts
selbst, sie zeigt nur, was hier entsteht.

Aufruf:  python3 site/scripts/generate-data.py [--repo <pfad>] [--out <pfad>]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from beancount import loader
from beancount.core import data

WURZEL = Path(__file__).resolve().parents[2]

# Nur diese Endungen gelten als Beleg.
BELEG_ENDUNGEN = {"pdf", "xml", "jpg", "jpeg", "png"}

# Status aus der Ampel. Reihenfolge = Dringlichkeit: steht mehr als eine Ampel
# in einer Zeile, gewinnt die erste dieser Liste.
AMPELN = [("🔴", "offen"), ("❓", "zu-klaeren"), ("🟡", "kandidat"),
          ("⛔", "nicht-erklaeren"), ("🟢", "belegt")]

# [=](konto:A+B~Filter) · [=gewinn](konto:…) · [=](beleg:belege/…pdf)
KONTO_RE = re.compile(r"\[=(?P<art>\w*)\]\(konto:(?P<konten>[^)~]+)(?:~(?P<filter>[^)]+))?\)")
BELEG_RE = re.compile(r"\[=\]\(beleg:(?P<pfad>[^)]+)\)")
DATEINAME_RE = re.compile(r"^(?P<datum>\d{4}-\d{2}-\d{2})\.(?P<rest>.+)\.(?P<ext>[a-z0-9]+)$")


def betrag(zahl: Decimal) -> str:
    """Deutsche Schreibweise, Minus als Gedankenstrich-Minus."""
    s = f"{abs(zahl):,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return ("−" if zahl < 0 else "") + s


def status_von(text: str) -> str:
    for zeichen, name in AMPELN:
        if zeichen in text:
            return name
    return "ohne"


def slug(text: str) -> str:
    text = (text.lower().replace("ä", "ae").replace("ö", "oe")
            .replace("ü", "ue").replace("ß", "ss"))
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", text)).strip("-")


# --------------------------------------------------------------- Ledger lesen

def buchungen_laden(repo: Path):
    eintraege, fehler, _ = loader.load_file(str(repo / "ledger" / "main.beancount"))
    if fehler:
        for f in fehler:
            print(f"  Ledger-Fehler: {f}")
    return [e for e in eintraege if isinstance(e, data.Transaction)]


def referenzen(tx) -> list[str]:
    """Belegverweise einer Buchung, am Transaktions- und am Posting-Level."""
    quellen = [tx.meta or {}] + [(p.meta or {}) for p in tx.postings]
    return [q[k] for q in quellen for k in ("document", "statement") if q.get(k)]


def posten(buchungen, jahr: str, praefixe: list[str], payee_filter: str | None,
           nur_belegte: bool = False):
    """Alle Postings des Jahres auf den genannten Konten.

    Ein Präfix mit "!" davor schließt aus — so bleibt die Vorsteuer aus dem
    Gewinn, obwohl sie unter Expenses:Betrieb liegt.
    """
    nehmen = [x for x in praefixe if not x.startswith("!")]
    lassen = [x[1:] for x in praefixe if x.startswith("!")]
    raus = []
    for tx in buchungen:
        if str(tx.date.year) != jahr:
            continue
        if payee_filter and payee_filter.lower() not in f"{tx.payee} {tx.narration}".lower():
            continue
        belege = referenzen(tx)
        if nur_belegte and not belege:
            continue
        for p in tx.postings:
            if not any(p.account.startswith(x) for x in nehmen):
                continue
            if any(p.account.startswith(x) for x in lassen):
                continue
            if p.units is None or p.units.number is None:
                continue
            raus.append({
                "datum": tx.date.isoformat(),
                "konto": p.account,
                "payee": (tx.payee or "").strip(),
                "narration": (tx.narration or "").strip(),
                "zahl": p.units.number,
                "betrag": betrag(p.units.number),
                "belege": belege,
            })
    return raus


def summe(liste) -> Decimal:
    return sum((p["zahl"] for p in liste), Decimal(0))


# ---------------------------------------------------- Arbeitsmappe auswerten

def arbeitsmappe_lesen(pfad: Path) -> list[dict]:
    """Formulare, Blöcke, Gruppen und ihre Feldtabellen."""
    formulare: list[dict] = []
    for zeile in pfad.read_text(encoding="utf-8").split("\n"):
        if zeile.startswith("## "):
            formulare.append({"titel": zeile[3:].strip(), "id": slug(zeile[3:]),
                              "bloecke": []})
        elif zeile.startswith("### ") and formulare:
            formulare[-1]["bloecke"].append(
                {"titel": zeile[4:].strip(), "id": slug(zeile[4:]), "gruppen": []})
        elif zeile.startswith("#### ") and formulare and formulare[-1]["bloecke"]:
            formulare[-1]["bloecke"][-1]["gruppen"].append(
                {"titel": zeile[5:].strip(), "zeilen": []})
        elif zeile.startswith("|") and formulare and formulare[-1]["bloecke"]:
            bloecke = formulare[-1]["bloecke"]
            if not bloecke[-1]["gruppen"]:
                bloecke[-1]["gruppen"].append({"titel": "", "zeilen": []})
            bloecke[-1]["gruppen"][-1]["zeilen"].append(zeile)
    return formulare


def felder_von(zeilen: list[str]) -> list[dict]:
    felder = []
    for zeile in zeilen:
        spalten = [s.strip() for s in zeile.strip().strip("|").split("|")]
        if len(spalten) < 4 or set(spalten[0]) <= set("-: ") or spalten[0] == "Zeile / Feld":
            continue
        bezeichnung = spalten[0]
        nummer = re.match(r"^\**\s*(\d+(?:[–-]\d+)?)", bezeichnung.lstrip("⛔🔴🟡🟢❓ *"))
        # Die Zeilennummer steht vorne in der Bezeichnung; im Feldnamen wäre
        # sie doppelt.
        name = re.sub(r"[⛔🔴🟡🟢❓*]", "", bezeichnung).strip()
        if nummer:
            name = name[len(nummer.group(1)):].strip()
        felder.append({
            "zeile": nummer.group(1) if nummer else "",
            "feld": name,
            "roh": spalten[1],
            "quelle": re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1", spalten[2]),
            "quelle_belege": [m.group(2) for m in
                              re.finditer(r"\[([^\]]*)\]\((belege/[^)]*)\)", spalten[2])],
            "status": status_von(spalten[3] or bezeichnung),
        })
    return felder


def werte_setzen(felder: list[dict], buchungen, jahr: str, repo: Path) -> None:
    """Rechnet die Herleitungen aus und hängt sie an die Felder."""
    for f in felder:
        roh = f["roh"]
        f["herleitung"] = []

        treffer = KONTO_RE.search(roh)
        if treffer:
            konten = [k.strip() for k in treffer.group("konten").split("+")]
            liste = posten(buchungen, jahr, konten, treffer.group("filter"))
            wert = summe(liste)
            # Einnahmen stehen im Ledger negativ. Im Formular gehören sie
            # positiv hin, deshalb das Vorzeichen drehen — bei "gewinn" für
            # die gemischte Summe aus Einnahmen und Ausgaben ebenso.
            if treffer.group("art") == "gewinn" or all(
                    k.startswith("Income") for k in konten if not k.startswith("!")):
                wert = -wert
            f["wert"] = betrag(wert)
            f["zahl"] = float(wert)
            f["herleitung"] = liste
            continue

        treffer = BELEG_RE.search(roh)
        if treffer:
            pfad = treffer.group("pfad")
            liste = [p for p in posten(buchungen, jahr, ["Expenses", "Income", "Assets"], None)
                     if pfad in p["belege"]]
            # Nur die Aufwands- und Ertragsseite, sonst zählt die Bank doppelt.
            liste = [p for p in liste if p["konto"].startswith(("Expenses", "Income"))]
            f["wert"] = betrag(summe(liste))
            f["zahl"] = float(summe(liste))
            f["herleitung"] = liste
            continue

        if roh.strip() == "=":
            f["wert"] = ""      # wird in summen_setzen gefüllt
            f["zahl"] = 0.0
            f["summe"] = True
            continue

        f["wert"] = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", roh)
        f["zahl"] = None


def summen_setzen(gruppe: dict) -> None:
    """Eine Summenzeile summiert die Zeilen derselben Nummer in ihrer Gruppe."""
    for f in gruppe["felder"]:
        if not f.get("summe"):
            continue
        gleiche = [g for g in gruppe["felder"]
                   if g is not f and g.get("zahl") is not None
                   and (g["zeile"] == f["zeile"] or not f["zeile"])
                   and g["status"] != "nicht-erklaeren"]
        wert = Decimal(str(sum(g["zahl"] for g in gleiche)))
        f["wert"] = betrag(wert)
        f["zahl"] = float(wert)


def erklaerung_bauen(repo: Path, buchungen) -> dict:
    jahre = {}
    for mappe in sorted((repo / "steuer").glob("*/arbeitsmappe.md")):
        jahr = mappe.parent.name
        formulare = arbeitsmappe_lesen(mappe)
        for form in formulare:
            for block in form["bloecke"]:
                for gruppe in block["gruppen"]:
                    gruppe["felder"] = felder_von(gruppe["zeilen"])
                    gruppe.pop("zeilen")
                    werte_setzen(gruppe["felder"], buchungen, jahr, repo)
                    summen_setzen(gruppe)
                block["felder_gesamt"] = sum(len(g["felder"]) for g in block["gruppen"])
                block["offen"] = sum(1 for g in block["gruppen"] for f in g["felder"]
                                     if f["status"] in ("offen", "zu-klaeren"))
            form["felder_gesamt"] = sum(b["felder_gesamt"] for b in form["bloecke"])
            form["offen"] = sum(b["offen"] for b in form["bloecke"])
        alle = [f for form in formulare for b in form["bloecke"]
                for g in b["gruppen"] for f in g["felder"]]
        jahre[jahr] = {
            "jahr": jahr,
            "dokumente": formulare,
            "felder_gesamt": len(alle),
            "belegt": sum(1 for f in alle if f["status"] == "belegt"),
            "vorlaeufig": sum(1 for f in alle if f["status"] == "kandidat"),
            "offen": sum(1 for f in alle if f["status"] in ("offen", "zu-klaeren")),
        }
    return jahre


# ------------------------------------------------------------------- Belege

def belege_bauen(repo: Path, buchungen) -> dict:
    dateien = {}
    for pfad in sorted((repo / "belege").rglob("*")):
        if not pfad.is_file() or pfad.suffix.lstrip(".").lower() not in BELEG_ENDUNGEN:
            continue
        rel = str(pfad.relative_to(repo))
        treffer = DATEINAME_RE.match(pfad.name)
        teile = rel.split("/")
        dateien[rel] = {
            "pfad": rel,
            "jahr": teile[2] if teile[1] == "ausgangsrechnungen" else teile[1],
            "datum": treffer.group("datum") if treffer else None,
            "bezeichnung": (treffer.group("rest").replace("-", " ").replace(".", " · ")
                            if treffer else pfad.stem),
            "ausgangsrechnung": teile[1] == "ausgangsrechnungen",
            "buchungen": [],
        }

    tote, ohne_beleg = [], []
    for tx in buchungen:
        verweise = referenzen(tx)
        for ref in verweise:
            if ref in dateien:
                dateien[ref]["buchungen"].append({
                    "datum": tx.date.isoformat(),
                    "payee": (tx.payee or "").strip(),
                    "narration": (tx.narration or "").strip(),
                })
            elif not (repo / ref).exists():
                tote.append({"datum": tx.date.isoformat(), "verweis": ref})

    return {
        "belege": list(dateien.values()),
        "tote_verweise": tote,
        "kennzahlen": {
            "dateien": len(dateien),
            "mit_buchung": sum(1 for b in dateien.values() if b["buchungen"]),
            "verwaist": sum(1 for b in dateien.values() if not b["buchungen"]),
            "tote_verweise": len(tote),
        },
    }


def aufgaben_bauen(repo: Path) -> dict:
    """Die Aufgabenliste aus STAND.md: Checkboxen, Gruppen nach Zwischentitel."""
    jahre = {}
    for stand in sorted((repo / "steuer").glob("*/STAND.md")):
        offen, erledigt = [], []
        for zeile in stand.read_text(encoding="utf-8").split("\n"):
            treffer = re.match(r"^- \[( |x)\] (.+)$", zeile)
            if not treffer:
                continue
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", treffer.group(2))
            (erledigt if treffer.group(1) == "x" else offen).append(text)
        jahre[stand.parent.name] = {"offen": offen, "erledigt": erledigt}
    return jahre


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=str(WURZEL))
    p.add_argument("--out", default=None)
    p.add_argument("--keine-pdfs", action="store_true",
                   help="Belegdateien nicht nach site/public/ kopieren")
    args = p.parse_args()
    repo = Path(args.repo).resolve()
    out = Path(args.out) if args.out else repo / "site" / "src" / "data"
    out.mkdir(parents=True, exist_ok=True)

    buchungen = buchungen_laden(repo)
    print(f"Ledger: {len(buchungen)} Buchungen")

    erklaerung = erklaerung_bauen(repo, buchungen)
    for jahr, inhalt in erklaerung.items():
        print(f"  {jahr}: {inhalt['felder_gesamt']} Felder, {inhalt['belegt']} belegt, "
              f"{inhalt['offen']} offen")
    belege = belege_bauen(repo, buchungen)
    print(f"  Belege: {belege['kennzahlen']['dateien']} Dateien, "
          f"{belege['kennzahlen']['verwaist']} ohne Buchung")

    meta = {
        "erzeugt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "jahre": sorted(erklaerung, reverse=True),
    }
    if not args.keine_pdfs:
        ziel = repo / "site" / "public" / "belege"
        if ziel.exists():
            shutil.rmtree(ziel)
        shutil.copytree(repo / "belege", ziel,
                        ignore=shutil.ignore_patterns("README.md"))
        print(f"  Belege nach site/public/belege/ kopiert")

    for name, inhalt in (("erklaerung", erklaerung), ("belege", belege),
                         ("aufgaben", aufgaben_bauen(repo)), ("meta", meta)):
        ziel = out / f"{name}.json"
        ziel.write_text(json.dumps(inhalt, ensure_ascii=False, indent=1, default=str),
                        encoding="utf-8")
        print(f"  geschrieben: {ziel.relative_to(repo)}")


if __name__ == "__main__":
    main()
