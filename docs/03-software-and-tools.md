# 03 – Software Stack & Tools (2015 Level)

## Executive Summary

Everything here runs on what was available in 2015: **Debian Jessie on C.H.I.P., Python 2.7, pygame
1.9.2, sysfs GPIO, python-smbus**. No cloud and no build server. One shell script turns a fresh
C.H.I.P. into a classroom computer.

## Stack

| Layer | 2015 choice | Why |
|---|---|---|
| OS | CHIP OS (Debian Jessie, Xfce) | Ready-made image, apt available, flashing via the CHIP Flasher (Chrome app) |
| Language | Python 2.7 (+ Python 3.4 available) | Readable for teachers, in the Jessie repository |
| Games | pygame 1.9.2 (`python-pygame`) | 2D games, no GPU acceleration needed |
| Block programming | Scratch 1.4 (`scratch` package) | Zyklus 2, no Flash plugin needed |
| Editor | Geany | Light, runs on 512 MB RAM |
| Hardware access | sysfs GPIO, `/dev/i2c-*`, python-smbus | No root daemons; i2c/gpio groups |

## Tools in this repository

| Tool | Purpose | Needs hardware? |
|---|---|---|
| [`tools/chip-setup.sh`](../tools/chip-setup.sh) | Prepare a C.H.I.P. for class: packages, pupil account, game autostart, SSH lock for pupils | yes (C.H.I.P.) |
| [`tools/cubetool.py`](../tools/cubetool.py) | Generate, decode, scan and program cube ID EEPROMs; check the power budget | `gen`/`parse`/`scan --simulate`: no |
| [`tools/xio-test.sh`](../tools/xio-test.sh) | Blink an LED on XIO-P0…P7; finds the GPIO base number on its own (kernel 4.3: 408, 4.4.13: 1013) | yes |
| [`game/cubeit_game.py`](../game/cubeit_game.py) | Micro learning game, 3 missions, DE/FR/IT/EN | no |

### Quick start: classroom computer

```bash
git clone https://github.com/GianniAlagna/CubeIT.git && cd CubeIT
```

```bash
sudo ./tools/chip-setup.sh --hostname cubeit-01
```

### Cubes: produce and check ID records

```bash
python tools/cubetool.py gen --type display --serial 2001 -o display.bin
```

```bash
sudo python tools/cubetool.py write display.bin --addr 0x51
```

```bash
python tools/cubetool.py scan            # real CubeBus on /dev/i2c-2
```

```bash
python tools/cubetool.py scan --simulate # in class without hardware
```

## Lab workflow 2015 (what we really had)

- **Version control:** Git + GitHub (free for open source)
- **Flashing:** CHIP Flasher in Chrome, or `CHIP-tools` (`chip-update-firmware.sh`) on Ubuntu
- **Serial console:** USB-UART adapter (FTDI) on U14 UART1, `screen /dev/ttyUSB0 115200`
- **3D printing:** OpenSCAD → Cura → Prusa i3 (PLA)
- **Electronics:** KiCad 4 (2015), test circuits on breadboards
- **Testing:** headless game tests with `SDL_VIDEODRIVER=dummy` (see [`tests/`](../tests))

## Operations and security in the classroom

- Pupil account without sudo; the game and tools are in `/opt`, `/usr/local/bin`.
- No pupil SSH login (`DenyUsers`), password changed for each class.
- The game stores only stars and the language in `~/.cubeit_progress.json`. No names, no network
  traffic.
- Updates: `git pull && sudo ./tools/chip-setup.sh` by the teacher. A full set of 10 units takes about
  30 minutes.
