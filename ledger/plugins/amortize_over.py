"""Lineare Abschreibung: eine Buchung, monatliche Teilbeträge.

Eine Transaktion mit der Metadata `amortize_months` wird durch monatliche
Buchungen ersetzt, vom Buchungsdatum bis heute. Zukünftige Monate entstehen
erst, wenn sie erreicht sind — so bleibt jeder Zwischenstand prüfbar.

    2025-01-15 * "Bürostuhl" "Abschreibungsplan"
      amortize_months: 60
      Expenses:Betrieb:Abschreibung        600.00 EUR
      Assets:Anlagen:Bueroeinrichtung:AfA -600.00 EUR
"""
from __future__ import annotations

import datetime
from decimal import Decimal

from beancount.core import data

__plugins__ = ("amortize_over",)


def _monate_spaeter(tag: datetime.date, n: int) -> datetime.date:
    monat = tag.month - 1 + n
    jahr = tag.year + monat // 12
    monat = monat % 12 + 1
    # Auf den letzten Tag des Zielmonats begrenzen (31.01. + 1 Monat).
    letzter = [31, 29 if jahr % 4 == 0 and (jahr % 100 or jahr % 400 == 0) else 28,
               31, 30, 31, 30, 31, 31, 30, 31, 30, 31][monat - 1]
    return datetime.date(jahr, monat, min(tag.day, letzter))


def amortize_over(entries, options_map):
    heute = datetime.date.today()
    neu, fehler = [], []

    for eintrag in entries:
        monate = (eintrag.meta or {}).get("amortize_months") if isinstance(
            eintrag, data.Transaction) else None
        if not monate:
            neu.append(eintrag)
            continue

        monate = int(monate)
        for i in range(monate):
            tag = _monate_spaeter(eintrag.date, i)
            if tag > heute:
                break
            postings = [
                p._replace(units=p.units._replace(
                    number=(p.units.number / Decimal(monate)).quantize(Decimal("0.01"))))
                for p in eintrag.postings
            ]
            neu.append(eintrag._replace(
                date=tag,
                narration=f"{eintrag.narration} ({i + 1}/{monate})",
                postings=postings,
                meta={**eintrag.meta, "amortize_months": None},
            ))

    return neu, fehler
