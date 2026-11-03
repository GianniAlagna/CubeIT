# 05 – Regulatory & Bureaucratic Roadmap (Switzerland, as of 2015)

> **Not legal advice.** This is a structured retrospective for planning. Thresholds, versions and
> responsible authorities change. Check the current version of every decree (fedlex.admin.ch) and the
> cantonal law before acting. References use the SR numbers of the classified compilation of federal law.

## Executive Summary

To bring CubeIT into Swiss public schools, we would have had to meet requirements on **five fronts at
once**: (A) education federalism, (B) teaching-material approval, (C) product conformity, (D) public
procurement, (E) company, liability and data protection.

**Estimate before the first school sale: CHF 30–80k in external costs, 2–4 years, at least 1 FTE.**
A self-funded hobby team cannot carry that. The decision to stop was rational.

The way to start again is **open source plus a PH partnership plus "teaching equipment" classification
plus one pilot canton**. That avoids about 70 % of the effort at first.

---

## A. Education federalism: who is the customer?

| Fact | Basis | Consequence for CubeIT |
|---|---|---|
| Compulsory school is a matter for the cantons | **Art. 62 para. 1 BV** (SR 101) | The "federal Swiss state" does **not** buy teaching material for compulsory school |
| Harmonisation through an intercantonal agreement | **HarmoS-Konkordat** (2007, in force since 1.8.2009), Art. 62 para. 4 BV | Shared goals, but no shared procurement |
| Coordination | **EDK** (national), regional: D-EDK, CIIP, Ticino | 3 curriculum regions = 3 language versions plus 3 evaluations |
| Curricula | **Lehrplan 21** (D-EDK released it in 2014, cantonal introduction 2015–2019+), **PER**, **Piano di studio TI** (2015) | Proof of fit needed for each region (see [04](04-lehrplan21-mapping.md)) |
| Federal level | SBFI: vocational training, universities, research; **educa.ch**: ICT expertise, no purchasing | Useful for networking and research funding, **not as a customer** |

**Assessment:** the biggest strategic mistake was the addressee. The right entry point would have been
1 school → 1 municipality → 1 cantonal teaching-material commission.

## B. Teaching-material approval

| Step | Who | Effort |
|---|---|---|
| Write didactic concept + teacher's guide | Project + PH | 3–6 months |
| Pilot classes with evaluation | **PH** (e.g. PH Zürich, PH FHNW, PH Schwyz, HEP Vaud, SUPSI-DFA) | 1–2 school years |
| Assessment by the cantonal **teaching-material commission** (status: compulsory / alternatively compulsory / recommended / permitted) | Canton (Bildungsdirektion / Volksschulamt) | 6–18 months, cycle-dependent |
| Publishing / distribution | Usually via **teaching-material publishers** (Lehrmittelverlag Zürich, Schulverlag plus, ilz – Interkantonale Lehrmittelzentrale) | Licence/royalty model, publisher's quality requirements |
| Teacher training | PH continuing-education programme | Course concept, trainers, 1–2 years lead time |

**Shortcut:** teachers may use **free supplementary material** within their teaching freedom, without
formal approval. That is the route for this repository.

## C. Product conformity: the most expensive block

### C.1 Classification (it decides everything)

| Question | Option 1: **toy** | Option 2: **teaching equipment / IT device** |
|---|---|---|
| Basis | Toy Ordinance **VSS** (SR 817.023.11, under the Foodstuffs Act), aligned with EU 2009/48/EC | Product Safety Act **PrSG** (SR 930.11) + PrSV (SR 930.111), plus the electrical decrees |
| Typical standards | **EN 71-1/-2/-3** (mechanics, flammability, migration), **EN 62115** (electric toys) | EN 60950-1 / EN 62368-1 (IT equipment), EMC standards |
| Note | Directive 2009/48/EC, Annex I, excludes *products intended for educational use in schools under the supervision of an adult instructor* | Applies only if marketing, packaging and sales channel consistently target **schools**. Sales to families turn it into a toy |
| Enforcement | Cantonal food inspectorate / BLV | Depends on the product: ESTI, BAKOM, SECO |

**Recommendation (2015 and today):** position the product as teaching equipment, but **design to
EN 71-1 anyway** (enclosed magnets, small parts, edges). Children are the users in both cases.

### C.2 Electrical, radio, chemical and environmental requirements

| Topic | Swiss law (2015) | EU equivalent | Relevance for CubeIT | Cost estimate |
|---|---|---|---|---|
| Electromagnetic compatibility | **VEMV** (SR 734.5) | 2004/108/EC → 2014/30/EU | Each cube combination is a system; test a representative worst-case configuration | CHF 5–15k per test campaign |
| Radio (WiFi/BT on C.H.I.P.) | **FAV** (SR 784.101.2), BAKOM | R&TTE 1999/5/EC → RED 2014/53/EU (from 13.6.2016) | Integration of a radio module: conformity of the **end product** needs checking; module certification does not carry over automatically | CHF 3–10k (or use a version without radio) |
| Low voltage | **NEV** (SR 734.26), ESTI | 2014/35/EU | Only the 230 V power supply → buy a certified one, document it | low |
| Hazardous substances (RoHS) | **ChemRRV** (SR 814.81), Annex 2.18 | 2011/65/EU | Supplier declarations for every part, including C.H.I.P. | admin effort |
| Batteries | ChemRRV Annex 2.15, **advance disposal fee (VEG)** via INOBAT | 2006/66/EC | Register LiPo, pay the fee | low |
| LiPo transport | ADR / IATA, **UN 38.3** test report | – | Shipping by post or courier only with a test report | CHF 5–10k if the cell has none |
| Electronic waste | **VREG** (SR 814.620) | WEEE 2012/19/EU | Join **SENS / SWICO**, advance recycling fee | membership + fee |
| Product liability | **PrHG** (SR 221.112.944) | 85/374/EEC | Fault-independent liability as manufacturer/importer → **product liability insurance** | CHF 1–3k/year |
| Technical documentation | PrSG Art. 5, conformity assessment | CE / declaration of conformity | Risk analysis, test reports, instructions in **DE/FR/IT** | 1–2 months of work |

