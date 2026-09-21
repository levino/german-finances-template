# Belegablage

```
belege/<JAHR>/<JJJJ-MM-TT>.<kurzbeschreibung>.<ext>
belege/ausgangsrechnungen/<JAHR>/<JJJJ-MM-TT>.<renr>.<kunde>.<ext>
```

Das Datum ist das **Belegdatum** (Rechnungs- oder Ausstellungsdatum), nicht das
Zahlungsdatum. ISO, Trennung mit `.`, Wörter mit `-`, keine Umlaute, keine
Leerzeichen. Formate: `pdf`, `xml`, `jpg`, `png`.

Beispiele:

```
belege/2025/2025-03-01.musterhoster-server-februar.pdf
belege/2025/2026-01-20.zuwendungsbestaetigung-musterhilfe-2025.pdf
belege/ausgangsrechnungen/2025/2025-02-01.RE2025020001.nordlicht-labs.pdf
```

Dass die Zuwendungsbestätigung ein Datum aus 2026 trägt und trotzdem im Ordner
2025 liegt, ist gewollt: der Ordner ist der Veranlagungszeitraum, das Datum ist
das des Belegs.

## Regeln

- **Originalformat.** PDF bleibt PDF, XRechnung bleibt XML. Nicht
  drucken-und-scannen, nicht konvertieren, nicht mehrere Belege zu einer Datei
  zusammenfassen.
- **Abgelegte Belege werden nie verändert.** Eine Korrektur ist ein
  zusätzlicher Beleg.
- **Verknüpfung an der Buchung**, nicht im Dateinamen: `document:` für einen
  echten Beleg, `statement:` für einen Kontoauszug. `statement:` ist die
  Notlösung — wo Vorsteuer- oder Sonderausgabenabzug dranhängt, muss
  `document:` stehen.
- Geprüft wird mit `python3 scripts/check_belege.py --year <jahr>`. Exit 0
  heißt: jede belegpflichtige Buchung hat eine Datei, und jede Datei existiert.

## Aufbewahrung

Belegvorhaltepflicht statt Vorlagepflicht: Unterlagen werden auf Verlangen
vorgelegt und bis zum Ablauf eines Jahres nach Bekanntgabe der Steuerfestsetzung
aufbewahrt (Musterfall Spenden: § 50 Abs. 8 EStDV). Für den Betrieb gelten die
längeren Fristen der GoBD, siehe `docs/gobd-verfahrensdokumentation.md`.
