# Estonian AI tells and translationese

Diagnostic patterns, not search-and-replace rules. Context wins: a pattern used on purpose by a native writer is not an error. Several tells together are the signal. The estonian-mcp tool that helps detect each pattern is named in brackets.

Each "Instead" line shows direction. Verify any new form you write (see `verification.md`).

## A. Sentence architecture

**1. English word order and clause shape.** The sentence follows the English skeleton: heavy subject first, verb late, prepositional chains turned into "jaoks/kohta/osas" chains.
Before: "Meie meeskonna poolt pakutavate lahenduste eesmärgiks on sinu e-poe jaoks väärtuse loomine."
Instead: "Aitame sinu e-poel rohkem müüa ja vähem käsitsi teha." (only if the source says so)

**2. "Poolt" passive calque.** English "by X" passive. [check_officialese: poolt-calque]
Before: "meie poolt arendatud moodul", "tellimused töödeldakse süsteemi poolt"
Instead: "meie arendatud moodul", "süsteem töötleb tellimused"

**3. Impersonal -takse/-ti where the actor is known.** Hides who does the work; in agency copy the actor is almost always "meie" or "sina". [check_officialese: impersonal-voice, check_style]
Before: "Projekti alguses analüüsitakse e-poe hetkeolukorda."
Instead: "Alguses vaatame üle, kuidas sinu e-pood praegu töötab."

**4. -mine nominalisation stacks.** Action turned into a noun, often with a support verb. [check_officialese: nominalisation]
Before: "Arenduse läbiviimine toimub peale nõuete kaardistamist."
Instead: "Kui nõuded on kirjas, hakkame arendama."

**5. Support verbs: teostama, läbi viima, toimuma, omama.** [check_officialese: officialese-filler]
Before: "Teostame versiooniuuenduse", "Omame pikaajalist kogemust", "Koolitus toimub veebis"
Instead: "Uuendame platvormi versiooni", "Meil on X aastat kogemust" (only with the real number), "Koolitus on veebis"

**6. Clause stacking and long sentences.** Several subordinate clauses chained with "mis", "et", "kuna". [check_officialese: clause-stacking / long-sentence, check_style]
Instead: split; first what happens, then what comes of it.

**7. "See ei ole X, see on Y" and "mitte ainult X, vaid ka Y".** English not-X-but-Y. Keep only when the negative half corrects a real belief.
Before: "See ei ole lihtsalt e-pood, see on sinu äri süda."
Instead: cut, or state the fact.

## B. Words and calques

**8. Anglicisms where Estonian has a normal word.** skoop, deliverable, lead, checkout, upgrade, fiks, apgreidima, launchima, feature (as "fiitšer"). See glossary. [spell_check flags many; check_domain_terms with glossary]

**9. Generic agency vocabulary.** visioon, innovaatiline, terviklahendus, optimeerimine, sünergia, lisaväärtus, personaalne lähenemine, kvaliteetne teenus, professionaalne meeskond. Replace with the concrete deliverable or cut.

**10. "Lahendus" as filler.** "Pakume lahendusi" says nothing. Name the moodul, liidestus, hoolduspakett, automatiseerimine.

**11. Slogan calques.** "viime su äri järgmisele tasemele", "sujuv kogemus", "kõik ühest kohast", "sinu edu on meie edu". Cut or state the concrete benefit the source supports.

**12. Promise inflation.** "tagame", "garanteerime", "alati", "kohe", "100%" where the source does not promise it. This is a fact change, not style. Flag it.

**13. Overused "jaoks", "osas", "kohta".** Case endings do this job. [check_style repetition]
Before: "Lahendused e-poodide jaoks hoolduse osas"
Instead: "E-poodide hooldus"

**14. Possessive and pronoun overuse.** "sinu e-pood, sinu kliendid, sinu äri, sinu meeskond" in every line; "see", "seda" as English "this/it" at sentence starts. Drop the pronoun where the reader already knows the owner.

**15. Pleonasms.** "samuti ka", "kõige optimaalsem", "eelnevalt ette valmistama", "tagasi tagastama". [check_redundancy]

## C. Orthography the models get wrong

**16. Split compounds.** "hoolduse pakett", "veebi leht", "arendus töö", "äri eesmärk" should be one word: hoolduspakett, veebileht, arendustöö, ärieesmärk. Proper-noun attributes stay separate: "Shopify arendus". [check_compounds is lexicon-based and misses many; read every multi-noun phrase yourself]

**17. Abbreviation endings without a hyphen.** OÜle, APIga, ERPst, SLAd should be OÜ-le, API-ga, ERP-st, SLA-d (the ending follows how the abbreviation is pronounced). [check_abbreviation_hyphenation]

**18. Capitalisation.** Weekdays and months lowercase; "eesti keel", "eesti e-poed" lowercase as adjectives; "Eesti" capital only as the country. Title Case headings ("E-poe Arendus Ja Hooldus") should be sentence case. "Sina/Teie" not capitalised mid-sentence in marketing copy. [check_capitalization]

**19. Missing commas before subordinate clauses.** Comma before et, sest, kuna, kuigi, kui (as a clause), mis, kes, mille. The tool skips kui/mis/kes, so check those by reading. [check_punctuation]

**20. Number and time formats.** 3.5 should be 3,5; 1,200 should be 1 200; 9:00 should be 9.00 in running text; € after the number with a space (49 €) or the word "eurot". Values are protected; record notation-only changes in the ledger. [check_numbers]

**21. Wrong object case.** Partitive after negation and after partitive verbs (vajama, armastama, ootama...): "Me ei paku tasuta audit" should be "auditit". [check_object_case]

**22. Invented compounds and wrong inflections.** Models produce plausible but non-existent compounds and case forms. Every compound you coin and every inflected form you are unsure of goes through paradigm / analyze_morphology / check_compound_familiarity.

## D. Page and tone level

**23. Register mixing.** Ministry Estonian ("vastavalt", "käesolev", "kohaldama") next to slang or hype in the same page. [classify_register: consistency.is_mixed]

**24. Helpdesk or clinic framing in agency copy.** "Mis sul viga on?", "diagnoos", "ravime su e-poe terveks". Medical or support-desk metaphors are usually the wrong frame for B2B agency copy; follow the client profile.

**25. Vague CTAs.** A button that does not say what happens next: "Alusta", "Kliki siia", "Võta ühendust" on every button. Name the action and its result.

**26. Repetition across the page.** The same phrase in hero, section intro and CTA (the same question or slogan three times). Read the page as a visitor; each line must add something. [check_term_consistency, check_style repetition]

**27. Rhetorical-question headlines and exclamation marks.** "Kas sinu e-pood on aeglane?!" Fine once; a pattern across sections reads as AI or as a cheap ad.

**28. Bold labels, emojis, Title Case and decorative arrows** carried over from English AI drafts. Remove the decoration (see [blader/humanizer](https://github.com/blader/humanizer) for the English-language versions of these patterns).

## Dashes

Estonian uses the spaced en dash (mõttekriips, " – ") legitimately, and an unspaced en dash for ranges (9.00–17.00, 2024–2026). Do not strip them by rule. Flag only dashes that replace commas or colons throughout a text, and English-style em dashes (—) without spaces.
