#!/bin/bash
# chip-setup.sh - prepare a C.H.I.P. (Debian Jessie / CHIP OS) as CubeIT classroom computer.
#
# What it does (idempotent, safe to re-run):
#   1. installs the 2015 learning stack: python + pygame, i2c tools, Scratch 1.4, geany
#   2. creates a pupil account without sudo rights ("schueler")
#   3. copies the CubeIT game to /opt/cubeit and adds a desktop + autostart entry
#   4. disables what a school network does not want: no SSH password login for pupils
#
# Usage: sudo ./chip-setup.sh [--no-autostart] [--hostname cubeit-01]
# License: MIT
set -euo pipefail

AUTOSTART=1
NEWHOST=""
while [ $# -gt 0 ]; do
    case "$1" in
        --no-autostart) AUTOSTART=0 ;;
        --hostname) NEWHOST="$2"; shift ;;
        *) echo "unknown option $1" >&2; exit 1 ;;
    esac
    shift
done

if [ "$(id -u)" -ne 0 ]; then
    echo "run as root: sudo $0" >&2
    exit 1
fi

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PUPIL="schueler"

echo "== 1/4 packages"
apt-get update
apt-get install -y python python-pygame python-smbus i2c-tools geany git
# Scratch 1.4 (squeak based) is in Debian Jessie; not critical if missing on a mirror
apt-get install -y scratch || echo "   scratch not available on this mirror - skipped"

echo "== 2/4 pupil account"
if ! id "$PUPIL" >/dev/null 2>&1; then
    adduser --disabled-password --gecos "CubeIT Schueler" "$PUPIL"
    echo "$PUPIL:cubeit" | chpasswd
    echo "   default password 'cubeit' - change it per class"
fi
usermod -aG i2c,gpio,audio,video "$PUPIL" 2>/dev/null || usermod -aG audio,video "$PUPIL"

echo "== 3/4 install game"
install -d /opt/cubeit
install -m 0755 "$REPO_DIR/game/cubeit_game.py" /opt/cubeit/cubeit_game.py
install -m 0755 "$REPO_DIR/tools/cubetool.py" /usr/local/bin/cubetool
install -m 0755 "$REPO_DIR/tools/xio-test.sh" /usr/local/bin/xio-test

DESKTOP=/usr/share/applications/cubeit.desktop
cat > "$DESKTOP" <<'EOF'
[Desktop Entry]
Type=Application
Name=CubeIT
Comment=Bau deinen Computer - Micro Learning
Exec=python /opt/cubeit/cubeit_game.py --fullscreen
Terminal=false
Categories=Education;Game;
EOF

AUTO_DIR="/home/$PUPIL/.config/autostart"
if [ "$AUTOSTART" -eq 1 ]; then
    install -d -o "$PUPIL" -g "$PUPIL" "$AUTO_DIR"
    install -m 0644 -o "$PUPIL" -g "$PUPIL" "$DESKTOP" "$AUTO_DIR/cubeit.desktop"
else
    rm -f "$AUTO_DIR/cubeit.desktop"
fi

echo "== 4/4 hardening"
if [ -f /etc/ssh/sshd_config ] && ! grep -q "^DenyUsers $PUPIL" /etc/ssh/sshd_config; then
    echo "DenyUsers $PUPIL" >> /etc/ssh/sshd_config
    service ssh reload || true
fi
if [ -n "$NEWHOST" ]; then
    echo "$NEWHOST" > /etc/hostname
    sed -i "s/127.0.1.1.*/127.0.1.1\t$NEWHOST/" /etc/hosts
    hostname "$NEWHOST"
fi

echo "done. Reboot, log in as '$PUPIL', CubeIT starts automatically."
