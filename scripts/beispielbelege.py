#!/usr/bin/env python3
"""Erzeugt die Beispielbelege der Vorlage als kleine PDFs.

Die Vorlage enthält keine Binärdateien. Dieses Skript schreibt die Belege, auf
die der Beispiel-Ledger verweist, damit `check_belege.py` durchläuft und die
Website etwas zum Verlinken hat. Ohne Abhängigkeiten — ein PDF ist Text.

    python3 scripts/beispielbelege.py
"""
from __future__ import annotations

from pathlib import Path

WURZEL = Path(__file__).resolve().parents[1]

BELEGE: dict[str, list[str]] = {
    "belege/ausgangsrechnungen/2025/2025-02-01.RE2025020001.nordlicht-labs.pdf": [
        "Rechnung RE2025020001",
        "Nordlicht Labs Pte. Ltd., Singapur",
        "Leistung: Softwareentwicklung Januar 2025",
        "40,0 h x 120,00 EUR = 4.800,00 EUR",
        "Keine deutsche Umsatzsteuer, Leistungsort Singapur (Par. 3a Abs. 2 UStG)",
    ],
    "belege/2025/2025-01-15.bueromoebel-muster-schreibtisch.pdf": [
        "Bueromoebel Muster - Rechnung",
        "Schreibtisch und Buerostuhl",
        "Netto 1.560,00 EUR + 19 % USt 296,40 EUR = 1.856,40 EUR",
        "Nutzungsdauer 13 Jahre laut AfA-Tabelle",
    ],
    "belege/2025/2025-03-01.musterhoster-server-februar.pdf": [
        "Musterhoster GmbH - Rechnung",
        "Serverkosten Februar 2025",
        "Netto 21,00 EUR + 19 % USt 3,99 EUR = 24,99 EUR",
    ],
    "belege/2025/2025-07-15.musterversicherung-haftpflicht-2025.pdf": [
        "Musterversicherung - Beitragsrechnung",
        "Privathaftpflicht 2025: 94,00 EUR",
    ],
    "belege/2025/2025-09-01.dachdeckerei-muster-dachreparatur.pdf": [
        "Dachdeckerei Muster - Rechnung",
        "Dachreparatur, Beispielweg 1",
        "Arbeitszeit 252,00 EUR",
        "Fahrtkosten 35,00 EUR",
        "Material 76,68 EUR",
        "Zusammen 433,68 EUR, davon Lohnanteil 287,00 EUR",
        "Zahlung bitte per Ueberweisung",
    ],
    "belege/2025/2026-01-20.zuwendungsbestaetigung-musterhilfe-2025.pdf": [
        "Musterhilfe e.V. - Zuwendungsbestaetigung",
        "nach amtlichem Muster",
        "Zuwendung am 06.05.2025: 250,00 EUR",
        "Freistellungsbescheid des Finanzamts Musterstadt vom 01.02.2024",
    ],
    "belege/2025/2026-02-10.schulgeldbestaetigung-2025.pdf": [
        "Freie Schule Musterstadt - Schulgeldbestaetigung 2025",
        "Kind: Nala Beispiel",
        "August bis Dezember 2025: 1.500,00 EUR",
        "Entgelte fuer Beherbergung, Betreuung und Verpflegung nicht enthalten",
    ],
    "belege/2025/2026-03-05.steuerbescheinigung-musterbroker-2025.pdf": [
        "Musterbroker - Steuerbescheinigung 2025",
        "Kapitalertraege (brutto): 100,00 EUR",
        "Kapitalertragsteuer: 25,00 EUR",
        "Solidaritaetszuschlag: 1,37 EUR",
    ],
    "data/raw/beispielbank/2025-03-31.kontoauszug.pdf": [
        "Beispielbank - Kontoauszug 1/2025, Geschaeftskonto",
        "31.03. Kontofuehrung 1. Quartal: 15,00 EUR netto, 2,85 EUR USt",
    ],
    "data/raw/beispielbank/2025-04-30.kontoauszug.pdf": [
        "Beispielbank - Kontoauszug 2/2025, Geschaeftskonto",
        "15.04. Finanzamt Musterstadt, Erstattung Umsatzsteuer 2024: 143,40 EUR",
    ],
    "data/raw/beispielbank/2025-06-30.kontoauszug.pdf": [
        "Beispielbank - Kontoauszug 3/2025, Privatkonto",
        "14.06. Dorfverein Musterstadt, Spende: 120,00 EUR",
    ],
}

FUSS = "Beispielbeleg der Vorlage german-finances-template. Erfundene Daten."


def pdf(zeilen: list[str]) -> bytes:
    """Minimales einseitiges PDF, nur mit der Standardschrift Helvetica."""
    def escape(text: str) -> str:
        return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

    inhalt = ["BT /F1 15 Tf 60 752 Td (" + escape(zeilen[0]) + ") Tj ET"]
    y = 752
    for zeile in zeilen[1:]:
        y -= 26
        inhalt.append(f"BT /F1 11 Tf 60 {y} Td (" + escape(zeile) + ") Tj ET")
    inhalt.append("BT /F1 8 Tf 60 42 Td (" + escape(FUSS) + ") Tj ET")
    strom = "\n".join(inhalt).encode("latin-1", "replace")

    objekte = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(strom)).encode() + b" >>\nstream\n" + strom + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]

    raus = bytearray(b"%PDF-1.4\n")
    positionen = []
    for i, objekt in enumerate(objekte, start=1):
        positionen.append(len(raus))
        raus += f"{i} 0 obj\n".encode() + objekt + b"\nendobj\n"
    start_xref = len(raus)
    raus += f"xref\n0 {len(objekte) + 1}\n".encode()
    raus += b"0000000000 65535 f \n"
    for pos in positionen:
        raus += f"{pos:010d} 00000 n \n".encode()
    raus += (f"trailer\n<< /Size {len(objekte) + 1} /Root 1 0 R >>\n"
             f"startxref\n{start_xref}\n%%EOF\n").encode()
    return bytes(raus)


def main() -> None:
    for pfad, zeilen in BELEGE.items():
        ziel = WURZEL / pfad
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_bytes(pdf(zeilen))
    print(f"{len(BELEGE)} Beispielbelege geschrieben.")


if __name__ == "__main__":
    main()
