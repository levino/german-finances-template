# Zwei Stufen: Python erzeugt die Daten aus dem Ledger, Node baut die Seiten.
# Build-Kontext ist das Repo-Root (der Punkt am Ende von docker build).

FROM python:3.12-slim AS daten
RUN pip install --no-cache-dir beancount==3.2.3
WORKDIR /repo
COPY ledger/ ./ledger/
COPY belege/ ./belege/
COPY steuer/ ./steuer/
COPY data/ ./data/
COPY scripts/check_belege.json ./scripts/check_belege.json
COPY site/scripts/ ./site/scripts/
RUN python3 site/scripts/generate-data.py

FROM node:22-slim AS bau
WORKDIR /app
COPY site/package.json site/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY site/ ./
COPY --from=daten /repo/site/src/data/ ./src/data/
COPY --from=daten /repo/site/public/ ./public/
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=bau /app/dist/ /usr/share/nginx/html/
# Datenstand und Commit ablegen, damit von außen prüfbar ist, was läuft.
COPY --from=daten /repo/site/src/data/meta.json /usr/share/nginx/html/version.json
ARG GIT_SHA=""
ENV GIT_SHA=$GIT_SHA
EXPOSE 80
