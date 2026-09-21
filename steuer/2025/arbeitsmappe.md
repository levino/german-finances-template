# Arbeitsmappe 2025

Die Feldquelle für ELSTER. Was hier nicht steht, wird nicht eingetippt.

Aufbau: `## ` ist ein abzugebendes Formular, `### ` ein Block darin, `#### `
eine Gruppe. Die Tabelle enthält die Felder.

Werte stehen nicht abgeschrieben da, sondern als Herleitung:

| Schreibweise | Wirkung |
|---|---|
| `[=](konto:Expenses:Spenden)` | Summe des Kontos im Jahr |
| `[=](konto:A+B~Empfänger)` | mehrere Konten, `~` filtert auf einen Empfänger |
| `[=](konto:A+!A:B)` | `!` schließt ein Unterkonto aus (etwa die Vorsteuer aus dem Gewinn) |
| `[=](beleg:belege/2025/x.pdf)` | Summe der Buchungen zu genau diesem Beleg |
| `=` in einer Zeile mit „Summe" | summiert die Zeilen derselben Nummer in der Gruppe |
| `[Text](belege/…)` | verlinkt den Beleg und bettet ihn unter dem Block ein |

Status: 🟢 belegt · 🟡 Wert da, Beleg fehlt · 🔴 offen · ❓ zu entscheiden ·
⛔ bewusst nicht erklärt. Nur Buchungen mit `document:` oder `statement:`
zählen als belegt.

---

## Einkommensteuer

### Hauptvordruck

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| Art der Erklärung | Einkommensteuererklärung | — | 🟢 |
| 19 Veranlagungsart | Zusammenveranlagung | verheiratet, beide unbeschränkt steuerpflichtig | 🟢 |
| ⛔ 37 Ergänzende Angaben (§ 150 Abs. 7 AO) | keine | freiwilliges Feld; eine Eintragung nimmt die Erklärung aus der automatischen Bearbeitung. Rechenwege erfragt das Finanzamt bei Bedarf | ⛔ |

### Sonderausgaben

#### Zeile 5 — Spenden

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 5 Musterhilfe e.V. | [=](beleg:belege/2025/2026-01-20.zuwendungsbestaetigung-musterhilfe-2025.pdf) | [Zuwendungsbestätigung](belege/2025/2026-01-20.zuwendungsbestaetigung-musterhilfe-2025.pdf) | 🟢 |
| 5 Dorfverein Musterstadt | [=](konto:Expenses:Spenden~Dorfverein) | Kontoauszug vom 14.06.2025; vereinfachter Nachweis nach § 50 Abs. 4 EStDV, unter 300 € | 🟢 |
| **5 Summe** | = | | 🟢 |

Ohne Zuwendungsbestätigung nach amtlichem Muster ist keine Position ansetzbar;
der vereinfachte Nachweis reicht nur bis 300 € je Zuwendung.

#### Zeile 12 — Schulgeld

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 12 Freie Schule, August bis Dezember | [=](konto:Expenses:Kinder:Schulgeld) | [Schulgeldbestätigung](belege/2025/2026-02-10.schulgeldbestaetigung-2025.pdf) | 🟢 |
| 🔴 12 Januar bis Juli | offen | zweite Bestätigung der Schule fehlt, siehe STAND.md | 🔴 |

Abziehbar sind 30 % des Schulgelds, höchstens 5.000 € je Kind. Die Entgelte für
Beherbergung, Betreuung und Verpflegung zählen nicht mit.

### Vorsorgeaufwand

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 🔴 Krankenversicherung | offen | Jahresbescheinigung fehlt | 🔴 |
| 46 Haftpflichtversicherung | [=](konto:Expenses:Versicherungen:Haftpflicht) | [Beitragsrechnung](belege/2025/2025-07-15.musterversicherung-haftpflicht-2025.pdf) | 🟢 |

