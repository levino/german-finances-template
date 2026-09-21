# Agenten-Anweisungen

Dieses Repo ist Buchführung **und** Steuerakte. Ledger, Belegablage und
Arbeitsmappe sind drei Rollen, nicht austauschbar — siehe `README.md`.

<beleg-regel>
Beträge in der Steuererklärung stammen aus Belegen, nicht aus dem Ledger. Ein
🟡 wird nie zu 🟢 ohne Datei unter `belege/`. Fehlt ein Beleg: Buchung stehen
lassen, fehlenden Beleg in `steuer/<jahr>/STAND.md` benennen, Position nicht
übertragen. Niemals eine Buchung erfinden, um eine Lücke zu schließen.
</beleg-regel>

<ledger>
- Interne Transfers: **eine** Buchung, auf der ausgehenden Seite.
- Betriebsausgaben netto, Vorsteuer auf `Expenses:Betrieb:Vorsteuer`.
- Kapitalerträge brutto, einbehaltene Steuer auf eigene Konten.
- Jeder Import endet mit einer `balance`-Direktive aus dem Kontoauszug.
- Nach jeder Änderung: `bean-check ledger/main.beancount`.
- Generierte Dateien nicht von Hand korrigieren — Parser oder Rohdaten ändern.
  Handkorrekturen gehören in `ledger/korrekturen.beancount`.
</ledger>

<belege>
`belege/<jahr>/<JJJJ-MM-TT>.<kurzbeschreibung>.<ext>`, Datum = Belegdatum.
Ausgangsrechnungen unter `belege/ausgangsrechnungen/<jahr>/`. Keine Umlaute,
keine Leerzeichen. Verknüpfung über `document:` (Rechnung) oder `statement:`
(Kontoauszug) an der Buchung. Originalformat behalten, abgelegte Belege nie
ändern. Prüfen: `python3 scripts/check_belege.py --year <jahr>`.
</belege>

<arbeitsmappe>
`steuer/<jahr>/arbeitsmappe.md` ist die Feldquelle für ELSTER, nichts anderes
wird eingetippt. Summen rechnet das Skript: in der Wertspalte steht
`[=](konto:…)`, nicht die abgeschriebene Zahl. Struktur und Auszeichnungen:
`site/README.md`.
</arbeitsmappe>

<recht>
Rechtsstände nie aus dem Gedächtnis. Vor jeder Zahlenangabe die Primärquelle
lesen und die URL notieren; sekundär Belegtes als solches kennzeichnen.
Keine Steuerberatung: aufbereiten, rechnen, Alternativen mit Argumenten zeigen.
Strittige Punkte gehören in `STAND.md`, entschieden wird von der Person, der
die Erklärung gehört. Entscheidungen dort mit Datum festhalten, damit sie nicht
zweimal gefragt werden.
</recht>

<niemals>
- Keine Schätzungen, keine erfundenen Buchungen, keine erfundenen Belege.
- Keine personenbezogenen Daten in Commit-Nachrichten (IBANs, Steuernummern).
- Keinen kurzen Commit-SHA zu einem vollen aufblasen — immer `git rev-parse`.
</niemals>

<befehle>
```bash
bean-check ledger/main.beancount
python3 scripts/check_belege.py --year 2025
python3 scripts/elster_uebergabe.py 2025
cd site && npm run alles && npm start
```
</befehle>
