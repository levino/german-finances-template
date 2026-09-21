---
name: steuererklaerung
description: Arbeitsweise, Belegregeln und Rechtsstand für die deutsche Steuererklärung in diesem Repo — laden bei allen Arbeiten an Einkommensteuer, EÜR, Umsatzsteuer, Belegablage, den Anlagen KAP/Kind/Vorsorgeaufwand, der ELSTER-Übertragung und der GoBD-Dokumentation.
---

# Steuererklärung

Dieses Repo ist Buchführung **und** Steuerakte. Der Ledger ist das Rechenwerk,
`steuer/<jahr>/arbeitsmappe.md` ist die Feldquelle für ELSTER, `belege/` ist der
Nachweis. Diese drei sind nicht austauschbar.

## 0. Die Beleg-Regel

> **Beträge in einer Steuererklärung stammen ausschließlich aus Belegen.
> Der Ledger ist ein Suchindex, keine Belegquelle.**

- Eine Buchung sagt, dass Geld geflossen ist. Was geleistet wurde, ob
  Umsatzsteuer enthalten ist und ob der Betrag abzugsfähig ist, steht auf dem
  Beleg.
- Zuflüsse bei Kapitalerträgen sind **netto nach Steuerabzug**. Die Anlage KAP
  will **brutto laut Bescheinigung**. Ledger-Zahlen sind hier nur
  Plausibilitäts-Untergrenzen.
- Jeder Wert trägt einen Status. **Nie einen 🟡 zu 🟢 hochstufen, ohne dass eine
  Datei unter `belege/` existiert.**
- Fehlt ein Beleg oder steht eine Entscheidung aus: Eintrag in
  `steuer/<jahr>/STAND.md`, nicht schätzen. Ableitbares selbst entscheiden und
  einarbeiten; nur echte Entscheidungen des Mandanten dort auflisten.
- **Niemals** Buchungen erfinden, um eine Lücke zu schließen. Lücken werden
  benannt und durch beschaffte Kontoauszüge geschlossen.

## 1. Ablauf je Veranlagungszeitraum

`steuer/<jahr>/` enthält vier Dokumente mit klarer Rollenteilung:

| Datei | Rolle |
|---|---|
| `arbeitsmappe.md` | Feldquelle für ELSTER. Pro Formular eine Tabelle. Nichts anderes wird eingetippt. |
| `STAND.md` | die einzige Aufgabenliste: Belege besorgen, Entscheidungen. Erledigtes fliegt raus. |
| `erhebung.md` | die Lebenssituation: welche Sachverhalte liegen überhaupt vor. |
| `elster-kopf.md`, `elster-fuss.md` | Stammdaten und Hinweise für die Übergabe. |

1. **Erheben** (Skill `steuerinterview`), dann **Ledger aktualisieren**,
   `bean-check` grün.
2. **Kandidaten sammeln** — Konten durchsuchen, als 🟡 in die Arbeitsmappe, mit
   Fundstelle.
3. **Belege eintragen** — ablegen, `document:` setzen, auf 🟢 heben, Betrag
   **aus dem Beleg**. Weicht der Beleg vom Ledger ab, ist das ein Befund, kein
   Fehler: dokumentieren.
4. **Vollständigkeit prüfen** — `check_belege.py`, Abgleich gegen das Vorjahr:
   welche Position gab es damals, fehlt jetzt, und warum?
5. **Erst dann ELSTER** — `scripts/elster_uebergabe.py <jahr>`.

## 2. Summen rechnet das Skript

In der Wertspalte steht die Herleitung, nicht die abgeschriebene Zahl:
`[=](konto:Expenses:Spenden)`. Auszeichnungen: `site/README.md`. Wer Summen von
Hand schreibt, hat sie nach der nächsten Nachbuchung falsch — und merkt es nicht.

## 3. Umgang mit Recht und Zahlen

- **Rechtsstände nie aus dem Gedächtnis.** Grenzen, Pauschbeträge und
  Paragraphenfassungen ändern sich jährlich. Vor jeder Zahlenangabe die
  Primärquelle lesen (`gesetze-im-internet.de`, BMF) und die URL notieren. Was
  nur sekundär belegt ist, wird als solches gekennzeichnet.
- **Keine Steuerberatung.** Zulässig ist: Sachverhalte aufbereiten, Belege
  zuordnen, Zahlen rechnen, Rechtslage recherchiert darstellen, Alternativen mit
  Argumenten zeigen. Entscheiden muss die Person, der die Erklärung gehört.
- **Berichte Dritter prüfen, nicht glauben.** Ein Broker-Steuerreport kann
  Fremdbestände enthalten und fehlende Anschaffungsdaten als „worst case"
  ansetzen. Jede übernommene Zahl gegen eine zweite Quelle halten.
- **Vorjahresbescheid als Kalibrierung.** Er zeigt, welche Höchstbeträge
  tatsächlich gegriffen haben — das entscheidet, wie viel Aufwand eine Position
  lohnt.
- **Rechnen, nicht raten.** Aufteilungen (Schulgeld auf zwei Kinder, Beiträge
  auf Personen) sind eigene Herleitungen: als solche kennzeichnen und die
  Rechnung zeigen.

## 4. Wiederkehrende Fragen, die früh geklärt werden müssen

- **Freiberuflich oder gewerblich?** Entscheidet über Anlage S oder G,
  Gewerbesteuer und § 35 EStG. Uneinheitliche Veranlagung in Vorjahren ist ein
  Befund, der aufgelöst werden muss.
- **Kleinunternehmer oder Regelbesteuerung?** Bei Regelbesteuerung werden
  Betriebsausgaben **netto** angesetzt und die Vorsteuer separat. Wer das
  verwechselt, dreht die halbe EÜR.
- **Liebhaberei.** Mehrjährige Verluste ohne Umsätze führen zur Prüfung der
  Gewinnerzielungsabsicht. Dokumentation der Absicht ist Vorsorge.
- **Reverse Charge beim Leistungsbezug** (§ 13b UStG) aus dem Ausland ist bei
  Regelbesteuerung zahlungsneutral, aber **erklärungspflichtig**.

## 5. Das Freitextfeld

Die „Ergänzenden Angaben" (§ 150 Abs. 7 AO) sind freiwillig. Eine Eintragung
nimmt die Erklärung aus der automatischen Bearbeitung und legt sie einem
Amtsträger vor. Rechenwege gehören nicht hinein — die erfragt das Finanzamt bei
Bedarf. Hinein gehört höchstens ein Sachverhalt, bei dem man selbst will, dass
ein Mensch draufschaut.
