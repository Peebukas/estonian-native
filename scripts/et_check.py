#!/usr/bin/env python3
"""Run the estonian-native verification battery against a LOCAL estonian-mcp server (stdio).

The script needs the `mcp` Python client library, so run it with the estonian-mcp
virtualenv's python (or any python with `mcp` installed).

Examples:
  ESTONIAN_MCP_ROOT=~/estonian-mcp ~/estonian-mcp/.venv/bin/python et_check.py text.txt
  ~/estonian-mcp/.venv/bin/python et_check.py text.txt --server-root ~/estonian-mcp \
      --glossary ../references/glossary-ecommerce.txt --words e-poe,liidestus --paradigm e-pood
  echo "tekst" | python et_check.py - --server-cmd "docker run -i --rm --network none estonian-mcp:a496fc6"

Server location (first match wins):
  --server-cmd "<command line>"     any command that speaks MCP over stdio (e.g. docker run -i ...)
  --server-root DIR / $ESTONIAN_MCP_ROOT
                                    an estonian-mcp checkout with .venv/ and server.py
  --server-python / $ESTONIAN_MCP_PYTHON  override the python used with --server-root
  --fasttext / $ESTNLTK_MCP_FASTTEXT_PATH  fastText model path (default: <root>/models/fasttext-et-medium,
                                    else the server's own default ~/.cache/estnltk-mcp/fasttext-et-medium)

On Linux the server is started inside `unshare -rn` (no network namespace) when available, so
no text can leave the machine. Use --no-unshare to disable. The script never edits the text;
it only reports JSON.
"""
import argparse, asyncio, json, os, shlex, shutil, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_GLOSSARY = os.path.normpath(os.path.join(HERE, "..", "references", "glossary-ecommerce.txt"))

BATTERY = [  # (tool, extra args)
    ("spell_check", {"suggestions": True}),
    ("check_compounds", {}),
    ("check_punctuation", {}),
    ("check_capitalization", {}),
    ("check_numbers", {}),
    ("check_abbreviation_hyphenation", {}),
    ("check_object_case", {}),
    ("check_redundancy", {}),
    ("check_officialese", {}),
    ("classify_register", {}),
]


def server_params(a):
    env = {"HOME": os.path.expanduser("~"), "PATH": os.environ.get("PATH", "/usr/bin:/bin")}
    glossary = a.glossary if a.glossary and os.path.exists(a.glossary) else None
    if a.server_cmd:
        # The command decides its own environment (e.g. docker -e ...); pass the glossary
        # path through only for commands that run on this filesystem.
        parts = shlex.split(a.server_cmd)
        if glossary:
            env["ESTNLTK_MCP_DOMAIN_GLOSSARY"] = os.path.abspath(glossary)
        cmd, args = parts[0], parts[1:]
    else:
        root = a.server_root
        if not root:
            sys.exit("Set --server-root or ESTONIAN_MCP_ROOT (an estonian-mcp checkout), or pass --server-cmd.")
        root = os.path.abspath(os.path.expanduser(root))
        py = a.server_python or os.path.join(root, ".venv", "bin", "python")
        cmd, args = py, [os.path.join(root, "server.py"), "--transport", "stdio"]
        fasttext = a.fasttext or os.path.join(root, "models", "fasttext-et-medium")
        if os.path.exists(fasttext):
            env["ESTNLTK_MCP_FASTTEXT_PATH"] = fasttext
        if glossary:
            env["ESTNLTK_MCP_DOMAIN_GLOSSARY"] = os.path.abspath(glossary)
    unshare = None if a.no_unshare else shutil.which("unshare")
    if unshare and sys.platform.startswith("linux"):
        return StdioServerParameters(command=unshare, args=["-rn", cmd, *args], env=env), bool(glossary)
    return StdioServerParameters(command=cmd, args=args, env=env), bool(glossary)


def parse(res):
    txt = "".join(getattr(c, "text", "") for c in res.content)
    try:
        return json.loads(txt)
    except Exception:
        # some tools stream several JSON objects back to back
        out, dec, i = [], json.JSONDecoder(), 0
        while i < len(txt):
            while i < len(txt) and txt[i].isspace():
                i += 1
            if i >= len(txt):
                break
            try:
                obj, j = dec.raw_decode(txt, i)
            except Exception:
                return txt
            out.append(obj); i = j
        return out


async def run(text, a, words, paradigm_words):
    report = {}
    params, has_glossary = server_params(a)
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            for tool, extra in BATTERY:
                res = await s.call_tool(tool, {"text": text, **extra})
                data = parse(res)
                if tool == "spell_check" and isinstance(data, list):
                    data = [d for d in data if isinstance(d, dict) and not d.get("spelling", True)]
                report[tool] = data
            res = await s.call_tool("check_compound_familiarity", {"text": text})
            fam = parse(res)
            if isinstance(fam, dict):
                fam = {"suspect_compounds": fam.get("suspect_compounds"),
                       "unattested": [c.get("lemma") for c in fam.get("unattested_compounds", [])]}
            report["check_compound_familiarity"] = fam
            if has_glossary:
                report["check_domain_terms"] = parse(await s.call_tool("check_domain_terms", {"text": text}))
                report["check_term_consistency"] = parse(await s.call_tool("check_term_consistency", {"text": text}))
            for wd in words:
                report.setdefault("spell_words", {})[wd] = parse(await s.call_tool("spell_check", {"text": wd, "suggestions": True}))
            for wd in paradigm_words:
                p = parse(await s.call_tool("paradigm", {"word": wd}))
                if isinstance(p, dict) and "forms" in p:
                    p = {f["form"]: f["surface"] for f in p["forms"]}
                report.setdefault("paradigm", {})[wd] = p
    return report


def main():
    ap = argparse.ArgumentParser(description="Estonian verification battery via a local estonian-mcp server.")
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--glossary", default=os.environ.get("ESTNLTK_MCP_DOMAIN_GLOSSARY", DEFAULT_GLOSSARY),
                    help="domain glossary, one term per line (default: references/glossary-ecommerce.txt)")
    ap.add_argument("--server-root", default=os.environ.get("ESTONIAN_MCP_ROOT"))
    ap.add_argument("--server-python", default=os.environ.get("ESTONIAN_MCP_PYTHON"))
    ap.add_argument("--server-cmd", default=os.environ.get("ESTONIAN_MCP_CMD"),
                    help="full stdio command line, e.g. 'docker run -i --rm --network none estonian-mcp:a496fc6'")
    ap.add_argument("--fasttext", default=os.environ.get("ESTNLTK_MCP_FASTTEXT_PATH"))
    ap.add_argument("--no-unshare", action="store_true", help="do not wrap the server in unshare -rn")
    ap.add_argument("--words", default="", help="comma-separated single words to spell-check")
    ap.add_argument("--paradigm", default="", help="comma-separated lemmas to inflect")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    words = [w.strip() for w in a.words.split(",") if w.strip()]
    pw = [w.strip() for w in a.paradigm.split(",") if w.strip()]
    print(json.dumps(asyncio.run(run(text, a, words, pw)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
