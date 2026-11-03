# 00 – Project History & Lessons Learned

> Status: retrospective. Written in 2026 and reconstructed from what the founders remember.
> Fields marked `[TBD]` are for the founders to fill in. We did not make up any dates or names.

## Executive Summary

CubeIT was an open-hardware idea for Swiss primary and lower-secondary schools. Each part of a computer
(processor, power, display, USB, sound) sits in its own **magnetic cube**. Children snap the cubes
together and see, physically, how a computer is built. A **C.H.I.P.** board (USD 9, 2015) was the "brain".

We ordered the first boards and started on simple games. We stopped when we understood what it takes to
get a product into Swiss public schools. The problem was not the technology. It was the
**regulatory, procurement and curriculum route**, which a two-person, self-funded hobby team could not
pay for or staff.

This repository publishes the concept, the tools and a first micro learning game, free of charge. Others
can now use what we had to leave unfinished.

## Timeline (reconstruction)

| When | Milestone | Notes |
|---|---|---|
| 2014 | Idea: "a computer you can take apart with your hands" | Lehrplan 21 released to the cantons by D-EDK (Oct/Nov 2014) |
| May 2015 | Next Thing Co. starts the C.H.I.P. Kickstarter (USD 9 computer) | Fits our budget for a classroom set |
| 2015 `[TBD month]` | **First board order** placed | Delivery to backers in waves, late 2015 – 2016 |
| 2015 | Cube concept, magnetic face design, first PLA shells | See [02-hardware.md](02-hardware.md) |
| 2015/16 | First basic games on the board (Python/pygame) | Rebuilt here: [game/](../game/) |
| 2016 `[TBD]` | Looked into a route to "the Swiss state" | Found: education is cantonal, see [05](05-regulatory-roadmap.md) |
| 2016 `[TBD]` | **Project paused** | Compliance and market access too big for an early-stage team |
| 2018 | Next Thing Co. ceases operations | Our single supplier would have gone away anyway |
| 2026 | Open-sourced as documentation + free game | This repository |

## What worked

- **The teaching idea holds up.** Lehrplan 21 later made *Medien und Informatik*, including
  "Aufbau und Funktionsweise von Informatiksystemen" (MI.2.3), a compulsory module. CubeIT targets
  exactly that competence.
- **Low hardware cost.** A complete demo set at hobby prices came to about CHF 60–90 (see the
  [BOM](../hardware/bom-prototype-2015.csv)).
- **Software stack.** Debian + Python + pygame on C.H.I.P. was enough for real learning games.

## What stopped us (root causes, by impact)

1. **Wrong addressee.** We wanted to go to "the federal state". Under **Art. 62 BV**, compulsory
   school is a **cantonal** matter. There is no single federal buyer. There are 26 cantons, 3 curricula
   (Lehrplan 21, PER, Piano di studio TI) and thousands of school authorities.
2. **Compliance costs before the first sale.** Toy/product safety, EMC, radio (WiFi/BT), battery
   transport, take-back schemes and product liability come to an estimated CHF 30–80k, plus 6–12 months.
   See [05](05-regulatory-roadmap.md).
3. **Teaching evidence required.** Before teaching material is recommended, cantons want pilots that a
   university of teacher education (PH) has evaluated, and teacher training. That takes 2–4 years.
4. **Single-source hardware.** All our cubes depended on one start-up (Next Thing Co.). That supplier
   risk would never have passed a public tender.
5. **Physics versus vision.** "Every face connects to anything" does not work for HDMI or USB 2.0
   high-speed signals over cheap magnetic pogo pins. We needed a mixed design: universal faces plus
   keyed faces. See [02](02-hardware.md).

## Lessons for anyone restarting this

- Start **bottom-up**: one teacher, one school, one canton. Do not start with "the Confederation".
- Partner with a **PH** (teacher-education university) from day one. They provide the evaluation, the
  credibility and access to the cantonal teaching-material bodies.
- Sell to schools as **teaching equipment used under supervision**, not as a toy. Get this
  classification checked early; it decides the whole compliance path.
- Design for **two suppliers** per critical part. Today: Raspberry Pi Zero 2 W, Orange Pi, ESP32.
- Publish open source early. Free material can be used in class without a tender.
