#!/bin/sh
# xio-test.sh - blink an LED on a C.H.I.P. XIO pin (sysfs GPIO, 2015 style).
#
# The 8 XIO pins of C.H.I.P. come from a PCF8574A I2C expander. Its GPIO base
# number changed between kernels (408 on 4.3, 1013 on 4.4.13), so we look it up
# instead of hard-coding it. Wire: XIO-Px -> 330 Ohm -> LED -> GND.
#
# Usage: sudo ./xio-test.sh [pin 0-7] [count]
# License: MIT
set -eu

PIN="${1:-0}"
COUNT="${2:-10}"

case "$PIN" in [0-7]) ;; *) echo "pin must be 0-7" >&2; exit 1 ;; esac

BASE=""
for chip in /sys/class/gpio/gpiochip*; do
    [ -r "$chip/label" ] || continue
    if grep -qi "pcf8574a" "$chip/label"; then
        BASE=$(cat "$chip/base")
    fi
done
if [ -z "$BASE" ]; then
    echo "No PCF8574A gpiochip found - is this a C.H.I.P.?" >&2
    exit 2
fi

GPIO=$((BASE + PIN))
G="/sys/class/gpio/gpio$GPIO"
echo "XIO-P$PIN = gpio$GPIO (base $BASE)"

[ -d "$G" ] || echo "$GPIO" > /sys/class/gpio/export
trap 'echo 0 > "$G/value" 2>/dev/null; echo "$GPIO" > /sys/class/gpio/unexport 2>/dev/null' EXIT INT TERM
echo out > "$G/direction"

i=0
while [ "$i" -lt "$COUNT" ]; do
    echo 1 > "$G/value"; sleep 1
    echo 0 > "$G/value"; sleep 1
    i=$((i + 1))
    echo "blink $i/$COUNT"
done
