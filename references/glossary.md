# Glossary: Estonian e-commerce and web-agency terms

One concept, one term, on every page. Use the "Use" column. Words in "Avoid" are either anglicisms, calques, stiff officialese, or simply a second term for the same thing (which breaks consistency). This is a general default for e-commerce and web-agency copy. A client profile's glossary overrides it; when a site already uses a different but correct term consistently, flag it instead of changing it page by page.

The machine-readable term list for estonian-mcp is `glossary-ecommerce.txt` (pass it to the server as `ESTNLTK_MCP_DOMAIN_GLOSSARY`, or to `scripts/et_check.py --glossary`). Keep both files in sync, and add client terms to a copy of it.

## Core terms

| Concept (EN) | Use | Avoid | Notes |
|---|---|---|---|
| online store, webshop | **e-pood** (e-poe, e-poodi, e-poes, e-poed) | online-pood, eshop, e-kauplus, internetipood, veebipood (as a second term) | The default noun for an online shop. |
| website | **veebileht** | veebisait, website, koduleht (in agency copy) | A single page of a site: **leht** / **alamleht**. |
| development | **arendus**, **arendustöö** | development, väljatöötamine, arendamise läbiviimine | Platform name + arendus is two words: "Shopify arendus". "e-poe arendus". |
| maintenance | **hooldus**; **hoolduspakett**, **hooldusleping** | maintenance, ülalpidamine, haldus (different meaning) | "haldus" = content/admin work, not technical maintenance. Do not mix them. |
| upgrade (version) | **versiooniuuendus** (platvormi versiooniuuendus) | upgrade, apgreid, uuendamise teostamine | For the act: "uuendame platvormi uuemale versioonile". |
| security patch/update | **turvauuendus**; **turvaparandus** for a single fix | security patch, patch'imine, pätš | "turvapaik" exists and passes spell-check, but pick one term per site. |
| integration | **liidestus**; process **liidestamine** | connector, integreerimine (as a second term), "ühendus" for system integration | "liidestus ERP-ga", "liidestame e-poe laoprogrammiga". Vabamorf does not know "liidestus" as a noun (see verification.md); the glossary is authoritative. If an existing page title uses "integratsioon" for SEO, flag it as a business decision. |
| checkout (process) | **ostu vormistamine**; **tellimuse vormistamine** | checkout, check-out, kassaprotsess | Button: "Vormista tellimus". "Kassasse" is acceptable as a shop-UI button only if the shop uses it consistently. |
| cart | **ostukorv** | korv (alone), shopping cart | |
| order | **tellimus** | order, ost (when meaning the order record) | |
| payment method / shipping method | **makseviis** / **tarneviis** | maksemeetod, saatmismeetod, shipping | |
| stock level | **laoseis** | stock, laovaru (as a second term) | |
| product catalogue | **tootekataloog** | product catalog, kataloog (alone, when the product catalogue is meant) | |
| module / extension | **moodul**; **moodularendus** | plugin (unless the source means a WordPress plugin), laiendus (as a second term), extension | |
| automation | **automatiseerimine**; verb "automatiseerime" | automatsioon, automation | Prefer the verb in selling copy. |
| digital worker | **digitöötaja** | digital worker, AI-agent (as the service name) | Confirm against the site's current service name; if the site uses another term, flag it. |
| quote / estimate | **hinnapakkumine** | kvoot, quote | Price enquiry: **hinnapäring**. |
| scope (of work) | **töö maht**, **töö ulatus** | skoop, scope | |
| introductory call | **tutvumisvestlus**; "tasuta N-minutiline vestlus" | audit, konsultatsioon (implies paid advice), demo | Name the step the visitor actually books. If the free call is not an audit, do not call it one. |
| business goal | **ärieesmärk** (one word) | äri eesmärk, ärilised eesmärgid (stiff) | Plain alternative: "mida sa e-poega saavutada tahad". |
| web development | **veebiarendus** | webiarendus, web development | |
| server management / hosting | **serverihaldus**, **majutus** | hosting (as a second term), serveri haldamine teostatakse | |
| speed optimisation | **kiiruse parandamine**, "teeme e-poe kiiremaks" | kiirusoptimeerimine (as a headline buzzword), optimeerimine | "optimeerimine" only when a concrete measure follows. |
| SLA | **teenustaseme leping (SLA)** at first mention, then **SLA** | service level agreement | Wording of an existing SLA is protected; do not rename the contract or its credits without a business decision. |
| VAT | **käibemaks**; "hinnad ei sisalda käibemaksu" / "hind sisaldab käibemaksu" | VAT, KM (in prose) | Tax treatment is a protected fact. |

## Address and pronouns

| Use | Avoid | Notes |
|---|---|---|
| sina, sinu, su; imperative 2nd sg ("Broneeri", "Kirjuta") | Teie/teie, Sina (capitalised mid-sentence), mixed sina/teie | One address form across the whole site. |
| meie, me; "Teeme", "Vaatame üle" | meie poolt, "teostatakse", "pakutakse" when the actor is the agency | Name the actor. |

## Words to cut or replace on sight

| Avoid | Problem | Try instead |
|---|---|---|
| visioon, innovaatilised lahendused, terviklahendus | Generic, says nothing | Name the deliverable: "liidestame", "uuendame", "hooldame" |
| optimeerimine (as a benefit) | Vague | The concrete change: "lehed laadivad kiiremini", "vähem käsitööd" |
| lahendus / lahendused (stacked) | Filler noun | The actual thing: moodul, liidestus, hoolduspakett |
| võimaldame, tagame | Consultant/legal tone; "tagame" can read as a guarantee | "saad", "teeme", or state the fact; never imply a guarantee the source does not give |
| viime uuele tasemele, tõstame järgmisele tasemele | Slogan calque | Say what changes |
| personaalne lähenemine, pikaajaline partnerlus, lisaväärtus | Brochure filler | The specific practice behind it, or cut |
| sujuv kogemus, sujuv ostuprotsess | Calque of "seamless" | "ostu vormistamine on lihtne ja kiire" only if the source supports it |
| omama ("omame kogemust") | Calque of "have" | "meil on kogemus" / "oleme teinud" |
| läbi viima, teostama | Support verbs, officialese | The real verb: analüüsima, uuendama, testima |
| jaoks (stacked) | Calque of "for" | Case endings or restructure: "e-poele", "sinu meeskonnale" |
| skoop, deliverable, lead, fiks, apgreid | Anglicisms | töö maht, tulemus, päring, parandus, versiooniuuendus |
