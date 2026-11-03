#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cubetool - identify CubeIT cubes on the CubeBus (I2C).

Every CubeIT cube carries a 24C02 EEPROM (256 bytes, I2C). The first 32 bytes
hold an ID record so the Brain cube (C.H.I.P.) knows which cubes are attached.
Address pins A0-A2 on each cube give 8 slots: 0x50-0x57.

Written for the 2015 stack: Debian Jessie on C.H.I.P., Python 2.7, python-smbus.
Also runs on Python 3. The 'gen', 'parse' and 'scan --simulate' commands need
no hardware at all, so the tool can be used in class on any laptop.

Usage:
  cubetool.py types
  cubetool.py gen   --type display --serial 42 [--rev 1.0] -o display.bin
  cubetool.py parse display.bin
  cubetool.py scan  [--bus 2] [--simulate]
  cubetool.py write display.bin --addr 0x51 [--bus 2]

ID record layout (32 bytes, little endian):
  0-3   magic "CUBE"
  4     format version (1)
  5     cube type id (see 'types')
  6-7   hardware revision major, minor
  8-11  serial number (uint32)
  12-27 name, ASCII, NUL padded (16 bytes)
  28-29 max current draw in mA (uint16)
  30    flags  bit0 = has keyed high-speed face, bit1 = has battery
  31    checksum: sum of bytes 0-31 == 0 (mod 256)

