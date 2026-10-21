# Mandatory verification with estonian-mcp

Models produce confident, wrong Estonian inflections and compounds. Before returning any Estonian text you wrote or changed, run the checks below on it. Never assert a case form, spelling or compound split from memory when the tools are available.

Run [silly-geese/estonian-mcp](https://github.com/silly-geese/estonian-mcp) yourself (tested at commit `a496fc6daacc071ef3437b3bbfcafcca164ea249`; see `server/README.md`). The server makes no outbound network calls at runtime. For unpublished or confidential client copy, prefer your own instance over the public hosted endpoint (`estonian-mcp.fly.dev`), because the text would otherwise leave your machine.

## How to reach the tools

1. **Connected MCP server (preferred).** If the agent has estonian-mcp connected (tools named `spell_check`, `check_compounds`, `paradigm` and so on), call the tools directly.
2. **Script fallback (no MCP connection needed).** Save the Estonian text to a file, then run:

   ```
   ESTONIAN_MCP_ROOT=/path/to/estonian-mcp \
     /path/to/estonian-mcp/.venv/bin/python <this skill's dir>/scripts/et_check.py text.txt \
     [--glossary <this skill's dir>/references/glossary-ecommerce.txt] [--words word1,word2] [--paradigm lemma1,lemma2]
   ```

   It starts the local server over stdio (inside `unshare -rn`, with no network, when available on Linux), runs the standard battery with the glossary, and prints JSON. Run `et_check.py --help` for all options. It never edits the text.
3. **Neither available.** Do the review by hand, then mark every ledger item `"verification": "unverified"` and add an "Unverified forms" list to the output: each coined compound, each inflected form you were unsure of, each abbreviation with a case ending. Never write "verified" when the tools did not run.

## Standard battery (every Estonian text you produce)

| Tool | Catches |
|---|---|
| `spell_check` | Misspellings, with suggestions |
| `check_compounds` | Common split compounds (lexicon-based, low recall) |
| `check_punctuation` | Missing comma before et, sest, kuna, kuigi, kuid, vaid, nagu... (skips kui/mis/kes) |
| `check_capitalization` | Weekdays, months, nationalities, language adjectives |
| `check_numbers` | Decimal and thousands separators |
| `check_abbreviation_hyphenation` | OÜle, APIga style errors |
| `check_object_case` | Object case after negation and partitive verbs |
| `check_redundancy` | Pleonasms (samuti ka, kõige optimaalsem) |
| `check_officialese` | Kantseliit: -mine nouns, impersonal voice, poolt, support verbs, long sentences |
| `classify_register` | Register and mixed-register flag (heuristic, 25+ words) |
| `check_compound_familiarity` | Compounds you coined that look invented (`is_suspect`) |
| `check_domain_terms`, `check_term_consistency` (with the glossary) | Terms outside the client glossary; one concept with several terms |

On demand: `paradigm` (all forms of a lemma), `analyze_morphology` (what form a word is), `synonyms` (WordNet senses with definitions), `find_related_words` (adjacent concepts; may return antonyms and inflections).

## Reading the results

- Fix every true hit. For a false positive, keep the text and say why in one line.
- `spell_check` passes any well-formed compound, including invented ones. Passing is not proof a word exists; run `check_compound_familiarity` on compounds you coined.
- `attested: false` from `check_compound_familiarity` is normal for correct specialist words (versiooniuuendus, ärieesmärk, digitöötaja, tutvumisvestlus are all unattested in its vocabulary). It is never a reason to rewrite on its own. Act only on `is_suspect: true`.
- `check_compounds` and `check_punctuation` have low recall. No hits does not mean no errors; read multi-noun phrases and kui/mis/kes clauses yourself.
- Keep tool mechanics out of the deliverable. Report what you changed and why, not what the tool said.
- A native speaker's correction beats the tool. Take it.

## Known gaps (tested 2026-10-21)

- **liidestus**: Vabamorf does not know it as a noun. `spell_check` flags "liidestust" and `paradigm("liidestus")` returns the verb "liidestuma". The glossary is authoritative here: liidestus, liidestuse, liidestust, liidestusi; "liidestus ERP-ga".
- **Abbreviation + ending** such as "ERP-ga", "ERP-st" or "SLA-d" can come back from `spell_check` as misspelled with no suggestions. If `check_abbreviation_hyphenation` is silent and the hyphen rule is followed, it is fine.
- `check_compounds` did not flag "arendus tööd" or "hoolduse paketti" in testing. Do not rely on it for those.
- Brand names, platform names (for example Magento, Hyvä) and English product names are flagged by `spell_check`; skip them.
