# estonian-mcp in action: Documentation quality check

This document shows how estonian-mcp tools were used to check Estonian technical documentation before publication. Names, hostnames, ports and deployment details have been removed.

## Setup

- **Server:** Self-hosted deployment via HTTPS with bearer authentication
- **Client:** Python JSON-RPC client over Streamable HTTP
- **Document:** Server deployment and operations documentation in Estonian (~1,000 words)
- **Tools called:** 12 out of 27 available tools
- **Process:** Three rounds of checks with fixes between rounds

## What was checked

The Estonian prose (table cells, labels, flowchart labels and plain-text descriptions) was extracted and checked. Code blocks, inline code, commands, URLs and identifiers were skipped.

## Rounds

| Tool | Round 1 | Round 2 | Round 3 (final) | Outcome |
|---|---|---|---|---|
| `spell_check` | 135 unique words flagged | 113 | 113 | 5 real fixes. The rest are brand/product names (Apache, ChatGPT, fastText), English quotes, UI labels, file/tool names, technical loanwords (token, commit) and a deliberate test string in the examples: accepted as correct |
| `check_compound_familiarity` | 2 suspect compounds | 0 | 0 | Both fixed |
| `check_officialese` | 1 (long sentence) | 1 | 0 | Fixed by restructuring |
| `check_punctuation` | 4 | 4 | 4 | False positives: all 4 are "…, nii et …" where the comma correctly comes before "nii" per EKI rules |
| `check_numbers` | 15 | 15 | 15 | False positives: times like "kell 9.25" correctly use a period per Estonian convention, and "Python 3.12" / "OAuth 2.1" are version numbers |
| `check_object_case` | 9 | 9 | 9 | False positives: an English quote, "mitte haru" (no verb present), and subjects of negated verbs (correctly nominative) |
| `check_term_consistency` | 22 groups | 21 | 21 | Reduced one deliberate variant ("bearer-token" → "token") in 3 places. The other groups are intentional pairs: a long form vs short form, or a colloquial term in the plain-words section vs the technical term elsewhere |
| `check_domain_terms` | 30 unlisted compounds | 29 | 29 | Info only. Technical terms not in the server's glossary (which was for a different domain) — none were suspect |
| `check_compounds`, `check_capitalization`, `check_abbreviation_hyphenation`, `check_redundancy` | 0 | 0 | 0 | Clean |
| `classify_register` | neutral, not mixed | neutral | neutral | Appropriate for technical documentation |
| `paradigm` (on demand) | — | — | — | Used to verify case forms for replacement candidates |

## What changed

### 1. Suspect compounds (2 fixes)

**Issue:** `check_compound_familiarity` flagged two compounds as unattested and suspect (not in the corpus vocabulary, and fastText neighbors under 0.55 similarity).

- "systemd turvaseaded" → "systemd turvasätted"
- "Codexi seadistuse ja CLI viitelehe järgi" → "… CLI juhendi järgi"

**Reason:** "turvaseaded" and "viiteleht" were flagged as suspect compounds; "turvasätted" and "juhend" are the attested native forms.

### 2. Unattested compounds ending in "-logi" (2 fixes)

**Issue:** `spell_check` rejected compounds ending in "-logi" because the standalone "logi" is not in the lexicon, though "-logi" is a valid compound ending.

- Table row labels: "Pöördumislogi" → "Päringute logi", "Vealogi" → "Vigade logi"

**Reason:** The model's vocabulary doesn't include "-logi" as a noun, so it rejects compounds built on it. The replacement uses the full noun form "päringute/vigade logi" instead of the compound.

### 3. Unstable noun (1 fix)

**Issue:** `spell_check` rejected "viipadesse" (illative plural of "viip" = HTTP request).

- "Ära pane tokenit jagatud viipadesse" → "Ära kirjuta tokenit jagatud päringutesse ega vestlustesse"

**Reason:** The noun "viip" has an unstable paradigm (paradigm check showed partial forms); "päring" is the stable, attested term.

### 4. Repository vs hoidla (1 fix)

