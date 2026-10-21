# Replacement ledger format

Use for site reviews, multi-page work, or whenever the user asks for a ledger. One item per replaced string. Group items by page family: shared UI, homepage, contact, services, about, portfolio, blog/shop UI, technical articles, legal.

## Item

```json
{
  "record_identifier": "cms_block_contact_et",
  "page_url": "/et/kontakt",
  "original": "EXACT CURRENT TEXT",
  "replacement_et": "PROPOSED TEXT",
  "reason": "Brief language/context reason",
  "facts_changed": false,
  "status": "language_edit"
}
```

Required fields:

| Field | Rule |
|---|---|
| `record_identifier` | The CMS block/page/attribute ID from the source map. Never invent one; if the source has none, use `page_url` + a short locator and say so in `reason`. |
| `page_url` | Route as given in the source (`/et/...`). |
| `original` | Exact current text, character for character, including spacing and punctuation. If it contains markup or CMS directives, copy them exactly. |
| `replacement_et` | Proposed Estonian. All markup, directives, placeholders, links and IDs from `original` present and unchanged. |
| `reason` | One short line: what was wrong (calque, case, compound, tone, CTA accuracy, terminology) and why the new text fits the page. |
| `facts_changed` | `false` for every language edit. `true` only with `status: "needs_business_decision"`. |
| `status` | One of the values below. |

Optional fields (add when useful, never instead of the required ones): `source_hash` (copy from the source map), `group`, `verification` (`"verified"` / `"unverified: <forms>"`), `notes`.

## Status values

| Status | Use when |
|---|---|
| `language_edit` | Grammar, spelling, word choice, natural phrasing. Meaning and facts unchanged. |
| `terminology` | Change made only to apply the glossary. |
| `cta_clarity` | Button or link text rewritten so it names the real next step (same destination, same offer). |
| `format_only` | Number, date, time or currency notation changed; value unchanged. |
| `legal_language_flag` | Legal/privacy/cookie text: language-only proposal, needs the owner's (or a lawyer's) sign-off. |
| `needs_business_decision` | The current text is ambiguous, contradicts another page, or a better wording would change an offer, price, term, SLA or claim. Propose options; do not pick one silently. |
| `no_change` | Reviewed and already natural. Use sparingly, for strings someone might expect to be changed (for example rejected-example candidates that turned out fine). |

## Rules

- Never put a rewritten customer quotation in a ledger; quotations get `no_change` or, for an obvious typo, `needs_business_decision`.
- One item per distinct string. If the same string appears on many pages (header, footer), list it once under shared UI with all `record_identifier`s in `notes`.
- After the ledger for a batch, give the full revised copy of each page in that batch in reading order, so the owner can read it as a visitor would.
- Return valid JSON (an array per group) when the user or the brief asks for machine-readable output; otherwise a Markdown table with the same columns is fine.
