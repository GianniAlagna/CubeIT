# 02 – Hardware Architecture (2015 Prototype Level)

## Executive Summary

- **Brain:** C.H.I.P. (Next Thing Co., 2015) in a 50 mm cube.
- **CubeBus:** each cube face carries an 8-pin magnetic pogo connector with **5 V, GND and I2C**. The pin
  layout is mirror-symmetric, so a face fits in any of its 180° orientations.
- **High-speed signals (HDMI, USB)** do **not** run over universal faces. They use **keyed faces**,
  which exist only on the Brain cube. This was the most important technical correction to the original
  vision.

## C.H.I.P. – key data (as of 2015/16)

| Feature | Value |
|---|---|
| SoC | Allwinner R8, ARM Cortex-A8, 1 GHz, Mali-400 GPU |
| RAM / storage | 512 MB DDR3 / 4 GB NAND (8 GB on later revisions) |
| Wireless | WiFi 802.11 b/g/n, Bluetooth 4.0 |
| Ports | 1× USB-A host, 1× micro-USB (power + OTG), 3.5 mm TRRS (composite video + audio) |
| Power | 5 V via micro-USB or CHN pin, AXP209 PMIC, JST connector for a 3.7 V LiPo |
| GPIO | 2×40 header (U13, U14): TWI/I2C, SPI, UART, LCD pins; 8× XIO via PCF8574A (I2C) |
| Extensions | "DIP" add-on boards (HDMI DIP, VGA DIP), identified by a 1-Wire EEPROM |
| OS | Debian Jessie based (CHIP OS / Buildroot), kernel 4.3 / 4.4 |
| Price | USD 9 (Kickstarter), HDMI DIP about USD 15 |

> **Supplier risk:** Next Thing Co. ceased operations in 2018. Equivalent options today: Raspberry Pi
> Zero 2 W (HDMI on board), Orange Pi Zero, Radxa Zero.

> **Video in Switzerland in 2015:** composite output on C.H.I.P. can be set to PAL. Old school projectors
> with a cinch (RCA) input could be used without a DIP board.

## System view

```
                 ┌───────────┐
                 │  AUDIO    │   universal face (CubeBus: 5V/GND/I2C)
                 └─────┬─────┘
┌───────────┐    ┌─────┴─────┐    ┌───────────┐
│  POWER    ├────┤   BRAIN   ╞════╡  DISPLAY  ├── HDMI/DVI ──> monitor
│ 5V LiPo   │    │  C.H.I.P. │    │  HDMI DIP │
└───────────┘    └─────╥─────┘    └───────────┘
                 ┌─────╨─────┐
                 │   USB     ├── keyboard / mouse
                 │  hub 4x   │
                 └───────────┘
   ────  universal face (any orientation)
   ════  keyed face (video: LCD/HDMI DIP signals)
   ║     keyed face (USB 2.0 + power)
```

## CubeBus – universal face (8-pin magnetic pogo, 2.5 mm pitch)

Two identical faces meet as **mirror images**: pin *i* meets pin *9 − i*. So that every signal lands on
itself, the layout is **palindromic**:

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Signal | GND | 5V | SDA | SCL | SCL | SDA | 5V | GND |

- 2 pins each for 5 V and GND → about 2 × 1.5 A capacity, with reserve for 2 A.
- I2C at 100 kHz (standard mode). Bus capacitance up to about 6 cubes is OK; beyond that, an I2C buffer
  (e.g. P82B715) is needed in the Power cube.
- **Magnet polarity:** 2 neodymium discs per face (N on the left, S on the right). Wrong orientations
  repel each other, which gives a natural mechanical key.
- Each cube carries a **24C02 EEPROM** (address 0x50–0x57, set with A0–A2). The record format is in
  [`tools/cubetool.py`](../tools/cubetool.py).

## Keyed faces (Brain cube only)

| Face | Signals | Why not universal |
|---|---|---|
| VIDEO | LCD-RGB / HDMI DIP header, 5 V, GND | Parallel RGB with 20+ lines, or TMDS at hundreds of MHz: impossible over cascaded pogo pins |
| USB | USB 2.0 D+/D−, 5 V, GND (4-pin magnetic, keyed) | 480 Mbit/s needs a 90 Ω differential impedance; one hop only |

Teaching statement: *"Fast data needs special connections. That is why your PC has different
sockets."* A good discussion question for Zyklus 3.

## Power budget

| Consumer | Worst case |
|---|---|
| Brain (C.H.I.P. with WiFi) | 600 mA |
| Display (HDMI DIP) | 150 mA |
| USB hub + keyboard + mouse | 100 mA + 2×100 mA |
| Audio (PAM8403, 2×3 W, limited to 0.5 W) | 120 mA |
| **Total** | **about 1.2 A** at 5 V → a 5 V / 2 A power cube is enough |

`cubetool.py scan` adds up the current from the ID records and warns above 1.8 A.

## Mechanics & child safety (designed in from the start)

- Shell: 50 × 50 × 50 mm, PLA/ABS 3D print (prototype) → injection-moulded ABS (series). Edges rounded
  to R ≥ 2 mm.
- **Magnets fully enclosed**: pressed into a pocket, glued, and covered by the face plate. EN 71-1
  restricts loose small magnets with a flux index above 50 kG²mm². A magnet must never be able to come out.
- LiPo only in the Power cube, with a protection circuit (PCM), a fuse and a screwed-shut housing.
  Children never touch cells.
- Only safety extra-low voltage (5 V) on the cube surfaces. The mains adapter is a certified off-the-shelf
  part.

## Prototype bill of materials

See [`hardware/bom-prototype-2015.csv`](../hardware/bom-prototype-2015.csv). These are indicative
hobby-scale prices (single units, AliExpress/Digikey, 2015).
