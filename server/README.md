# Running estonian-mcp yourself

The skill's verification step uses [silly-geese/estonian-mcp](https://github.com/silly-geese/estonian-mcp) (Apache-2.0), an MCP server built on EstNLTK and Vabamorf. This folder does **not** contain its code. Every option below fetches it from GitHub at the pinned commit:

```
https://github.com/silly-geese/estonian-mcp.git
commit a496fc6daacc071ef3437b3bbfcafcca164ea249   (v0.7.1, 2026-10-17)
```

Review the upstream code yourself before trusting it with confidential text. Upstream also runs a free public server (`https://estonian-mcp.fly.dev/mcp`). That is fine for public text, but unpublished client copy is better checked on your own machine.

**Recommendation:** the server needs network access only while you install it. Run it with outbound network blocked: `--network none` / an `internal` Docker network, `unshare -rn`, or systemd `IPAddressDeny=any`.

## Option A: source install, stdio (simplest, Linux/macOS)

Requires `git` and [`uv`](https://docs.astral.sh/uv/).

```sh
git clone https://github.com/silly-geese/estonian-mcp.git ~/estonian-mcp
cd ~/estonian-mcp
git checkout a496fc6daacc071ef3437b3bbfcafcca164ea249
UV_PROJECT_ENVIRONMENT=$PWD/.venv uv sync --frozen --no-install-project --no-dev

# Language resources (one-time, needs network). Read the script first.
mkdir -p models
ESTNLTK_MCP_FASTTEXT_PATH=$PWD/models/fasttext-et-medium .venv/bin/python scripts/fetch_resources.py </dev/null
```

`fetch_resources.py` downloads three things: NLTK `punkt_tab`, Estonian WordNet (via EstNLTK's own downloader) and a compressed fastText model from the project's GitHub release (MD5-checked).

### If punkt_tab fails ("SSRF attempt to restricted IP")

NLTK's downloader refuses hosts that resolve to private or reserved address ranges, which happens behind some proxies and sandboxes. Fetch it by hand and check the sha256 that NLTK publishes in its `index.xml` (package `punkt_tab`, attribute `sha256_checksum`):

```sh
curl -fsSL https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml | grep -o '<package id="punkt_tab"[^>]*>'
curl -fsSL -o /tmp/punkt_tab.zip https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt_tab.zip
echo "e57f64187974277726a3417ca6f181ec5403676c717672eef6a748a7b20e0106  /tmp/punkt_tab.zip" | sha256sum -c -
mkdir -p .venv/nltk_data/tokenizers && unzip -q -o /tmp/punkt_tab.zip -d .venv/nltk_data/tokenizers
.venv/bin/python scripts/fetch_resources.py </dev/null   # should now say "All resources present"
```

The hash above is the one NLTK published on 2026-10-21. NLTK republishes this archive in place from time to time, so if it no longer matches, compare it with the current `index.xml` before you accept the new file.

### Launch command (stdio)

```
command: /usr/bin/unshare        # Linux only; drop it (and "-rn") elsewhere
args:    -rn ~/estonian-mcp/.venv/bin/python ~/estonian-mcp/server.py --transport stdio
env:     ESTNLTK_MCP_FASTTEXT_PATH=~/estonian-mcp/models/fasttext-et-medium
         ESTNLTK_MCP_DOMAIN_GLOSSARY=/path/to/estonian-native/references/glossary-ecommerce.txt   (optional)
```

`unshare -rn` starts the server in an empty network namespace (no outbound calls possible). Use absolute paths in MCP client configs; most clients do not expand `~`.

## Option B: Docker, stdio

```sh
docker build -t estonian-mcp:a496fc6 server/
docker run -i --rm --network none estonian-mcp:a496fc6
```

The [Dockerfile](Dockerfile) clones upstream at the pinned commit, installs from the lockfile, fetches punkt_tab with the sha256 check above, WordNet and the fastText model (MD5-checked) at **build** time, and runs as a non-root user. To use a glossary, mount it and set the variable:

```sh
docker run -i --rm --network none \
  -v "$PWD/references/glossary-ecommerce.txt:/glossary.txt:ro" \
  -e ESTNLTK_MCP_DOMAIN_GLOSSARY=/glossary.txt estonian-mcp:a496fc6
```

## Option C: self-hosted HTTPS with a bearer token (Docker Compose + Caddy)

For several people or a remote agent:

```sh
cd server
cp .env.example .env          # set DOMAIN and ESTNLTK_MCP_AUTH_TOKEN (32+ random bytes)
docker compose up -d --build
```

- [docker-compose.yml](docker-compose.yml): estonian-mcp in HTTP mode on an `internal: true` network (no internet route), Caddy in front with automatic HTTPS.
- [Caddyfile](Caddyfile): exposes only `/mcp` and `/health`; `/metrics`, the landing page and everything else return 404; access logs discarded.
- estonian-mcp checks `Authorization: Bearer <token>` itself (`ESTNLTK_MCP_AUTH_TOKEN`, minimum 16 characters) and refuses to start in HTTP mode without one.
- Endpoint for clients: `https://<DOMAIN>/mcp` (streamable HTTP).

Never commit `.env`.

## Option D: systemd (source install, HTTP on localhost)

[estonian-mcp.service](estonian-mcp.service) runs a source install from `/opt/estonian-mcp` on `127.0.0.1:8081` for a reverse proxy on the same host (Caddy, nginx). The token comes from `/etc/estonian-mcp.env`, and `IPAddressDeny=any` with `IPAddressAllow=localhost` blocks outbound traffic. Put your proxy in front with HTTPS and expose only `/mcp` (and `/health` if you monitor it).

## ChatGPT and other clients without custom headers

ChatGPT's web custom connectors (developer mode) accept OAuth, no authentication, or mixed authentication. They cannot send a static bearer token, so Option C will not work there as-is. Your choices:

- Upstream's own `deploy/` stack (nginx with an OAuth client flow, `deploy/new-oauth-client.sh`) at the same commit. Read its `deploy/README.md`.
- A client that can send a header (Cursor, Claude Code, Codex, the ChatGPT desktop app per OpenAI's current docs).
- No authentication, only for public, non-confidential text.

Check OpenAI's [developer mode help article](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) for the current options; they have changed before.

## License

estonian-mcp is © its contributors, licensed under Apache-2.0 (see its `LICENSE` and `NOTICE`). The files in this folder are MIT, like the rest of this repository.
