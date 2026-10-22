# Zwei Stufen: Python erzeugt die Daten aus dem Ledger, Node baut die Seiten.
# Build-Kontext ist das Repo-Root (der Punkt am Ende von docker build).

FROM python:3.12-slim@sha256:cb33f7f771ecec2ef1225cf39b159591a040391bd73e4c01f00fdfc4c47611d2 AS daten
RUN pip install --no-cache-dir beancount==3.2.3
WORKDIR /repo
COPY ledger/ ./ledger/
COPY belege/ ./belege/
COPY steuer/ ./steuer/
COPY data/ ./data/
COPY scripts/check_belege.json ./scripts/check_belege.json
COPY site/scripts/ ./site/scripts/
RUN python3 site/scripts/generate-data.py

FROM node:22-slim@sha256:de170b39439eb0e5a3444ad7d60b015614a381e10fecae2e30ec9e735122f38d AS bau
WORKDIR /app
COPY site/package.json site/package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY site/ ./
COPY --from=daten /repo/site/src/data/ ./src/data/
COPY --from=daten /repo/site/public/ ./public/
RUN npm run build

FROM nginx:1.27-alpine@sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10
COPY --from=bau /app/dist/ /usr/share/nginx/html/
# Datenstand und Commit ablegen, damit von außen prüfbar ist, was läuft.
COPY --from=daten /repo/site/src/data/meta.json /usr/share/nginx/html/version.json
ARG GIT_SHA=""
ENV GIT_SHA=$GIT_SHA
EXPOSE 80
