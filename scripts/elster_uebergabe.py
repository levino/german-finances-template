#!/usr/bin/env python3
"""Erzeugt die ELSTER-Übergabe eines Jahres als Markdown und als XML.

Quelle ist `site/src/data/erklaerung.json` — also dieselbe Auswertung, die auch
die Website zeigt. Übertragen werden nur Felder mit Status belegt (🟢) und
Kandidat (🟡, als vorläufig markiert). Alles andere bleibt bewusst draußen.

    python3 site/scripts/generate-data.py && python3 scripts/elster_uebergabe.py 2025
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

WURZEL = Path(__file__).resolve().parents[1]
UEBERTRAGEN = {"belegt", "kandidat"}


def felder(block: dict):
    for gruppe in block["gruppen"]:
        for feld in gruppe["felder"]:
            if feld["status"] in UEBERTRAGEN and (feld.get("wert") or "").strip():
                yield gruppe["titel"], feld


def markdown(jahr: str, daten: dict, kopf: str, fuss: str) -> str:
    teile = [kopf.rstrip(), ""]
    for form in daten["dokumente"]:
        teile.append(f"\n## {form['titel']}\n")
        for block in form["bloecke"]:
            zeilen = list(felder(block))
            if not zeilen:
                continue
            teile.append(f"### {block['titel']}\n")
            teile.append("| Zeile | Feld | Wert |")
            teile.append("|---|---|---|")
            for _gruppe, feld in zeilen:
                summe = feld.get("summe")
                stern = "**" if summe else ""
                teile.append(f"| {stern}{feld['zeile'] or '—'}{stern} | "
                             f"{stern}{feld['feld']}{stern} | {stern}{feld['wert']}{stern} |")
            teile.append("")
    teile.append(fuss.rstrip())
    return "\n".join(teile) + "\n"


def xml(jahr: str, daten: dict) -> str:
    zeilen = [f'<?xml version="1.0" encoding="utf-8"?>',
              f'<elster-uebergabe jahr="{jahr}">']
    for form in daten["dokumente"]:
        zeilen.append(f'  <formular name={quoteattr(form["titel"])}>')
        for block in form["bloecke"]:
            eintraege = list(felder(block))
            if not eintraege:
                continue
            zeilen.append(f'    <block name={quoteattr(block["titel"])}>')
            for gruppe, feld in eintraege:
                attribute = [f'zeile={quoteattr(feld["zeile"])}',
                             f'feld={quoteattr(feld["feld"])}',
                             f'wert={quoteattr(feld["wert"])}',
                             'eintragen="ja"']
                if feld["status"] == "kandidat":
                    attribute.append('vorlaeufig="ja"')
                if gruppe:
                    attribute.append(f'gruppe={quoteattr(gruppe)}')
                zeilen.append("      <posten " + " ".join(attribute) + "/>")
            zeilen.append("    </block>")
        zeilen.append("  </formular>")
    zeilen.append("</elster-uebergabe>")
    return "\n".join(zeilen) + "\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    jahr = sys.argv[1]
    quelle = WURZEL / "site" / "src" / "data" / "erklaerung.json"
    if not quelle.exists():
        print("site/src/data/erklaerung.json fehlt — erst den Generator laufen lassen.")
        return 1
    daten = json.loads(quelle.read_text(encoding="utf-8")).get(jahr)
    if not daten:
        print(f"Kein Jahr {jahr} in der Auswertung.")
        return 1

    ordner = WURZEL / "steuer" / jahr
    kopf = (ordner / "elster-kopf.md").read_text(encoding="utf-8") if (ordner / "elster-kopf.md").exists() else f"# ELSTER-Übergabe {jahr}"
    fuss = (ordner / "elster-fuss.md").read_text(encoding="utf-8") if (ordner / "elster-fuss.md").exists() else ""

    (ordner / "elster-uebergabe.md").write_text(markdown(jahr, daten, kopf, fuss), encoding="utf-8")
    (ordner / "elster-uebergabe.xml").write_text(xml(jahr, daten), encoding="utf-8")
    print(f"geschrieben: steuer/{jahr}/elster-uebergabe.md und .xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
