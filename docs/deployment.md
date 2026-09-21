# Deployment

Die Vorlage baut eine statische Seite. Wie sie ausgeliefert wird, ist offen —
hier steht das Muster, das sich bewährt hat, samt der Fallen.

## Muster: CI baut das Image, GitOps rollt aus

1. Push auf `main` → CI baut das Container-Image und pusht es in eine Registry,
   getaggt mit **dem Commit**, zusätzlich `:latest`.
2. Die CI setzt danach den Tag im GitOps-Repo (Kubernetes-Manifest) auf den
   neuen Commit.
3. Argo CD (oder Flux) sieht die Änderung in git und rollt aus.

`.forgejo/workflows/build-site.yml` zeigt Schritt 1 und 2. Für GitHub Actions
ist es dieselbe Abfolge.

## Die Falle: `:latest` rollt nie aus

Ein GitOps-Werkzeug vergleicht **git** mit dem Cluster. Steht im Manifest ein
gleitendes `:latest`, bleibt diese Zeile für immer gleich, es gibt keinen
Unterschied, und es passiert nichts — egal wie oft ein neues `:latest` in der
Registry landet. `imagePullPolicy: Always` hilft nicht: die Policy greift erst,
wenn ein Pod **neu erzeugt** wird, und genau das löst niemand aus.

Das ist unauffällig, weil alles grün aussieht: die CI-Läufe sind erfolgreich,
die Images liegen in der Registry, die Anwendung läuft. Sie läuft nur mit dem
Stand vom ersten Tag. In einem echten Fall waren es drei Wochen und 97 grüne
Läufe.

Also: **exakten Commit pinnen**, und den Tag von der CI hochsetzen lassen.
Nebenbei entfällt `imagePullPolicy`, weil ein neuer Tag den Pull erzwingt.

Und den Tag nie aus einer Kurzform zusammensetzen — `git rev-parse HEAD` oder
aus der Registry kopieren. Ein erfundener voller Commit-Hash führt zu
`ImagePullBackOff`, und der Fehler sieht aus wie ein Rechteproblem.

## Prüfbar machen: eine Version-Route

Ohne Anmeldung ist von außen nicht zu sehen, welcher Stand läuft. Eine kleine
öffentliche Route, die Commit und Datenstand ausgibt, beantwortet die Frage in
einer Sekunde:

```json
{"commit": "…", "erzeugt": "2026-09-21T14:28:09+00:00", "gestartet": "…"}
```

Der Datenstand kann älter sein als der Commit: wenn sich nur die Seiten
geändert haben, nimmt der Image-Bau die Datenstufe aus dem Cache. Das ist
richtig so.

## Zwei Klassen von Geheimnissen

- **App-Geheimnisse** (OIDC-Client-Secret, Cookie-Schlüssel) gehören
  verschlüsselt ins GitOps-Repo, etwa als SealedSecret. Sie rotieren mit der
  Anwendung.
- **Infrastruktur-Zugänge** (Registry-Pull, git-Zugang des GitOps-Werkzeugs)
  gehören **nur** in den Cluster, direkt angelegt, nie ins Repo — auch nicht
  verschlüsselt. Ein versiegelter Infra-Schlüssel bleibt für immer in der
  Historie. Preis: sie sind nicht aus git reproduzierbar und müssen beim
  Neuaufbau von Hand erzeugt werden. Genau dafür gibt es ein Runbook.

Wird der Pull-Zugang gelöscht, merkt man es erst beim nächsten Rollout: der
laufende Pod bedient weiter, der neue kommt mit `401` nicht an das Image.

## Anmeldung vor der Seite

Die Seite enthält Belege und Steuerdaten, sie braucht eine Anmeldung. Wer sie
selbst baut, statt einen Proxy davorzustellen, muss die Reihenfolge kennen:

```
Header → öffentliche Routen → /auth/* → Wächter → statische Dateien → 404
```

Der Node-Adapter von Astro liefert im `standalone`-Modus das gebaute
Verzeichnis aus, **bevor** eigener Code läuft. Eine Prüfung in
`src/middleware.ts` sieht die vorgerenderten Seiten und die Beleg-PDFs
deshalb nie. Also: Adapter im `middleware`-Modus und die Reihenfolge selbst
bestimmen.

Der Wächter schaut sich den Pfad **nicht** an. Keine Regel „wenn Pfad mit X
beginnt, dann frei" — daran kommen doppelte URL-Kodierung und `..`-Segmente
vorbei. Frei ist nur, was vorher als Route registriert wurde.