### C.3 The magnet trap

EN 71-1 restricts **small magnets with a flux index above 50 kG²mm²** that can come loose. Strong
neodymium magnets almost always exceed this. Children who swallow several magnets face life-threatening
bowel injuries. **The design must never let a magnet come loose**, which needs tension, torque, drop and
soak tests. That was a central, expensive test point for CubeIT.

## D. Public procurement

| Aspect | Basis (2015) | Consequence |
|---|---|---|
| Schools/municipalities as public buyers | **IVöB** (1994/2001) + cantonal procurement law; federal: BöB (SR 172.056.1) | Above the thresholds, a tender is mandatory |
| Thresholds (supplies, non-treaty area, IVöB 2001 Annex 2) | Single-source award below about CHF 100k, invitation procedure below about CHF 250k, open above that | A cantonal roll-out goes beyond single-source award → open procedure with suitability criteria (references, financial capacity, delivery capability) |
| Treaty area | WTO GPA, cantons: about CHF 350k for supplies | International competition |
| Suitability criteria | Commercial register entry, social insurance, references, often **ISO 9001** | A start-up without references is rarely suitable |

**Assessment:** below the thresholds, individual schools can buy single-source. That is realistic for
pilots, not for a roll-out.

## E. Company, taxes, data protection

| Topic | Basis | Requirement |
|---|---|---|
| Legal form | **GmbH** Art. 772 ff. OR (share capital CHF 20,000) or AG (CHF 100,000) | Limit liability before the first sale |
| VAT | **Art. 10 MWSTG**: liable from CHF 100,000 turnover per year | Below that, voluntary registration is possible (input tax on prototypes) |
| Data protection (2015) | **DSG 1992** (SR 235.1) for private companies; schools are subject to **cantonal** data protection law (e.g. IDG ZH) | Offline game without personal data → no processing of personal data → best solution. Today: **revDSG** since 1.9.2023 |
| Intellectual property | Trademark "CubeIT" (IGE), designs | Check before investing in a brand |

---

## Feasibility gate: early stage vs. requirement

| Requirement | Needed | Available in 2015 | Gap |
|---|---|---|---|
| Legal entity + insurance | GmbH, product liability | Private individuals | 🔴 |
| Conformity (EMC, toy/IT, radio, battery) | CHF 30–80k, accredited lab | Hobby budget | 🔴 |
| Teaching evidence | PH-evaluated pilot | Prototype, games | 🔴 |
| Teaching material in 3 languages | DE/FR/IT + teacher's guide | DE drafts | 🟠 |
| Series production + 2nd source | Injection mould CHF 15–40k, alternative SoC | 3D printing, single source | 🔴 |
| Procurement suitability | References, financial capacity | none | 🔴 |
| Technology | Working prototype | Available (with corrections, see [02](02-hardware.md)) | 🟢 |

**Result:** 1 of 7 criteria met. Stopping was the right call.

---

## Restart path (prioritised by impact, as of 2026)

| # | Action | Effect | Effort |
|---|---|---|---|
| 1 | **Open source** (this repo): game, tools, 3D files, lesson plans, free | Teachers can use it without approval or a tender | low |
| 2 | Use **pre-certified hardware** (e.g. Raspberry Pi Zero 2 W with its own CE/RED) plus passive cubes | Smaller EMC/radio scope | medium |
| 3 | **PH partnership** for a pilot (1 canton, 3–5 classes, 1 school year) | Evidence base, access to teaching-material commissions | medium |
| 4 | Positioning: **teaching equipment under supervision**, sold B2B to schools only | Toy route possibly not applicable (get this checked!) | low |
| 5 | Funding: Innosuisse (before 2018: **KTI**), **Hasler Stiftung** (ICT education), Gebert Rüf Stiftung, cantonal innovation funding | Pays for the compliance block | medium |
| 6 | Licensing to a **teaching-material publisher** instead of distributing ourselves | Publisher brings procurement suitability and distribution | medium |

## Next steps (concrete)

1. Assign a licence for the repo and publish it (MIT/CC BY-SA, done).
2. Find 1 teacher (Zyklus 2) to test it with a class. Use the game as a door-opener.
3. Request a meeting with the *Medien und Informatik* department of one PH.
4. Get the classification "toy vs. teaching equipment" checked in writing by a test lab or conformity
   specialist (CHF 500–1,500).
5. Only after that, decide on hardware for a small series.
