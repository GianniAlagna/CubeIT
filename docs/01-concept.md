# 01 – Concept: A Computer You Can Hold in Your Hands

## Executive Summary

A computer is a black box to children. CubeIT breaks it into **cubes about 50 mm across**, one cube per
function, held together by **magnets**. When the right cubes touch, the computer boots. Children learn
the IPO model (EVA in German: Eingabe – Verarbeitung – Ausgabe) by doing it, then move on to
programming on the computer they built themselves.

## Target group

| Cycle (Lehrplan 21) | Age | CubeIT use |
|---|---|---|
| Zyklus 1 (KG – Kl. 2) | 4–8 | Snap and name the cubes, colour/shape matching, unplugged games |
| **Zyklus 2 (Kl. 3–6)** | 8–12 | **Primary target**: build the computer, boot it, first programs |
| Zyklus 3 (Kl. 7–9) | 12–15 | Program sensors/LEDs (Python), read the CubeBus, build their own cubes |

## Cube catalogue

| Cube | Colour | Function | Lesson |
|---|---|---|---|
| **Brain** | blue | C.H.I.P.: CPU 1 GHz, 512 MB RAM, 4 GB storage, WiFi/BT | Processing (Verarbeitung) |
| **Power** | yellow | 5 V / 2 A, LiPo battery or mains adapter | No power, no computer |
| **Display** | magenta | HDMI (passive DVI adapter) / VGA | Output (Ausgabe) |
| **USB** | green | 4-port USB hub for keyboard and mouse | Input (Eingabe) |
| **Audio** | orange | Speaker + amplifier | Output (sound) |
| Sensor | white | Temperature / light (I2C) | Data from the environment (MI.2.1) |
| LED matrix | red | 8×8 LEDs | Binary, pixels, images |
| Buttons | grey | 4 buttons | Events, game controller |

Every cube shows its **colour and a text label** (CHIP, 5V, HDMI …), so colour-blind children can tell
them apart too.

## The core rule: "Magnets must touch"

- Cubes connect through any face of a cube that is already connected (above, below, left, right, front,
  back).
- The Brain cube finds connected cubes through an ID chip in each cube (see [02](02-hardware.md),
  [cubetool](../tools/cubetool.py)).
- A cube that touches nothing stays dark. Children see right away that a connection is missing.

## Lesson sequence (one double lesson = 90 min)

1. **Unpack (10 min)**: What is inside a computer? Children guess, then open the transparent Brain cube.
2. **Play first (15 min)**: Mission 1 of the [micro learning game](../game/) on a ready-made set.
3. **Build it for real (30 min)**: Groups of 3 build their own computer from cubes. *Power on.*
   If it doesn't work: debug (which cube is missing?).
4. **Program (25 min)**: Missions 2 and 3 on the computer they built themselves.
5. **Reflect (10 min)**: Draw the EVA diagram on paper: which cube is input, processing, output?

## Design principles

- **Touch before screen.** Physical understanding first, abstraction afterwards.
- **Micro learning.** Units of at most 5 minutes, immediate feedback, stars instead of grades.
- **Offline first.** No cloud, no account, no personal data. That removes school data-protection
  questions.
- **Multilingual.** DE / FR / IT / EN from the start (Switzerland has 3 curriculum regions).
- **Open source.** Schools may copy, adapt and print. Free material needs no procurement process.