**Issue:** `spell_check` rejected "repositoorium" (a loanword from English "repository").

- "sellesse repositooriumisse" → "sellesse hoidlasse"
- "Repositooriumi faile" → "Lähtekoodi hoidla faile"

**Reason:** The native Estonian term is "hoidla" (storage place, archive); "repositoorium" is not recognized.

### 5. Long sentence (1 fix)

**Issue:** `check_officialese` flagged a 28-content-word sentence as bureaucratically long for non-legal prose.

- Before: "Tulemused paigaldamise ajal (…):" (followed by a bullet list)
- After: "Paigaldamise ajal (…) olid tulemused järgmised." (then the list)

**Reason:** The sentence introduced a list with a colon at the end of a long clause. Restructuring made it a standalone sentence with a clear subject and verb before the enumeration.

## False positives and accepted warnings

### Punctuation: "nii et" with comma

`check_punctuation` flagged 4 instances of "…, nii et …" as missing a comma. These are **false positives**: per EKI orthography rules, the comma correctly comes *before* "nii" when "nii et" introduces a result clause.

### Numbers: Estonian time and version formats

`check_numbers` flagged 15 instances:
- Times like "kell 9.25" (the period is correct in Estonian time notation)
- Version numbers like "Python 3.12", "OAuth 2.1" (correctly use a period, not a comma)

These are **false positives**: the tool's rule (use a comma for decimals) doesn't distinguish time/version notation from numeric values.

### Object case: quotes and no-verb contexts

`check_object_case` flagged 9 instances:
- One English quote: "cannot present custom API keys"
- "mitte haru" (not a branch) — no verb, so no object case applies
- Subjects of negated verbs (nominative is correct): "veebiliides ei saa", "limiit ei kehti", "režiim ei toeta"

These are **false positives**: the rule expects accusative/partitive after negated verbs, but these are subjects (nominative), not objects.

### Term consistency: deliberate variants

`check_term_consistency` grouped 21 term sets where multiple forms appear. Most are **intentional**:
- "töölauarakendus" (full form) vs "rakendus" (short form)
- "salasõna" (plain-words section) vs "token" (technical sections)
- "bearer-token" → unified to "token" (the one real change)

The tool correctly identified synonym groups; the user chose to keep most variants for readability.

### Domain terms: technical vocabulary

`check_domain_terms` reported 29 technical compounds not in the server's glossary (systemd, vhost, liivakastireeglid, töölauarakendus, etc.). These are **expected**: the server's glossary was for e-commerce, not system administration. None were flagged as suspect or coined.

## Flowchart validation

Both the English and Estonian mermaid flowcharts were rendered with `@mermaid-js/mermaid-cli` 11:
- Exit code: 0 (syntax valid)
- Output: SVG written successfully
- Labels with special characters were correctly quoted

## Summary

- **27 tools available**, 12 used
- **~1,000 words** of Estonian prose checked
- **5 real issues found and fixed** over 3 rounds
- **Remaining flags (51 total):** false positives (punctuation, numbers, object case) or accepted variants (term consistency, domain terms)
- **Register classification:** neutral (appropriate for technical docs)
- **Processing:** Real-time JSON-RPC calls over HTTPS with bearer auth

The tools caught unattested compounds, unstable noun forms and one long sentence that a human proofreader might have missed. False positives were explainable and consistent (rule-based checks applied to edge cases outside their design scope).

## Tools not shown here but available

The following tools were not needed for this document, but are part of the 27-tool set:

- `tokenize`, `analyze_morphology`, `lemmatize`, `pos_tag`: morphological analysis
- `syllabify`: syllable boundaries with quantity and accent
- `named_entities`: people, places, organizations
- `synonyms`: Estonian WordNet synsets
- `find_related_words`: fastText semantic neighbors
- `check_style`: repetition, hedging, sentence-length variance
- `check_hyphenation`: safe line-break positions
- `check_legalese`, `check_defined_terms`, `common_legal_usage`: legal text tools

See the main [README.md](../README.md) for the full tool list and descriptions.