License: MIT
"""
from __future__ import print_function

import argparse
import struct
import sys
import time

MAGIC = b"CUBE"
FORMAT = 1
RECORD_LEN = 32
EEPROM_ADDRS = list(range(0x50, 0x58))
DEFAULT_BUS = 2      # C.H.I.P.: TWI2 on header U13 pins 9/11 = /dev/i2c-2

# type id: (key, human name, default mA, flags)
TYPES = {
    0x01: ("brain", "Brain C.H.I.P.", 600, 0x01),
    0x02: ("power", "Power 5V LiPo", 0, 0x02),
    0x03: ("display", "Display HDMI/DVI", 150, 0x01),
    0x04: ("usb", "USB Hub 4x", 100, 0x01),
    0x05: ("audio", "Audio Speaker", 120, 0x00),
    0x06: ("sensor", "Sensor Temp/Light", 10, 0x00),
    0x07: ("led", "LED Matrix 8x8", 200, 0x00),
    0x08: ("button", "Buttons 4x", 5, 0x00),
}
KEY_TO_ID = dict((v[0], k) for k, v in TYPES.items())


def checksum(data):
    return (256 - (sum(bytearray(data)) & 0xFF)) & 0xFF


def build_record(type_id, serial, rev=(1, 0), name=None, current=None, flags=None):
    key, human, ma, fl = TYPES[type_id]
    name = (name or human).encode("ascii", "replace")[:16]
    body = struct.pack(
        "<4sBBBBI16sHB",
        MAGIC, FORMAT, type_id, rev[0], rev[1], serial,
        name.ljust(16, b"\0"),
        ma if current is None else current,
        fl if flags is None else flags,
    )
    return body + bytearray([checksum(body)])


def parse_record(data):
    data = bytes(bytearray(data))
    if len(data) < RECORD_LEN:
        raise ValueError("record too short: %d bytes" % len(data))
    data = data[:RECORD_LEN]
    if data == b"\xff" * RECORD_LEN:
        raise ValueError("blank EEPROM (not programmed yet - use 'gen' + 'write')")
    if sum(bytearray(data)) & 0xFF != 0:
        raise ValueError("checksum error")
    magic, fmt, tid, rmaj, rmin, serial, name, ma, flags = struct.unpack("<4sBBBBI16sHB", data[:31])
    if magic != MAGIC:
        raise ValueError("no CubeIT magic (blank or foreign EEPROM)")
    if fmt != FORMAT:
        raise ValueError("unsupported format version %d" % fmt)
    return {
        "type_id": tid,
        "type": TYPES.get(tid, ("unknown",))[0],
        "rev": "%d.%d" % (rmaj, rmin),
        "serial": serial,
        "name": name.rstrip(b"\0").decode("ascii", "replace"),
        "max_mA": ma,
        "keyed_face": bool(flags & 0x01),
        "battery": bool(flags & 0x02),
    }


class SimBus(object):
    """Fake I2C bus with a typical classroom setup, for teaching without hardware."""

    def __init__(self):
        self.mem = {
            0x50: build_record(0x02, 1001),
            0x51: build_record(0x03, 2001),
            0x52: build_record(0x04, 3001),
            0x54: build_record(0x05, 4001),
            0x56: bytearray([0xFF] * RECORD_LEN),      # blank EEPROM, not programmed yet
        }

    def read_i2c_block_data(self, addr, offset, length):
        if addr not in self.mem:
            raise IOError(121, "Remote I/O error")
        return list(self.mem[addr][offset:offset + length])


def open_bus(bus, simulate):
    if simulate:
        return SimBus()
    try:
        import smbus
    except ImportError:
        sys.exit("python-smbus missing: sudo apt-get install python-smbus i2c-tools  (or use --simulate)")
    return smbus.SMBus(bus)


def read_record(dev, addr):
    out = bytearray()
    for off in range(0, RECORD_LEN, 16):            # SMBus block reads are limited to 32, use 16 for safety
        out += bytearray(dev.read_i2c_block_data(addr, off, 16))
    return out


def cmd_types(_args):
    print("ID    KEY       NAME                 mA   FLAGS")
    for tid in sorted(TYPES):
        key, human, ma, fl = TYPES[tid]
        print("0x%02X  %-8s  %-19s %4d   0x%02X" % (tid, key, human, ma, fl))
    return 0


def cmd_gen(args):
    tid = KEY_TO_ID.get(args.type)
    if tid is None:
        try:
            tid = int(args.type, 0)
        except ValueError:
            sys.exit("unknown type '%s' (see: cubetool.py types)" % args.type)
    if tid not in TYPES:
        sys.exit("unknown type id 0x%02X" % tid)
    rev = tuple(int(x) for x in args.rev.split("."))
    rec = build_record(tid, args.serial, rev, args.name)
    image = rec + bytearray([0xFF] * (256 - RECORD_LEN))   # full 24C02 image
    with open(args.output, "wb") as fh:
        fh.write(bytes(image))
    print("wrote %s (%d bytes) for %s #%d" % (args.output, len(image), TYPES[tid][0], args.serial))
    return 0


def print_record(addr, rec):
    face = "keyed" if rec["keyed_face"] else "universal"
    print("0x%02X  %-8s rev %-4s serial %-7d %-18s %4d mA  %s%s" % (
        addr, rec["type"], rec["rev"], rec["serial"], rec["name"], rec["max_mA"],
        face, ", battery" if rec["battery"] else ""))


def cmd_parse(args):
    with open(args.file, "rb") as fh:
        data = fh.read()
    try:
        print_record(0, parse_record(data))
    except ValueError as exc:
        print("invalid record: %s" % exc)
        return 1
    return 0


def cmd_scan(args):
    dev = open_bus(args.bus, args.simulate)
    found, budget = 0, TYPES[0x01][2]      # the Brain cube itself is the bus master
    print("Scanning CubeBus %s ..." % ("(simulated)" if args.simulate else "/dev/i2c-%d" % args.bus))
    for addr in EEPROM_ADDRS:
        try:
            raw = read_record(dev, addr)
        except (IOError, OSError):
            continue
        try:
            rec = parse_record(raw)
        except ValueError as exc:
            print("0x%02X  ?        %s" % (addr, exc))
            continue
        print_record(addr, rec)
        found += 1
        budget += rec["max_mA"]
    print("%d cube(s) identified, worst-case current %d mA incl. Brain" % (found, budget))
    if budget > 1800:
        print("WARNING: above 1.8 A budget of a single Power cube (5 V / 2 A, 10% reserve)")
    return 0 if found else 2


def cmd_write(args):
    with open(args.file, "rb") as fh:
        data = bytearray(fh.read())[:RECORD_LEN]
    parse_record(data)                      # refuse to write garbage
    dev = open_bus(args.bus, False)
    addr = int(args.addr, 0)
    for off in range(0, RECORD_LEN, 8):    # 24C02 page size: 8 bytes
        dev.write_i2c_block_data(addr, off, list(data[off:off + 8]))
        time.sleep(0.01)                    # t_WR max 5 ms, keep margin
    back = parse_record(read_record(dev, addr))
    print_record(addr, back)
    print("verified")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="CubeIT cube identification tool")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("types", help="list known cube types")
    g = sub.add_parser("gen", help="generate a 24C02 EEPROM image")
    g.add_argument("--type", required=True)
    g.add_argument("--serial", type=int, required=True)
    g.add_argument("--rev", default="1.0")
    g.add_argument("--name")
    g.add_argument("-o", "--output", required=True)
    pa = sub.add_parser("parse", help="decode an EEPROM image file")
    pa.add_argument("file")
    s = sub.add_parser("scan", help="list cubes attached to the Brain cube")
    s.add_argument("--bus", type=int, default=DEFAULT_BUS)
    s.add_argument("--simulate", action="store_true")
    w = sub.add_parser("write", help="program a cube EEPROM (hardware only)")
    w.add_argument("file")
    w.add_argument("--addr", required=True)
    w.add_argument("--bus", type=int, default=DEFAULT_BUS)
    args = p.parse_args(argv)
    handlers = {"types": cmd_types, "gen": cmd_gen, "parse": cmd_parse, "scan": cmd_scan, "write": cmd_write}
    if args.cmd not in handlers:
        p.print_help()
        return 1
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
