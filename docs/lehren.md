# Lehren

Fehler, die in einem echten Durchgang passiert sind, und was daraus folgt.
Jeder Punkt hat einmal Zeit gekostet.

## Buchführung

**Kapitalertragsteuer gehört als eigene Buchung ins Buch.** Wer die Steuer im
Nettozufluss versteckt, kann Zeile 7 der Anlage KAP nicht füllen: die will den
Bruttoertrag laut Bescheinigung. Also `Income:Kapitalertraege` brutto,
`Expenses:Steuern:Kapitalertragsteuer` und `:Solidaritaetszuschlag` daneben.
Manche Banken buchen die Steuer als eigene Kontobewegung, andere nur netto —
bei letzteren braucht es je Jahr eine Nachbuchung laut Bescheinigung.

**Interne Transfers nur einmal buchen**, auf der ausgehenden Seite. Sonst steht
jeder Transfer doppelt im Buch, und die Summen beider Konten sind falsch.

**Betriebsausgaben netto, Vorsteuer eigenes Konto.** Bei Regelbesteuerung ist
die Vorsteuer ein durchlaufender Posten. Wer brutto bucht, dreht die halbe EÜR
falsch. `Expenses:Betrieb:Vorsteuer` sammelt sie und geht in die EÜR-Zeile für
die abziehbare Vorsteuer, nicht in die Kostenzeilen.

**Provisionen aus Devisengeschäften belasten das Konto.** Ein Generator, der
sie als Aufwand bucht, aber nicht vom Bestand abzieht, produziert eine
Abweichung, die jahrelang mitwächst. Am Ende stimmte der Saldo um 5,26 € nicht.
Gefunden nur, weil der Broker-Export einen Sollstand nennt, gegen den man
rechnen kann.

**Salden gegen eine externe Quelle prüfen, nicht gegen sich selbst.** Jeder
Import bekommt am Ende eine `balance`-Direktive aus dem Kontoauszug.

**Altjahre nicht umschreiben.** Stimmt ein Saldo nicht und die Erklärung ist
abgegeben, wird zum Jahreswechsel gegen das Kapitalkonto korrigiert — mit
Begründung in einer eigenen Datei, die kein Generator überschreibt.

## Belege

**Originalformat behalten.** PDF bleibt PDF, XRechnung bleibt XML. Nicht
drucken-und-scannen, nicht zusammenfassen, abgelegte Belege nie ändern. Eine
Korrektur ist ein zusätzlicher Beleg.

**Ein Beleg je Posten.** Wenn ein Feld aus drei Bescheinigungen besteht, stehen
drei Zeilen in der Arbeitsmappe und eine Summenzeile darüber. Wer nur die Summe
schreibt, kann später nicht zeigen, woraus sie besteht.

**Belegdatum ist das Rechnungsdatum, nicht das Zahlungsdatum.** Sonst findet
man den Beleg zur Buchung nicht wieder.

## Berichte von Dritten prüfen, nicht glauben

Ein Steuerreport eines Brokers wies in der Anlage KAP-INV einen Gewinn von über
100.000 € aus. Der Grund: seine Anfangsbestände standen auf null, also führte
er laufende Bestände als Leerverkäufe und setzte für Verkäufe ohne
Anschaffungsdaten nach eigener Aussage „the worst case scenario, which is that
the capital gain is equal to the whole proceeds" an. Zusätzlich enthielt er
Wertpapiere eines fremden Depots. Aus den Posten mit bekannten Kosten ergab
sich statt eines Gewinns ein Verlust.

Daraus: **jede Zahl aus einem fremden Report gegen eine zweite Quelle halten.**
Dividenden, Zinsen, einbehaltene Steuer und realisierte Ergebnisse lassen sich
aus dem Jahresauszug nachrechnen. Stimmen zwei unabhängige Exporte auf den
Cent, ist die Zahl belastbar — sonst nicht.

## Fristen und Verfahren

**Rechtsstände nie aus dem Gedächtnis.** Grenzen und Pauschbeträge ändern sich
jährlich. Vor jeder Zahlenangabe die Primärquelle lesen (Gesetzestext, BMF) und
die URL notieren. Was nur sekundär belegt ist, wird als solches gekennzeichnet.

**Das Freitextfeld ist freiwillig — und hat einen Preis.** Wer es füllt, nimmt
die Erklärung aus der automatischen Bearbeitung und legt sie einem Bearbeiter
vor. Rechenwege gehören nicht hinein, die erfragt das Finanzamt bei Bedarf.
Hinein gehört höchstens ein Sachverhalt, bei dem man selbst will, dass ein
Mensch draufschaut.

**Vorjahresbescheid als Kalibrierung.** Er zeigt, welche Höchstbeträge
tatsächlich gegriffen haben. Das entscheidet, wie viel Aufwand eine Position
noch lohnt.

## Werkzeuge

**Summen rechnet das Skript, nicht die Hand.** In der Arbeitsmappe steht die
Herleitung als Konto-Ausdruck, nicht die abgeschriebene Zahl. Sonst veralten
Summen still — und widersprechen sich irgendwann gegenseitig.

**Erklärender Text und Zahlen dürfen nicht doppelt gepflegt werden.** In einer
Übergabe an ELSTER standen einmal zwei Gewinne: die Tabelle rechnete korrekt,
ein Hinweistext nannte noch den Wert von vor einer Nachbuchung. Solche Texte
gehören gelöscht, nicht gepflegt.

**Kein „aktuelles Jahr".** Eine Oberfläche, die „das Jahr, an dem gerade
gearbeitet wird" berechnet, lässt fertige Jahre verschwinden und verlinkt von
einem Jahr ins andere. Jedes Jahr bekommt seinen Pfad, jede Übersicht listet
alle.
