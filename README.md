# estonian-native

An agent skill for writing, translating and reviewing Estonian so it reads as native Estonian rather than translated English, with a mandatory grammar-check step against a local [estonian-mcp](https://github.com/silly-geese/estonian-mcp) server.

> **Eesti keeles:** estonian-native on tehisaruagendile mõeldud oskus (SKILL.md), mis aitab tõlkida ja toimetada eestikeelseid veebilehe-, e-poe- ja turundustekste nii, et need kõlaksid loomulikult. Oskus leiab tõlkekeele, kantseliidi ja tehisaru tüüpvead ning jätab hinnad ja muud faktid muutmata. Sõnavormide kontrolliks kasutab oskus sinu enda arvutis töötavat estonian-mcp serverit, nii et tekst ei lahku sinu masinast.

## What it does

- **Translate** English (or another language) into Estonian from the meaning, not the source sentence shape.
- **Review and rewrite** Estonian website, e-shop, UI, email and marketing copy: translationese, calques, kantseliit (officialese), AI-writing tells, wrong case, split compounds, abbreviation hyphens, commas, number formats.
- **Site reviews** with a machine-readable replacement ledger (exact original, proposed Estonian, reason, `facts_changed`, status), batch by batch, with coverage and open-question reports.
- **Protects facts**: prices, tax, terms, SLAs, durations, contacts, names, quotes, legal meaning, code, placeholders and CMS directives stay intact. No invented claims or promises.
- **Verifies** every Estonian text it produces with estonian-mcp (spell check, compounds, punctuation, capitalisation, numbers, abbreviation hyphens, object case, redundancy, officialese, register, glossary terms). If the tools are not available, it lists the forms it could not verify.

Client-specific rules (audience, address form, protected facts, rejected wording, extra glossary terms) go in a **client profile**, see [templates/client-profile-template.md](templates/client-profile-template.md) and the fictional [example](examples/client-profile-example-agency.md).

## Repository layout

```
SKILL.md                         the skill (frontmatter + instructions)
references/
  glossary.md                    Estonian e-commerce / web-agency terms with "avoid" variants
  glossary-ecommerce.txt         the same terms as an estonian-mcp domain glossary
  ai-tells-et.md                 28 Estonian AI-writing and translationese patterns
  ledger-format.md               replacement-ledger JSON format and status values
  verification.md                the mandatory estonian-mcp step, how to read results, known gaps
scripts/et_check.py              runs the verification battery against a local server (stdio)
templates/
  brief-template.md              per-run brief (source packet, scope, return format)
  client-profile-template.md     per-client rules
examples/
  client-profile-example-agency.md   a filled-in profile for a fictional agency
server/                          how to run estonian-mcp locally or self-hosted (no vendored code)
```

## Using the skill

The skill is a plain `SKILL.md` folder, so any agent that loads Agent Skills can use it.

- **Claude Code:** copy or clone the repository into `~/.claude/skills/estonian-native/` (or a project's `.claude/skills/`).
- **Cursor:** put it in your project's or user skills folder (for example `.cursor/skills/estonian-native/`), or reference `SKILL.md` from a rule.
- **Codex and other Agent Skills hosts:** copy it into the host's skills directory, for example `~/.agents/skills/estonian-native/`.
- **Agents without skill support:** paste `SKILL.md` into the system prompt or project instructions and attach the `references/` files.

Then ask in plain language, for example: "Translate this landing page into Estonian", "Review the Estonian copy on these pages and give me a ledger", or "Kas see tekst kõlab loomulikult?".

For a client job, give the agent a client profile and, for larger jobs, a brief from `templates/brief-template.md`.

## Connecting estonian-mcp

Set up the server first: see [server/README.md](server/README.md) (source install, Docker, self-hosted HTTPS with a bearer token, or systemd). Pinned upstream commit: `a496fc6daacc071ef3437b3bbfcafcca164ea249`.

### Cursor (`~/.cursor/mcp.json`)

Local stdio (recommended; Linux example with no network for the server):

```json
{
  "mcpServers": {
    "estonian-mcp": {
      "type": "stdio",
      "command": "/usr/bin/unshare",
      "args": ["-rn", "/home/you/estonian-mcp/.venv/bin/python", "/home/you/estonian-mcp/server.py", "--transport", "stdio"],
      "env": {
        "ESTNLTK_MCP_FASTTEXT_PATH": "/home/you/estonian-mcp/models/fasttext-et-medium",
        "ESTNLTK_MCP_DOMAIN_GLOSSARY": "/home/you/estonian-native/references/glossary-ecommerce.txt"
      }
    }
  }
}
```

On macOS or Windows, drop `unshare`: use the venv's python as `command` and start `args` at `server.py`. Docker works the same way: `"command": "docker"`, `"args": ["run", "-i", "--rm", "--network", "none", "estonian-mcp:a496fc6"]`.

Your own HTTPS server with a bearer token:

```json
{
  "mcpServers": {
    "estonian-mcp": {
      "url": "https://mcp.example.com/mcp",
      "headers": { "Authorization": "Bearer ${env:ESTONIAN_MCP_TOKEN}" }
    }
  }
}
```

Set `ESTONIAN_MCP_TOKEN` in the environment Cursor is launched from; do not paste the token into the file.

### Codex CLI

Local stdio (Linux example):

```sh
codex mcp add estonian-mcp -- /usr/bin/unshare -rn ~/estonian-mcp/.venv/bin/python ~/estonian-mcp/server.py --transport stdio
```

Self-hosted server with bearer authentication:

```sh
export ESTONIAN_MCP_TOKEN='<token-from-env-file>'
codex mcp add estonian-mcp --url https://<DOMAIN>/mcp --bearer-token-env-var ESTONIAN_MCP_TOKEN
```

or in `~/.codex/config.toml`:

```toml
[mcp_servers.estonian-mcp]
url = "https://<DOMAIN>/mcp"
bearer_token_env_var = "ESTONIAN_MCP_TOKEN"
```

`bearer_token_env_var` holds the *name* of the environment variable, not the token itself. The ChatGPT desktop app and Codex IDE extension also read this config file. See [server/README.md](server/README.md) for Apache + systemd deployment.

### ChatGPT (custom connector)

ChatGPT on the web reaches MCP servers through a custom connector in **developer mode** (streamable HTTP over HTTPS only; it cannot start a local stdio process). Add an app/connector with your server URL `https://<your-domain>/mcp`, then select it in the conversation.

**Important:** ChatGPT custom MCP connectors support only **OAuth 2.0 or no authentication**. They cannot send a static bearer token (`Authorization: Bearer <token>`). In OpenAI's own words from their [authentication documentation](https://platform.openai.com/docs/actions/authentication), ChatGPT "cannot present custom API keys" and does not support machine-to-machine OAuth grants. So:

- ✅ You can use a server with **no authentication** for public text
- ❌ You **cannot** connect ChatGPT web to a self-hosted server that requires a static bearer token
- ✅ Use the **ChatGPT desktop app** or **Codex** instead for bearer-authenticated servers (see the Codex section above)

Menu names change often; follow OpenAI's current [developer mode help article](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) and [Custom Actions documentation](https://platform.openai.com/docs/actions) for the exact path.

### Without an MCP connection

`scripts/et_check.py` starts the server itself over stdio and prints a JSON report:

```sh
ESTONIAN_MCP_ROOT=~/estonian-mcp ~/estonian-mcp/.venv/bin/python scripts/et_check.py text.txt \
  --words e-poe,liidestus --paradigm e-pood
```

Run `scripts/et_check.py --help` for all options (`--server-cmd` for Docker, `--glossary`, `--no-unshare`).

## Known estonian-mcp gaps (tested at a496fc6, October 2026)

- **liidestus** (integration): Vabamorf does not know it as a noun. `spell_check` flags "liidestust" and `paradigm` returns the verb *liidestuma*. The glossary wins here.
- **Abbreviations with case endings** such as "ERP-ga", "ERP-st", "SLA-d" can be reported as misspelled even when written correctly. If `check_abbreviation_hyphenation` is silent, they are fine.
- **Brand and platform names** (Magento, Hyvä, Shopify and the like) are flagged by `spell_check`.
- **Split compounds** are caught only from a small lexicon: "arendus tööd" and "hoolduse paketti" were not flagged. Read multi-noun phrases yourself.
- **Commas**: `check_punctuation` flags the compound conjunction "nii et" ("…, nii et tekst …"), which needs no comma between its parts; it does not check clauses starting with *kui*, *mis* or *kes*.
- `check_compound_familiarity` marks many correct specialist words as unattested (versiooniuuendus, ärieesmärk, tutvumisvestlus). Act only on `is_suspect: true`.

## Credits

- Structure and approach adapted from [oguzhankayan/turkish-native](https://github.com/oguzhankayan/turkish-native) (MIT).
- Grammar tooling: [silly-geese/estonian-mcp](https://github.com/silly-geese/estonian-mcp) (Apache-2.0), built on [EstNLTK](https://github.com/estnltk/estnltk) and Vabamorf. Not included in this repository; referenced by URL and commit.
- English AI-writing patterns referenced from [blader/humanizer](https://github.com/blader/humanizer) (MIT) and Wikipedia's "Signs of AI writing".

## License

MIT, see [LICENSE](LICENSE). estonian-mcp and its language resources keep their own licenses.