### Anlage KAP

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 4 Günstigerprüfung | ja | Meistbegünstigung von Amts wegen, kein Risiko | 🟢 |
| 7 Kapitalerträge mit Steuerabzug | [=](konto:Income:Kapitalertraege) | [Steuerbescheinigung](belege/2025/2026-03-05.steuerbescheinigung-musterbroker-2025.pdf), Bruttoertrag | 🟢 |
| 37 Kapitalertragsteuer | [=](konto:Expenses:Steuern:Kapitalertragsteuer) | dieselbe Bescheinigung | 🟢 |
| 38 Solidaritätszuschlag | [=](konto:Expenses:Steuern:Solidaritaetszuschlag) | dieselbe Bescheinigung | 🟢 |

Zeile 7 verlangt den **Bruttobetrag** laut Bescheinigung. Der Zufluss auf dem
Konto ist um die einbehaltene Steuer gekürzt und taugt nur als Untergrenze —
deshalb sind Ertrag und Steuer im Ledger getrennt gebucht.

### Anlage S

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 4 Gewinn aus freiberuflicher Tätigkeit | [=gewinn](konto:Income:Betrieb+Expenses:Betrieb+Expenses:Tech+!Expenses:Betrieb:Vorsteuer) | Übertrag aus der Anlage EÜR, Zeile 97 | 🟢 |

### Haushaltsnahe Aufwendungen

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 6 Handwerkerleistung, Rechnungsbetrag | [=](konto:Expenses:Haushaltsnah:Handwerker) | [Rechnung Dachdeckerei](belege/2025/2025-09-01.dachdeckerei-muster-dachreparatur.pdf) | 🟢 |
| 9 davon Lohnanteil | 287,00 | dieselbe Rechnung, Arbeitszeit und Fahrtkosten getrennt ausgewiesen; Material zählt nicht | 🟢 |

Die Steuerermäßigung beträgt 20 % der Arbeitskosten, höchstens 1.200 €.
Überwiesen, nicht bar — Barzahlung wäre schädlich.

---

## Anlage EÜR

### Betriebseinnahmen

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 14 Umsatzsteuerfreie Umsätze | [=](konto:Income:Betrieb:Honorare) | [Ausgangsrechnung RE2025020001](belege/ausgangsrechnungen/2025/2025-02-01.RE2025020001.nordlicht-labs.pdf); Leistungsort Singapur, § 3a Abs. 2 UStG | 🟢 |
| 18 Vereinnahmte Umsatzsteuererstattung | [=](konto:Income:Betrieb:Umsatzsteuererstattung) | Kontoauszug April 2025 | 🟢 |
| **Summe** | = | | 🟢 |

### Betriebsausgaben

#### Zeile 33 — Abschreibung

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 33 Büroeinrichtung | [=](konto:Expenses:Betrieb:Abschreibung) | [Rechnung Büromöbel](belege/2025/2025-01-15.bueromoebel-muster-schreibtisch.pdf), 1.560,00 netto auf 13 Jahre | 🟢 |

#### Zeile 57 — Abziehbare Vorsteuer

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 57 Vorsteuer aus Rechnungen | [=](konto:Expenses:Betrieb:Vorsteuer) | die Einzelrechnungen, je Buchung verknüpft | 🟢 |

#### Zeile 60 — Übrige Betriebsausgaben

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 60 Hosting | [=](konto:Expenses:Tech:Hosting) | Monatsrechnungen des Hosters | 🟢 |
| 60 Kontoführung | [=](konto:Expenses:Betrieb:Kontofuehrung) | Kontoauszüge, Entgelte mit Umsatzsteuer ausgewiesen | 🟢 |
| **60 Summe** | = | | 🟢 |

### Gewinnermittlung

| Zeile / Feld | Wert 2025 | Quelle | Status |
|---|---|---|---|
| 76 Summe Betriebseinnahmen | [=](konto:Income:Betrieb) | | 🟢 |
| 77 Summe Betriebsausgaben | [=](konto:Expenses:Betrieb+Expenses:Tech+!Expenses:Betrieb:Vorsteuer) | ohne Vorsteuer, die ist ein durchlaufender Posten | 🟢 |
| 97 Steuerpflichtiger Gewinn | [=gewinn](konto:Income:Betrieb+Expenses:Betrieb+Expenses:Tech+!Expenses:Betrieb:Vorsteuer) | | 🟢 |
