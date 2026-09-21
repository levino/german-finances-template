# Verfahrensdokumentation (GoBD)

Vorlage. Sie beschreibt, **wie** gebucht und aufbewahrt wird — im Prüfungsfall
ist sie der Nachweis, dass das Verfahren ordnungsgemäß ist. Wer das Verfahren
ändert, ändert dieses Dokument mit und trägt es in Abschnitt 8 ein.

Platzhalter in `<spitzen Klammern>` ersetzen.

## 1. Unternehmen und Umfang

| | |
|---|---|
| Unternehmen | `<Name, Anschrift>` |
| Tätigkeit | `<z. B. freiberufliche IT-Beratung>` |
| Steuernummer | `<Nr.>` |
| Gewinnermittlung | Einnahmenüberschussrechnung, § 4 Abs. 3 EStG |
| Umsatzsteuer | `<Regelbesteuerung / Kleinunternehmer>`, `<Ist- / Soll-Versteuerung>` |
| Aufzeichnungspflicht | § 22 UStG, § 147 AO |

## 2. Belegwesen

Eingangsbelege kommen digital (E-Mail, Kundenportal) oder auf Papier. Digitale
Belege werden im Originalformat abgelegt, Papierbelege gescannt; das Original
wird `<vernichtet / aufbewahrt>`.

Ablage: `belege/<jahr>/<belegdatum>.<kurzbeschreibung>.<ext>`,
Ausgangsrechnungen unter `belege/ausgangsrechnungen/<jahr>/`. Details in
`belege/README.md`.

**Unveränderbarkeit:** abgelegte Belege werden nicht verändert. Jede Änderung
ist ein zusätzlicher Beleg. Nachvollziehbar ist das über die
Versionsgeschichte des Repositories: jede Ablage und jede Buchung ist ein
Commit mit Zeitstempel und Urheber.

## 3. Buchführung

Doppelte Buchführung in Beancount, Textdateien unter `ledger/`. Kontenrahmen
in `ledger/accounts.beancount`. Betriebliche Buchungen laufen über
`Expenses:Betrieb:*` und `Income:Betrieb:*`.

- Betriebsausgaben werden **netto** gebucht, die Vorsteuer separat.
- Interne Übertragungen werden **einmal** gebucht, auf der ausgehenden Seite.
- Jede belegpflichtige Buchung trägt `document:` (Beleg) oder `statement:`
  (Kontoauszug). Welche Konten belegpflichtig sind, steht in
  `scripts/check_belege.json`.
- Jeder Import endet mit einer `balance`-Direktive aus dem Kontoauszug.

## 4. Datenherkunft

| Quelle | Weg | Ablage |
|---|---|---|
| `<Bank>` | `<CSV- oder PDF-Export>` | `data/raw/<bank>/` |
| `<Broker>` | `<Jahresauszug>` | `data/raw/<broker>/` |

Die Rohdaten bleiben unverändert liegen. Was daraus entsteht, ist reproduzierbar.

## 5. Prüfungen

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Formale Richtigkeit | `bean-check ledger/main.beancount` | keine Fehler |
| Belegpflicht | `python3 scripts/check_belege.py --year <jahr>` | Exit 0 |
| Salden | `balance`-Direktiven gegen die Kontoauszüge | im Ledger |

## 6. Aufbewahrung

Aufbewahrungsfristen nach § 147 Abs. 3 AO. Das Repository liegt auf
`<Ort>` und wird nach `<Ziel>` gesichert; Sicherungen werden `<Frequenz>`
geprüft. Für Jahre, deren Frist abgelaufen ist, gilt `<Regel>`.

## 7. Zugriff

| Person | Rolle | Rechte |
|---|---|---|
| `<Name>` | Inhaber | vollständig |
| `<Name>` | `<Steuerberatung / Agent>` | `<lesend / schreibend>` |

## 8. Änderungshistorie

| Datum | Version | Änderung |
|---|---|---|
| `<JJJJ-MM-TT>` | 1.0 | Erstfassung |
