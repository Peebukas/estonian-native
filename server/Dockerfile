# syntax=docker/dockerfile:1.7
#
# Builds silly-geese/estonian-mcp (Apache-2.0) at a pinned commit, without vendoring its code.
# All downloads happen at BUILD time. The running container needs no outbound network.
#
#   docker build -t estonian-mcp:a496fc6 server/
#   docker run -i --rm --network none estonian-mcp:a496fc6            # stdio
#
ARG ESTONIAN_MCP_REPO=https://github.com/silly-geese/estonian-mcp.git
ARG ESTONIAN_MCP_COMMIT=a496fc6daacc071ef3437b3bbfcafcca164ea249

# ---- builder ----
FROM python:3.13-slim AS builder
ARG ESTONIAN_MCP_REPO
ARG ESTONIAN_MCP_COMMIT

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 UV_LINK_MODE=copy UV_PROJECT_ENVIRONMENT=/opt/venv
COPY --from=ghcr.io/astral-sh/uv:0.5.18 /uv /usr/local/bin/uv
RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates curl unzip \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git init -q . \
 && git remote add origin "$ESTONIAN_MCP_REPO" \
 && git fetch -q --depth 1 origin "$ESTONIAN_MCP_COMMIT" \
 && git checkout -q FETCH_HEAD \
 && test "$(git rev-parse HEAD)" = "$ESTONIAN_MCP_COMMIT"

# Python dependencies from the project's lockfile (pinned hashes).
RUN uv sync --frozen --no-install-project --no-dev

# NLTK punkt_tab, fetched with curl and checked against the sha256 that NLTK's own
# index.xml published for it (checked 2026-10-21). NLTK republishes this archive in place
# from time to time; if the hash no longer matches, the build fails on purpose. Compare
# with https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml (package
# id="punkt_tab", attribute sha256_checksum) and update PUNKT_TAB_SHA256 after review.
# (Fetching by hand also avoids NLTK's downloader refusing hosts that resolve to proxy
# address ranges in some sandboxes.)
ARG PUNKT_TAB_SHA256=e57f64187974277726a3417ca6f181ec5403676c717672eef6a748a7b20e0106
RUN curl -fsSL --retry 3 -o /tmp/punkt_tab.zip \
      https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt_tab.zip \
 && echo "$PUNKT_TAB_SHA256  /tmp/punkt_tab.zip" | sha256sum -c - \
 && mkdir -p /opt/venv/nltk_data/tokenizers \
 && unzip -q -o /tmp/punkt_tab.zip -d /opt/venv/nltk_data/tokenizers \
 && rm /tmp/punkt_tab.zip

# Estonian WordNet via EstNLTK's own resource downloader (answers its [Y/n] prompt).
RUN echo "y" | /opt/venv/bin/python -c "from estnltk.wordnet import Wordnet; assert Wordnet()['kasutama']"

# Compressed Estonian fastText model from the project's release, MD5 as published upstream.
RUN mkdir -p /opt/models \
 && curl -fsSL --retry 3 -o /opt/models/fasttext-et-medium \
      https://github.com/silly-geese/estonian-mcp/releases/download/v0.1.0-models/fasttext-et-medium \
 && echo "3690ee9983fc95740a61125fd58ed385  /opt/models/fasttext-et-medium" | md5sum -c -

# Smoke test: sentence layer and morphology work offline.
RUN /opt/venv/bin/python -c "from estnltk import Text; t=Text('Kooli maja on suur. Teine lause siin.'); t.tag_layer(['sentences','morph_analysis']); assert len(list(t.sentences))==2"

# ---- runtime ----
FROM python:3.13-slim AS runtime
ARG ESTONIAN_MCP_COMMIT
LABEL org.opencontainers.image.source="https://github.com/silly-geese/estonian-mcp" \
      org.opencontainers.image.revision="${ESTONIAN_MCP_COMMIT}" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    ESTNLTK_MCP_FASTTEXT_PATH=/opt/models/fasttext-et-medium \
    ESTNLTK_MCP_METRICS_PATH=/tmp/estonian-mcp-metrics.json

RUN groupadd --system --gid 1000 app && useradd --system --uid 1000 --gid app --create-home app
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/models /opt/models
COPY --from=builder /app/server.py /app/LICENSE /app/NOTICE /app/
COPY --from=builder /app/data /app/data
# WordNet opens its SQLite DB read-write (journal file), so the runtime user needs write access.
RUN chown -R app:app /opt/venv/lib/python3.13/site-packages/estnltk/estnltk_resources
USER app

# Default: stdio for `docker run -i`. docker-compose.yml switches to HTTP.
ENTRYPOINT ["python", "/app/server.py"]
CMD ["--transport", "stdio"]
