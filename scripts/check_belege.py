#!/usr/bin/env python3
"""Belegpflicht prüfen: hat jede Buchung einen Beleg, existiert jede Datei?

Exit 0 = alles belegt. Sonst 1, mit Liste. Welche Konten belegpflichtig sind,
steht in `scripts/check_belege.json` — dieselbe Datei benutzt der Generator der
Website, damit beide Zahlen übereinstimmen.

    python3 scripts/check_belege.py [--year 2025]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from beancount import loader
from beancount.core import data

WURZEL = Path(__file__).resolve().parents[1]


def verweise(tx) -> tuple[list[str], list[str]]:
    quellen = [tx.meta or {}] + [(p.meta or {}) for p in tx.postings]
    dokumente = [q["document"] for q in quellen if q.get("document")]
    auszuege = [q["statement"] for q in quellen if q.get("statement")]
    return dokumente, auszuege


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--year")
    args = p.parse_args()

    konfig = json.loads((WURZEL / "scripts" / "check_belege.json").read_text())
    pflicht = tuple(konfig["belegpflichtig"])
    auszug_genuegt = tuple(konfig["statement_genuegt"])
    ausnahmen = {(a["datum"], a["konto"]) for a in konfig.get("ausnahmen", [])}

    eintraege, fehler, _ = loader.load_file(str(WURZEL / "ledger" / "main.beancount"))
    if fehler:
        print(f"Ledger hat {len(fehler)} Fehler — erst die beheben.")
        return 1

    ohne_beleg, tote = [], []
    for tx in eintraege:
        if not isinstance(tx, data.Transaction):
            continue
        if args.year and str(tx.date.year) != args.year:
            continue

        dokumente, auszuege = verweise(tx)
        for pfad in dokumente + auszuege:
            if not (WURZEL / pfad).exists():
                tote.append(f"{tx.date} {tx.payee or tx.narration}: {pfad}")

        betroffen = [x.account for x in tx.postings if x.account.startswith(pflicht)]
        if not betroffen:
            continue
        if dokumente:
            continue
        # Nur ein Kontoauszug: reicht, wenn alle betroffenen Konten es erlauben.
        if auszuege and all(k.startswith(auszug_genuegt) for k in betroffen):
            continue
        offen = [k for k in betroffen
                 if (tx.date.isoformat(), k) not in ausnahmen]
        if not offen:
            continue
        betroffen = offen
        ohne_beleg.append(f"{tx.date} {(tx.payee or tx.narration)[:40]:40} "
                          f"{', '.join(sorted(set(betroffen)))}")

    for titel, liste in (("Buchungen ohne Beleg", ohne_beleg),
                         ("Verweise auf fehlende Dateien", tote)):
        if liste:
            print(f"\n{titel} ({len(liste)}):")
            for zeile in liste:
                print(f"  {zeile}")

    if ohne_beleg or tote:
        return 1
    print("Alles belegt." + (f" (Jahr {args.year})" if args.year else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
