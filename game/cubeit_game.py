#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CubeIT - Micro Learning Game "Bau deinen Computer"
==================================================

A free micro learning game for children (age 8-12) written the way we could
have written it in 2015 for the C.H.I.P. board (Allwinner R8, 512 MB RAM,
Debian Jessie, Python 2.7, pygame 1.9.2). It still runs on any modern
Python 3 + pygame 2 installation.

Three missions, each about 5 minutes:
  1. Bau den Computer  - which cubes does a computer need? (IPO / EVA model)
  2. Robo-Cube         - write a small program to steer a robot (algorithms)
  3. Binaer-Wuerfel     - represent numbers with on/off LEDs (data)

Controls: keyboard only (Pocket C.H.I.P. friendly) or mouse.
Languages: Deutsch (CH), Francais, Italiano, English.

License: MIT (see LICENSE in repository root).
"""
from __future__ import division, print_function, unicode_literals

import array
import io
import json
import math
import os
import random
import sys

try:
    import pygame
except ImportError:
    print("pygame fehlt / missing. Debian/C.H.I.P.: sudo apt-get install python-pygame")
    sys.exit(1)

VERSION = "0.1.0"
W, H = 640, 480                      # logical resolution (fits HDMI + PAL composite)
FPS = 30
SAVE_FILE = os.path.join(os.path.expanduser("~"), ".cubeit_progress.json")

# --------------------------------------------------------------------------
# Colours (high contrast, colour-blind friendly: every cube also has a label)
# --------------------------------------------------------------------------
BG = (24, 28, 40)
PANEL = (38, 44, 62)
PANEL_HI = (58, 66, 92)
WHITE = (240, 240, 240)
GREY = (130, 136, 150)
DARK = (14, 16, 22)
GREEN = (80, 200, 120)
RED = (230, 80, 80)
YELLOW = (250, 210, 70)
BLUE = (80, 150, 240)
CYAN = (80, 210, 220)
MAGENTA = (210, 110, 220)
ORANGE = (245, 150, 60)

# --------------------------------------------------------------------------
# Texts. Swiss German spelling: no "sharp s", always "ss".
# --------------------------------------------------------------------------
LANGS = ["de", "fr", "it", "en"]
LANG_NAMES = {"de": "Deutsch", "fr": "Français", "it": "Italiano", "en": "English"}

T = {
    "de": {
        "title": "CubeIT – Bau deinen Computer",
        "m1": "Mission 1: Bau den Computer",
        "m2": "Mission 2: Robo-Cube",
        "m3": "Mission 3: Binär-Würfel",
        "lang": "Sprache",
        "quit": "Beenden",
        "menu_hint": "Pfeiltasten + Enter oder Maus. ESC = zurück",
        "m1_goal": "Ziel: Verbinde Strom, Bildschirm und USB mit dem Gehirn-Würfel. Dann drücke P (Power).",
        "m1_hint": "1-4 Würfel wählen · Pfeile bewegen · Enter setzen · Entf entfernen · P Power",
        "power": "Power",
        "no_power": "Nichts passiert... Der Computer hat keinen Strom!",
        "no_display": "Der Computer läuft, aber du siehst nichts. Es fehlt die AUSGABE!",
        "no_input": "Das Bild ist da, aber du kannst nichts eingeben. Es fehlt die EINGABE!",
        "loose": "Ein Würfel berührt die anderen nicht. Magnete müssen sich berühren!",
        "booted": "Geschafft! Dein Computer läuft.",
        "eva": "EVA-Prinzip: Eingabe (USB) – Verarbeitung (Gehirn) – Ausgabe (Bildschirm).",
        "continue": "Enter = weiter",
        "m2_goal": "Ziel: Programmiere den Roboter bis zur Flagge.",
        "m2_hint": "Pfeil hoch: VOR · Pfeil links/rechts: drehen · Rücktaste: löschen · Leertaste: Start",
        "fwd": "VOR",
        "left": "LINKS",
        "right": "RECHTS",
        "del": "LÖSCHEN",
        "run": "START",
        "program": "Programm",
        "crash": "Autsch! Wand. Das ist ein BUG. Ändere dein Programm.",
        "not_goal": "Programm fertig, aber das Ziel ist nicht erreicht.",
        "level_done": "Super! Ziel erreicht.",
        "optimal": "Kürzestes Programm: {0} Befehle. Deins: {1}.",
        "pattern": "Siehst du Muster? Programmierer nennen das eine SCHLEIFE.",
        "level": "Level {0}/{1}",
        "m3_goal": "Ziel: Schalte die LEDs so, dass die Zahl {0} entsteht.",
        "m3_hint": "Tasten 1-5 oder Klick: LED an/aus",
        "m3_info": "Computer kennen nur AN (1) und AUS (0). Das nennt man BINÄR.",
        "round": "Runde {0}/{1}",
        "correct": "Richtig!",
        "mission_done": "Mission erfüllt!",
        "stars": "Sterne",
    },
    "fr": {
        "title": "CubeIT – Construis ton ordinateur",
        "m1": "Mission 1: Construis l'ordinateur",
        "m2": "Mission 2: Robo-Cube",
        "m3": "Mission 3: Cubes binaires",
        "lang": "Langue",
        "quit": "Quitter",
        "menu_hint": "Flèches + Entrée ou souris. ESC = retour",
        "m1_goal": "But: relie l'alimentation, l'écran et l'USB au cube cerveau. Puis appuie sur P (Power).",
        "m1_hint": "1-4 choisir · flèches bouger · Entrée poser · Suppr enlever · P Power",
        "power": "Power",
        "no_power": "Rien ne se passe... L'ordinateur n'a pas de courant!",
        "no_display": "L'ordinateur tourne, mais tu ne vois rien. Il manque la SORTIE!",
        "no_input": "L'image est là, mais tu ne peux rien saisir. Il manque l'ENTRÉE!",
        "loose": "Un cube ne touche pas les autres. Les aimants doivent se toucher!",
        "booted": "Bravo! Ton ordinateur fonctionne.",
        "eva": "Principe ETS: Entrée (USB) – Traitement (cerveau) – Sortie (écran).",
        "continue": "Entrée = continuer",
        "m2_goal": "But: programme le robot jusqu'au drapeau.",
        "m2_hint": "Flèche haut: avancer · gauche/droite: tourner · Retour: effacer · Espace: lancer",
        "fwd": "AVANCE",
        "left": "GAUCHE",
        "right": "DROITE",
        "del": "EFFACER",
        "run": "LANCER",
        "program": "Programme",
        "crash": "Aïe! Un mur. C'est un BUG. Corrige ton programme.",
        "not_goal": "Programme terminé, mais le but n'est pas atteint.",
        "level_done": "Super! But atteint.",
        "optimal": "Programme le plus court: {0} ordres. Le tien: {1}.",
        "pattern": "Tu vois un motif? Les programmeurs appellent ça une BOUCLE.",
        "level": "Niveau {0}/{1}",
        "m3_goal": "But: allume les LED pour former le nombre {0}.",
        "m3_hint": "Touches 1-5 ou clic: LED on/off",
        "m3_info": "Les ordinateurs ne connaissent que ON (1) et OFF (0). C'est le BINAIRE.",
        "round": "Manche {0}/{1}",
        "correct": "Juste!",
        "mission_done": "Mission accomplie!",
        "stars": "Étoiles",
    },
    "it": {
        "title": "CubeIT – Costruisci il tuo computer",
        "m1": "Missione 1: Costruisci il computer",
        "m2": "Missione 2: Robo-Cube",
        "m3": "Missione 3: Cubi binari",
        "lang": "Lingua",
        "quit": "Esci",
        "menu_hint": "Frecce + Invio o mouse. ESC = indietro",
        "m1_goal": "Obiettivo: collega alimentazione, schermo e USB al cubo cervello. Poi premi P (Power).",
        "m1_hint": "1-4 scegli · frecce muovi · Invio posa · Canc togli · P Power",
        "power": "Power",
        "no_power": "Non succede niente... Il computer non ha corrente!",
        "no_display": "Il computer funziona, ma non vedi niente. Manca l'OUTPUT!",
        "no_input": "L'immagine c'è, ma non puoi scrivere niente. Manca l'INPUT!",
        "loose": "Un cubo non tocca gli altri. I magneti devono toccarsi!",
        "booted": "Fatto! Il tuo computer funziona.",
        "eva": "Principio IEO: Input (USB) – Elaborazione (cervello) – Output (schermo).",
        "continue": "Invio = avanti",
        "m2_goal": "Obiettivo: programma il robot fino alla bandiera.",
        "m2_hint": "Freccia su: avanti · sinistra/destra: girare · Backspace: cancella · Spazio: avvia",
        "fwd": "AVANTI",
        "left": "SINISTRA",
        "right": "DESTRA",
        "del": "CANCELLA",
        "run": "AVVIA",
        "program": "Programma",
        "crash": "Ahi! Un muro. È un BUG. Correggi il programma.",
        "not_goal": "Programma finito, ma l'obiettivo non è raggiunto.",
        "level_done": "Super! Obiettivo raggiunto.",
        "optimal": "Programma più corto: {0} comandi. Il tuo: {1}.",
        "pattern": "Vedi uno schema? I programmatori lo chiamano CICLO.",
        "level": "Livello {0}/{1}",
        "m3_goal": "Obiettivo: accendi i LED per formare il numero {0}.",
        "m3_hint": "Tasti 1-5 o clic: LED acceso/spento",
        "m3_info": "I computer conoscono solo ACCESO (1) e SPENTO (0). Si chiama BINARIO.",
        "round": "Turno {0}/{1}",
        "correct": "Giusto!",
        "mission_done": "Missione compiuta!",
        "stars": "Stelle",
    },
    "en": {
        "title": "CubeIT – Build your computer",
        "m1": "Mission 1: Build the computer",
        "m2": "Mission 2: Robo-Cube",
        "m3": "Mission 3: Binary cubes",
        "lang": "Language",
        "quit": "Quit",
        "menu_hint": "Arrow keys + Enter or mouse. ESC = back",
        "m1_goal": "Goal: connect power, display and USB to the brain cube. Then press P (Power).",
        "m1_hint": "1-4 pick cube · arrows move · Enter place · Del remove · P power",
        "power": "Power",
        "no_power": "Nothing happens... The computer has no power!",
        "no_display": "The computer runs, but you see nothing. OUTPUT is missing!",
        "no_input": "The picture is there, but you cannot type. INPUT is missing!",
        "loose": "A cube does not touch the others. Magnets must touch!",
        "booted": "Well done! Your computer is running.",
        "eva": "IPO model: Input (USB) – Processing (brain) – Output (display).",
        "continue": "Enter = continue",
        "m2_goal": "Goal: program the robot to reach the flag.",
        "m2_hint": "Arrow up: forward · left/right: turn · Backspace: delete · Space: run",
        "fwd": "FWD",
        "left": "LEFT",
        "right": "RIGHT",
        "del": "DELETE",
        "run": "RUN",
        "program": "Program",
        "crash": "Ouch! A wall. That is a BUG. Change your program.",
        "not_goal": "Program finished, but the goal was not reached.",
        "level_done": "Great! Goal reached.",
        "optimal": "Shortest program: {0} commands. Yours: {1}.",
        "pattern": "Do you see a pattern? Programmers call that a LOOP.",
        "level": "Level {0}/{1}",
        "m3_goal": "Goal: switch the LEDs to make the number {0}.",
        "m3_hint": "Keys 1-5 or click: LED on/off",
        "m3_info": "Computers only know ON (1) and OFF (0). That is called BINARY.",
        "round": "Round {0}/{1}",
        "correct": "Correct!",
        "mission_done": "Mission complete!",
        "stars": "Stars",
    },
}

# Cube catalogue: the physical CubeIT modules, as the game knows them.
CUBES = {
    "brain": {
        "label": "CHIP", "color": BLUE,
        "name": {"de": "Gehirn-Würfel", "fr": "Cube cerveau", "it": "Cubo cervello", "en": "Brain cube"},
        "info": {
            "de": "Hier sitzt der C.H.I.P.: Prozessor (1 GHz), Arbeitsspeicher (512 MB) und Speicher (4 GB). Er rechnet, aber allein kann er nichts zeigen.",
            "fr": "Ici se trouve le C.H.I.P.: processeur (1 GHz), mémoire vive (512 Mo) et stockage (4 Go). Il calcule, mais seul il ne peut rien montrer.",
            "it": "Qui c'è il C.H.I.P.: processore (1 GHz), memoria RAM (512 MB) e memoria (4 GB). Calcola, ma da solo non può mostrare niente.",
            "en": "This is the C.H.I.P.: processor (1 GHz), memory (512 MB RAM) and storage (4 GB). It computes, but alone it cannot show anything.",
        },
    },
    "power": {
        "label": "5V", "color": YELLOW,
        "name": {"de": "Strom-Würfel", "fr": "Cube alimentation", "it": "Cubo alimentazione", "en": "Power cube"},
        "info": {
            "de": "Liefert 5 Volt Strom. Ohne Strom läuft kein Computer – wie ein Herz, das Blut pumpt.",
            "fr": "Fournit 5 volts. Sans courant, aucun ordinateur ne marche – comme un cœur qui pompe le sang.",
            "it": "Fornisce 5 volt. Senza corrente nessun computer funziona – come un cuore che pompa il sangue.",
            "en": "Delivers 5 volts. Without power no computer works – like a heart pumping blood.",
        },
    },
    "display": {
        "label": "HDMI", "color": MAGENTA,
        "name": {"de": "Bildschirm-Würfel", "fr": "Cube écran", "it": "Cubo schermo", "en": "Display cube"},
        "info": {
            "de": "HDMI/DVI: Macht aus den Daten des Prozessors ein Bild für den Monitor. Das ist die AUSGABE.",
            "fr": "HDMI/DVI: transforme les données du processeur en image pour le moniteur. C'est la SORTIE.",
            "it": "HDMI/DVI: trasforma i dati del processore in un'immagine per il monitor. È l'OUTPUT.",
            "en": "HDMI/DVI: turns the processor's data into a picture for the monitor. That is the OUTPUT.",
        },
    },
    "usb": {
        "label": "USB", "color": GREEN,
        "name": {"de": "USB-Würfel", "fr": "Cube USB", "it": "Cubo USB", "en": "USB cube"},
        "info": {
            "de": "Hier steckst du Tastatur und Maus ein. Das ist die EINGABE – so sagst du dem Computer, was er tun soll.",
            "fr": "Ici tu branches clavier et souris. C'est l'ENTRÉE – tu dis à l'ordinateur ce qu'il doit faire.",
            "it": "Qui colleghi tastiera e mouse. È l'INPUT – così dici al computer cosa fare.",
            "en": "Plug in keyboard and mouse here. That is the INPUT – how you tell the computer what to do.",
        },
    },
    "audio": {
        "label": "AUDIO", "color": ORANGE,
        "name": {"de": "Ton-Würfel", "fr": "Cube son", "it": "Cubo audio", "en": "Sound cube"},
        "info": {
            "de": "Macht Töne und Musik. Cool – aber nicht nötig, damit der Computer startet.",
            "fr": "Fait des sons et de la musique. Cool – mais pas nécessaire pour démarrer l'ordinateur.",
            "it": "Fa suoni e musica. Bello – ma non serve per avviare il computer.",
            "en": "Makes sounds and music. Cool – but not needed for the computer to start.",
        },
    },
}
TRAY = ["power", "display", "usb", "audio"]

BOOT_LOG = [
    "U-Boot SPL 2015.10 (C.H.I.P.)",
    "DRAM: 512 MiB",
    "NAND: 4096 MiB",
    "Starting kernel ...",
    "[    0.000000] Linux version 4.3.0-ntc",
    "[    1.204411] usb 1-1: new keyboard found",
    "[    1.893002] hdmi: 640x480 connected",
    "Debian GNU/Linux 8 chip tty1",
    "CubeIT OS ready.  chip@cubeit:~$ _",
]

# Robo-Cube mazes. S = start (facing east), G = goal, # = wall.
MAZES = [
    ["########",
     "#S...###",
     "####.###",
     "####..G#",
     "########"],
    ["########",
     "#S.....#",
     "######.#",
     "#G.....#",
     "########"],
    ["########",
     "#S#...##",
     "#.#.#.##",
     "#...#.G#",
     "########"],
]
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]   # east, south, west, north (clockwise)
MAX_PROGRAM = 24


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def load_progress():
    try:
        with io.open(SAVE_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return {"lang": data.get("lang", "de"), "stars": data.get("stars", {})}
    except Exception:
        return {"lang": "de", "stars": {}}


def save_progress(progress):
    try:
        with io.open(SAVE_FILE, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(progress, ensure_ascii=False))
    except Exception:
        pass   # read-only SD card or kiosk mode: progress simply is not kept


def wrap(text, font, width):
    words = text.split(" ")
    lines, line = [], ""
    for word in words:
        test = word if not line else line + " " + word
        if font.size(test)[0] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text(surf, text, font, color, pos, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surf.blit(img, rect)
    return rect


def draw_wrapped(surf, text, font, color, rect, line_gap=2):
    y = rect[1]
    for line in wrap(text, font, rect[2]):
        draw_text(surf, line, font, color, (rect[0], y))
        y += font.get_linesize() + line_gap
    return y


def draw_star(surf, center, r, filled):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((center[0] + rad * math.cos(ang), center[1] + rad * math.sin(ang)))
    if filled:
        pygame.draw.polygon(surf, YELLOW, pts)
    pygame.draw.polygon(surf, YELLOW, pts, 2)


def draw_stars(surf, center, n, total=3, r=12):
    for i in range(total):
        draw_star(surf, (center[0] + (i - (total - 1) / 2.0) * r * 2.4, center[1]), r, i < n)


class Sound(object):
    """Tiny square-wave beeps generated in memory: no asset files needed."""

    def __init__(self):
        self.ok = False
        self.cache = {}
        try:
            pygame.mixer.init(22050, -16, 1, 512)
            self.ok = pygame.mixer.get_init() is not None
        except Exception:
            self.ok = False

    def beep(self, freq=660, ms=80, vol=0.25):
        if not self.ok:
            return
        key = (freq, ms)
        if key not in self.cache:
            try:
                rate = pygame.mixer.get_init()[0]
                n = int(rate * ms / 1000.0)
                period = max(2, int(rate / float(freq)))
                amp = int(32767 * vol)
                buf = array.array("h", [amp if (i % period) < period // 2 else -amp for i in range(n)])
                raw = buf.tobytes() if hasattr(buf, "tobytes") else buf.tostring()
                self.cache[key] = pygame.mixer.Sound(buffer=raw)
            except Exception:
                self.ok = False
                return
        try:
            self.cache[key].play()
        except Exception:
            pass

    def good(self):
        self.beep(880, 90)

    def bad(self):
        self.beep(180, 180)

    def click(self):
        self.beep(520, 30, 0.15)


class Button(object):
    def __init__(self, rect, text_key, color=PANEL_HI, action=None):
        self.rect = pygame.Rect(rect)
        self.text_key = text_key
        self.color = color
        self.action = action

    def draw(self, surf, game, focus=False):
        pygame.draw.rect(surf, self.color, self.rect, 0)
        pygame.draw.rect(surf, WHITE if focus else GREY, self.rect, 2)
        label = game.t(self.text_key)
        font = game.font_s if game.font_s.size(label)[0] <= self.rect.w - 8 else game.font_xs
        draw_text(surf, label, font, WHITE, self.rect.center, center=True)

    def hit(self, pos):
        return pos is not None and self.rect.collidepoint(pos)


# --------------------------------------------------------------------------
# Scenes
# --------------------------------------------------------------------------
class Scene(object):
    def __init__(self, game):
        self.game = game

    def handle(self, event, pos):
        pass

    def update(self, dt):
        pass

    def draw(self, surf):
        pass

    def header(self, surf, title):
        pygame.draw.rect(surf, PANEL, (0, 0, W, 40))
        draw_text(surf, title, self.game.font_m, WHITE, (16, 10))
        draw_text(surf, "CubeIT " + VERSION, self.game.font_xs, GREY, (W - 90, 14))

    def footer(self, surf, text):
        pygame.draw.rect(surf, PANEL, (0, H - 28, W, 28))
        draw_text(surf, text, self.game.font_xs, GREY, (16, H - 21))


class LanguageScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)
        self.sel = LANGS.index(game.lang) if game.lang in LANGS else 0

    def rects(self):
        return [pygame.Rect(W // 2 - 120, 140 + i * 60, 240, 46) for i in range(len(LANGS))]

    def choose(self, i):
        self.game.lang = LANGS[i]
        self.game.progress["lang"] = LANGS[i]
        save_progress(self.game.progress)
        self.game.sound.good()
        self.game.goto(MenuScene(self.game))

    def handle(self, event, pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.sel = (self.sel - 1) % len(LANGS)
            elif event.key == pygame.K_DOWN:
                self.sel = (self.sel + 1) % len(LANGS)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.choose(self.sel)
            elif event.key == pygame.K_ESCAPE:
                self.game.goto(MenuScene(self.game))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects()):
                if r.collidepoint(pos):
                    self.choose(i)

    def draw(self, surf):
        surf.fill(BG)
        self.header(surf, "Sprache · Langue · Lingua · Language")
        for i, r in enumerate(self.rects()):
            pygame.draw.rect(surf, PANEL_HI if i == self.sel else PANEL, r)
            pygame.draw.rect(surf, WHITE if i == self.sel else GREY, r, 2)
            draw_text(surf, LANG_NAMES[LANGS[i]], self.game.font_m, WHITE, r.center, center=True)
        self.footer(surf, "Up / Down + Enter")


class MenuScene(Scene):
    ITEMS = ["m1", "m2", "m3", "lang", "quit"]

    def __init__(self, game):
        Scene.__init__(self, game)
        self.sel = 0
        self.t = 0.0

    def rects(self):
        return [pygame.Rect(120, 150 + i * 56, 400, 44) for i in range(len(self.ITEMS))]

    def activate(self, i):
        item = self.ITEMS[i]
        self.game.sound.click()
        if item == "m1":
            self.game.goto(BuildScene(self.game))
        elif item == "m2":
            self.game.goto(RoboScene(self.game))
        elif item == "m3":
            self.game.goto(BinaryScene(self.game))
        elif item == "lang":
            self.game.goto(LanguageScene(self.game))
        else:
            self.game.running = False

    def handle(self, event, pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.sel = (self.sel - 1) % len(self.ITEMS)
            elif event.key == pygame.K_DOWN:
                self.sel = (self.sel + 1) % len(self.ITEMS)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.activate(self.sel)
            elif event.key == pygame.K_ESCAPE:
                self.game.running = False
        elif event.type == pygame.MOUSEMOTION:
            for i, r in enumerate(self.rects()):
                if r.collidepoint(pos):
                    self.sel = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.rects()):
                if r.collidepoint(pos):
                    self.activate(i)

    def update(self, dt):
        self.t += dt

    def draw(self, surf):
        surf.fill(BG)
        g = self.game
        # little animated cube stack as logo
        for i, key in enumerate(["power", "brain", "display", "usb"]):
            x = W // 2 - 116 + i * 60
            y = 62 + int(4 * math.sin(self.t * 3 + i))
            draw_cube(surf, g, key, pygame.Rect(x, y, 52, 52), lit=True)
        draw_text(surf, g.t("title"), g.font_m, WHITE, (W // 2, 132), center=True)
        for i, r in enumerate(self.rects()):
            item = self.ITEMS[i]
            pygame.draw.rect(surf, PANEL_HI if i == self.sel else PANEL, r)
            pygame.draw.rect(surf, WHITE if i == self.sel else GREY, r, 2)
            draw_text(surf, g.t(item), g.font_s, WHITE, (r.x + 14, r.y + 13))
            if item in ("m1", "m2", "m3"):
                draw_stars(surf, (r.right - 50, r.centery), g.progress["stars"].get(item, 0), r=9)
        self.footer(surf, g.t("menu_hint"))


def draw_cube(surf, game, key, rect, lit=False, connected=False):
    cube = CUBES[key]
    col = cube["color"] if lit else tuple(int(c * 0.45) for c in cube["color"])
    pygame.draw.rect(surf, col, rect)
    inner = rect.inflate(-10, -10)
    pygame.draw.rect(surf, tuple(min(255, c + 30) for c in col), inner, 2)
    draw_text(surf, cube["label"], game.font_xs, DARK, rect.center, center=True)
    # magnet pads in the middle of each side
    pad = WHITE if connected else GREY
    cx, cy = rect.center
    for px, py, pw, ph in ((cx - 6, rect.top, 12, 3), (cx - 6, rect.bottom - 3, 12, 3),
                           (rect.left, cy - 6, 3, 12), (rect.right - 3, cy - 6, 3, 12)):
        pygame.draw.rect(surf, pad, (px, py, pw, ph))


class BuildScene(Scene):
    """Mission 1: assemble cubes magnetically around the brain cube (MI.2.3)."""
    COLS, ROWS, CELL = 7, 5, 56
    GX, GY = 24, 56
    BRAIN = (3, 2)

    def __init__(self, game):
        Scene.__init__(self, game)
        self.grid = {self.BRAIN: "brain"}
        self.cursor = [2, 2]
        self.pick = 0
        self.info_key = "brain"
        self.message = None
        self.msg_color = WHITE
        self.fails = 0
        self.boot = None          # boot animation timer
        self.done = False
        self.power_btn = Button((456, 300, 160, 40), "power", (90, 40, 40))

    # --- model -----------------------------------------------------------
    def connected(self):
        seen = {self.BRAIN}
        todo = [self.BRAIN]
        while todo:
            x, y = todo.pop()
            for dx, dy in DIRS:
                n = (x + dx, y + dy)
                if n in self.grid and n not in seen:
                    seen.add(n)
                    todo.append(n)
        return seen

    def placed_types(self, cells):
        return set(self.grid[c] for c in cells)

    def press_power(self):
        conn = self.placed_types(self.connected())
        allp = set(self.grid.values())
        g = self.game
        if "power" not in conn:
            msg = "loose" if "power" in allp else "no_power"
        elif "display" not in conn:
            msg = "loose" if "display" in allp else "no_display"
        elif "usb" not in conn:
            msg = "loose" if "usb" in allp else "no_input"
        else:
            msg = None
        if msg:
            self.fails += 1
            self.message, self.msg_color = g.t(msg), RED
            g.sound.bad()
        else:
            self.boot = 0.0
            g.sound.good()

    def place(self, cell):
        if cell == self.BRAIN:
            self.info_key = "brain"
            return
        key = TRAY[self.pick]
        # each physical cube exists once: moving it removes it from old cell
        for c, k in list(self.grid.items()):
            if k == key:
                del self.grid[c]
        self.grid[cell] = key
        self.info_key = key
        self.message = None
        self.game.sound.click()

    def remove(self, cell):
        if cell in self.grid and cell != self.BRAIN:
            del self.grid[cell]
            self.game.sound.click()

    def cell_rect(self, c):
        return pygame.Rect(self.GX + c[0] * self.CELL, self.GY + c[1] * self.CELL, self.CELL - 4, self.CELL - 4)

    def tray_rect(self, i):
        return pygame.Rect(self.GX + i * 96, 358, 56, 56)

    def cell_at(self, pos):
        x = (pos[0] - self.GX) // self.CELL
        y = (pos[1] - self.GY) // self.CELL
        if 0 <= x < self.COLS and 0 <= y < self.ROWS:
            return (int(x), int(y))
        return None

    # --- events ----------------------------------------------------------
    def handle(self, event, pos):
        g = self.game
        if self.boot is not None:
            if self.done and event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                stars = 3 if self.fails == 0 else (2 if self.fails <= 2 else 1)
                g.award("m1", stars)
                g.goto(MenuScene(g))
            return
        if event.type == pygame.KEYDOWN:
            k = event.key
            if k == pygame.K_ESCAPE:
                g.goto(MenuScene(g))
            elif k == pygame.K_LEFT:
                self.cursor[0] = max(0, self.cursor[0] - 1)
            elif k == pygame.K_RIGHT:
                self.cursor[0] = min(self.COLS - 1, self.cursor[0] + 1)
            elif k == pygame.K_UP:
                self.cursor[1] = max(0, self.cursor[1] - 1)
            elif k == pygame.K_DOWN:
                self.cursor[1] = min(self.ROWS - 1, self.cursor[1] + 1)
            elif pygame.K_1 <= k <= pygame.K_4:
                self.pick = k - pygame.K_1
                self.info_key = TRAY[self.pick]
            elif k in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.place(tuple(self.cursor))
            elif k in (pygame.K_DELETE, pygame.K_BACKSPACE):
                self.remove(tuple(self.cursor))
            elif k == pygame.K_p:
                self.press_power()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.power_btn.hit(pos) and event.button == 1:
                self.press_power()
                return
            for i in range(len(TRAY)):
                if self.tray_rect(i).collidepoint(pos):
                    self.pick = i
                    self.info_key = TRAY[i]
                    return
            cell = self.cell_at(pos)
            if cell:
                self.cursor = list(cell)
                if event.button == 1:
                    self.place(cell)
                elif event.button == 3:
                    self.remove(cell)

    def update(self, dt):
        if self.boot is not None:
            self.boot += dt
            if self.boot > len(BOOT_LOG) * 0.35 + 0.6:
                self.done = True

    # --- drawing ---------------------------------------------------------
    def draw(self, surf):
        g = self.game
        surf.fill(BG)
        self.header(surf, g.t("m1"))
        if self.boot is not None:
            self.draw_boot(surf)
            return
        conn = self.connected()
        for x in range(self.COLS):
            for y in range(self.ROWS):
                r = self.cell_rect((x, y))
                pygame.draw.rect(surf, PANEL, r, 1)
        for c, key in self.grid.items():
            draw_cube(surf, g, key, self.cell_rect(c), lit=c in conn, connected=c in conn)
        cr = self.cell_rect(tuple(self.cursor)).inflate(6, 6)
        pygame.draw.rect(surf, WHITE, cr, 2)
        # tray
        used = set(self.grid.values())
        for i, key in enumerate(TRAY):
            r = self.tray_rect(i)
            draw_cube(surf, g, key, r, lit=key not in used)
            draw_text(surf, str(i + 1), g.font_xs, WHITE, (r.x - 14, r.y + 2))
            if i == self.pick:
                pygame.draw.rect(surf, WHITE, r.inflate(8, 8), 2)
        # info card
        card = pygame.Rect(440, 56, 184, 232)
        pygame.draw.rect(surf, PANEL, card)
        cube = CUBES[self.info_key]
        pygame.draw.rect(surf, cube["color"], (card.x, card.y, card.w, 6))
        draw_text(surf, cube["name"][g.lang], g.font_s, WHITE, (card.x + 10, card.y + 14))
        draw_wrapped(surf, cube["info"][g.lang], g.font_xs, WHITE, (card.x + 10, card.y + 44, card.w - 18, 180))
        self.power_btn.draw(surf, g)
        # goal / feedback line
        text, col = (self.message, self.msg_color) if self.message else (g.t("m1_goal"), CYAN)
        draw_wrapped(surf, text, g.font_xs, col, (440, 352, 184, 90))
        self.footer(surf, g.t("m1_hint"))

    def draw_boot(self, surf):
        g = self.game
        scr = pygame.Rect(40, 60, 560, 300)
        pygame.draw.rect(surf, DARK, scr)
        pygame.draw.rect(surf, MAGENTA, scr, 3)
        n = min(len(BOOT_LOG), int(self.boot / 0.35) + 1)
        for i in range(n):
            draw_text(surf, BOOT_LOG[i], g.font_mono, GREEN, (scr.x + 14, scr.y + 12 + i * 30))
        if self.done:
            draw_text(surf, g.t("booted"), g.font_m, YELLOW, (W // 2, 386), center=True)
            draw_wrapped(surf, g.t("eva"), g.font_xs, WHITE, (60, 408, 520, 40))
            stars = 3 if self.fails == 0 else (2 if self.fails <= 2 else 1)
            draw_stars(surf, (W // 2, 438), stars)
            self.footer(surf, g.t("continue"))


class RoboScene(Scene):
    """Mission 2: sequence commands to steer a robot (MI.2.2 algorithms)."""
    CELL = 44
    GX, GY = 24, 64

    def __init__(self, game):
        Scene.__init__(self, game)
        self.level = 0
        self.results = []
        self.buttons = [
            Button((24, 300, 86, 36), "fwd", (40, 90, 60), "F"),
            Button((116, 300, 86, 36), "left", (40, 70, 110), "L"),
            Button((208, 300, 86, 36), "right", (40, 70, 110), "R"),
            Button((300, 300, 86, 36), "del", (100, 60, 40), "DEL"),
            Button((24, 344, 362, 36), "run", (40, 110, 60), "RUN"),
        ]
        self.load_level()

    def load_level(self):
        self.maze = MAZES[self.level]
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                if ch == "S":
                    self.start = (x, y)
                elif ch == "G":
                    self.goal = (x, y)
        self.program = []
        self.optimal = self.shortest()
        self.reset_robot()
        self.state = "edit"      # edit | run | crash | miss | win
        self.message = None

    def reset_robot(self):
        self.pos = self.start
        self.dir = 0
        self.pc = 0
        self.timer = 0.0

    def wall(self, p):
        x, y = p
        if y < 0 or y >= len(self.maze) or x < 0 or x >= len(self.maze[y]):
            return True
        return self.maze[y][x] == "#"

    def shortest(self):
        start = (self.start, 0)
        dist = {start: 0}
        queue = [start]
        while queue:
            (p, d) = queue.pop(0)
            if p == self.goal:
                return dist[(p, d)]
            nexts = [(p, (d + 3) % 4), (p, (d + 1) % 4)]
            f = (p[0] + DIRS[d][0], p[1] + DIRS[d][1])
            if not self.wall(f):
                nexts.append((f, d))
            for s in nexts:
                if s not in dist:
                    dist[s] = dist[(p, d)] + 1
                    queue.append(s)
        return 0

    def command(self, c):
        g = self.game
        if self.state in ("crash", "miss"):
            self.state = "edit"
            self.reset_robot()
            self.message = None
        if self.state != "edit":
            return
        if c == "DEL":
            if self.program:
                self.program.pop()
                g.sound.click()
        elif c == "RUN":
            if self.program:
                self.reset_robot()
                self.state = "run"
        elif len(self.program) < MAX_PROGRAM:
            self.program.append(c)
            g.sound.click()

    def handle(self, event, pos):
        g = self.game
        if self.state == "win":
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    g.goto(MenuScene(g))
                    return
                self.next_level()
            return
        if event.type == pygame.KEYDOWN:
            k = event.key
            if k == pygame.K_ESCAPE:
                g.goto(MenuScene(g))
            elif k == pygame.K_UP:
                self.command("F")
            elif k == pygame.K_LEFT:
                self.command("L")
            elif k == pygame.K_RIGHT:
                self.command("R")
            elif k in (pygame.K_BACKSPACE, pygame.K_DELETE):
                self.command("DEL")
            elif k in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                self.command("RUN")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for b in self.buttons:
                if b.hit(pos):
                    self.command(b.action)

    def next_level(self):
        g = self.game
        if self.level + 1 < len(MAZES):
            self.level += 1
            self.load_level()
        else:
            g.award("m2", int(round(sum(self.results) / float(len(self.results)))))
            g.goto(MenuScene(g))

    def update(self, dt):
        if self.state != "run":
            return
        self.timer += dt
        if self.timer < 0.4:
            return
        self.timer = 0.0
        g = self.game
        c = self.program[self.pc]
        if c == "L":
            self.dir = (self.dir + 3) % 4
        elif c == "R":
            self.dir = (self.dir + 1) % 4
        else:
            f = (self.pos[0] + DIRS[self.dir][0], self.pos[1] + DIRS[self.dir][1])
            if self.wall(f):
                self.state = "crash"
                self.message = (g.t("crash"), RED)
                g.sound.bad()
                return
            self.pos = f
            g.sound.click()
        self.pc += 1
        if self.pos == self.goal:
            self.state = "win"
            n = len(self.program)
            stars = 3 if n <= self.optimal else (2 if n <= self.optimal + 3 else 1)
            self.results.append(stars)
            g.sound.good()
            return
        if self.pc >= len(self.program):
            self.state = "miss"
            self.message = (g.t("not_goal"), ORANGE)
            g.sound.bad()

    def draw(self, surf):
        g = self.game
        surf.fill(BG)
        self.header(surf, g.t("m2") + "  ·  " + g.t("level").format(self.level + 1, len(MAZES)))
        # maze
        for y, row in enumerate(self.maze):
            for x, ch in enumerate(row):
                r = pygame.Rect(self.GX + x * self.CELL, self.GY + y * self.CELL, self.CELL - 2, self.CELL - 2)
                if ch == "#":
                    pygame.draw.rect(surf, DARK, r)
                    pygame.draw.rect(surf, (52, 56, 70), r, 1)
                else:
                    pygame.draw.rect(surf, (66, 76, 104), r)
                if (x, y) == self.goal:
                    pygame.draw.line(surf, WHITE, (r.x + 14, r.y + 8), (r.x + 14, r.bottom - 8), 3)
                    pygame.draw.polygon(surf, GREEN, [(r.x + 15, r.y + 8), (r.right - 10, r.y + 15), (r.x + 15, r.y + 22)])
        # robot
        cx = self.GX + self.pos[0] * self.CELL + self.CELL // 2 - 1
        cy = self.GY + self.pos[1] * self.CELL + self.CELL // 2 - 1
        dx, dy = DIRS[self.dir]
        col = RED if self.state == "crash" else CYAN
        pygame.draw.rect(surf, col, (cx - 15, cy - 15, 30, 30))
        tip = (cx + dx * 13, cy + dy * 13)
        pygame.draw.polygon(surf, DARK, [tip, (cx - dy * 9 - dx * 5, cy + dx * 9 - dy * 5),
                                         (cx + dy * 9 - dx * 5, cy - dx * 9 - dy * 5)])
        # buttons
        for b in self.buttons:
            b.draw(surf, g)
        # program panel
        panel = pygame.Rect(404, 56, 220, 324)
        pygame.draw.rect(surf, PANEL, panel)
        draw_text(surf, "{0}  ({1}/{2})".format(g.t("program"), len(self.program), MAX_PROGRAM),
                  g.font_s, WHITE, (panel.x + 10, panel.y + 8))
        names = {"F": g.t("fwd"), "L": g.t("left"), "R": g.t("right")}
        colors = {"F": (40, 90, 60), "L": (40, 70, 110), "R": (40, 70, 110)}
        for i, c in enumerate(self.program):
            r = pygame.Rect(panel.x + 8 + (i % 3) * 70, panel.y + 38 + (i // 3) * 34, 66, 28)
            active = self.state in ("run", "crash") and i == min(self.pc, len(self.program) - 1)
            pygame.draw.rect(surf, colors[c], r)
            pygame.draw.rect(surf, YELLOW if active else GREY, r, 2 if active else 1)
            draw_text(surf, names[c], g.font_xs, WHITE, r.center, center=True)
        # status line
        box = (24, 392, 600, 52)
        if self.state == "win":
            n = len(self.program)
            stars = self.results[-1]
            draw_text(surf, g.t("level_done"), g.font_m, YELLOW, (24, 390))
            draw_text(surf, g.t("optimal").format(self.optimal, n), g.font_xs, WHITE, (24, 420))
            draw_stars(surf, (560, 404), stars)
            if self.level == 1:
                draw_text(surf, g.t("pattern"), g.font_xs, CYAN, (24, 436))
            self.footer(surf, g.t("continue"))
            return
        if self.message:
            draw_wrapped(surf, self.message[0], g.font_xs, self.message[1], box)
        else:
            draw_wrapped(surf, g.t("m2_goal"), g.font_xs, CYAN, box)
        self.footer(surf, g.t("m2_hint"))


class BinaryScene(Scene):
    """Mission 3: build numbers from on/off LED cubes (MI.2.1 data)."""
    BITS = [16, 8, 4, 2, 1]
    ROUNDS = 5

    def __init__(self, game):
        Scene.__init__(self, game)
        pool = list(range(1, 32))
        random.shuffle(pool)
        # first round is easy (single LED), then grow
        easy = [n for n in pool if bin(n).count("1") == 1]
        rest = [n for n in pool if bin(n).count("1") > 1]
        self.targets = [easy[0]] + sorted(rest[:self.ROUNDS - 1], key=lambda n: bin(n).count("1"))
        self.round = 0
        self.on = [False] * 5
        self.toggles = 0
        self.minimal = 0
        self.flash = None
        self.finished = False
        self.t = 0.0

    def value(self):
        return sum(b for b, o in zip(self.BITS, self.on) if o)

    def rect(self, i):
        return pygame.Rect(70 + i * 104, 170, 84, 84)

    def toggle(self, i):
        if self.flash is not None or self.finished:
            return
        self.on[i] = not self.on[i]
        self.toggles += 1
        self.game.sound.click()
        if self.value() == self.targets[self.round]:
            self.minimal += bin(self.targets[self.round]).count("1")
            self.flash = 0.0
            self.game.sound.good()

    def stars(self):
        extra = self.toggles - self.minimal
        return 3 if extra <= 0 else (2 if extra <= 6 else 1)

    def handle(self, event, pos):
        g = self.game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            g.goto(MenuScene(g))
            return
        if self.finished:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                g.award("m3", self.stars())
                g.goto(MenuScene(g))
            return
        if event.type == pygame.KEYDOWN and pygame.K_1 <= event.key <= pygame.K_5:
            self.toggle(event.key - pygame.K_1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(5):
                if self.rect(i).collidepoint(pos):
                    self.toggle(i)

    def update(self, dt):
        self.t += dt
        if self.flash is not None:
            self.flash += dt
            if self.flash > 1.2:
                self.flash = None
                self.round += 1
                self.on = [False] * 5
                if self.round >= self.ROUNDS:
                    self.finished = True
                    self.round = self.ROUNDS - 1

    def draw(self, surf):
        g = self.game
        surf.fill(BG)
        self.header(surf, g.t("m3") + "  ·  " + g.t("round").format(self.round + 1, self.ROUNDS))
        target = self.targets[self.round]
        if self.finished:
            draw_text(surf, g.t("mission_done"), g.font_l, YELLOW, (W // 2, 180), center=True)
            draw_wrapped(surf, g.t("m3_info"), g.font_s, WHITE, (80, 240, 480, 80))
            draw_stars(surf, (W // 2, 330), self.stars(), r=16)
            self.footer(surf, g.t("continue"))
            return
        draw_text(surf, g.t("m3_goal").format(target), g.font_m, CYAN, (W // 2, 80), center=True)
        draw_text(surf, str(target), g.font_l, WHITE, (W // 2, 128), center=True)
        for i, b in enumerate(self.BITS):
            r = self.rect(i)
            on = self.on[i]
            pygame.draw.rect(surf, PANEL, r)
            pygame.draw.rect(surf, WHITE if on else GREY, r, 2)
            led = YELLOW if on else (60, 60, 50)
            pygame.draw.circle(surf, led, (r.centerx, r.y + 32), 18)
            if on:
                glow = int(4 + 3 * math.sin(self.t * 6))
                pygame.draw.circle(surf, (255, 240, 160), (r.centerx, r.y + 32), 18 + glow, 2)
            draw_text(surf, "1" if on else "0", g.font_m, WHITE, (r.centerx, r.y + 68), center=True)
            draw_text(surf, str(b), g.font_s, GREY, (r.centerx, r.bottom + 16), center=True)
            draw_text(surf, str(i + 1), g.font_xs, GREY, (r.x + 4, r.y + 2))
        parts = [str(b) for b, o in zip(self.BITS, self.on) if o]
        formula = (" + ".join(parts) if parts else "0") + " = " + str(self.value())
        col = GREEN if self.value() == target else WHITE
        draw_text(surf, formula, g.font_m, col, (W // 2, 312), center=True)
        bits = "".join("1" if o else "0" for o in self.on)
        draw_text(surf, "binär / binary: " + bits, g.font_mono, GREY, (W // 2, 346), center=True)
        if self.flash is not None:
            draw_text(surf, g.t("correct"), g.font_l, GREEN, (W // 2, 396), center=True)
        else:
            draw_wrapped(surf, g.t("m3_info"), g.font_xs, CYAN, (70, 384, 500, 50))
        self.footer(surf, g.t("m3_hint"))


# --------------------------------------------------------------------------
# Game shell
# --------------------------------------------------------------------------
class Game(object):
    def __init__(self, args):
        pygame.mixer.pre_init(22050, -16, 1, 512)
        pygame.init()
        pygame.display.set_caption("CubeIT")
        flags = 0
        size = (W, H)
        if "--fullscreen" in args:
            info = pygame.display.Info()
            size = (info.current_w or W, info.current_h or H)
            flags = pygame.FULLSCREEN
        for a in args:
            if a.startswith("--size="):
                try:
                    size = tuple(int(v) for v in a.split("=", 1)[1].lower().split("x"))
                except ValueError:
                    pass
        self.screen = pygame.display.set_mode(size, flags)
        pygame.mouse.set_visible(True)
        self.canvas = pygame.Surface((W, H))
        self.font_xs = pygame.font.Font(None, 20)
        self.font_s = pygame.font.Font(None, 26)
        self.font_m = pygame.font.Font(None, 32)
        self.font_l = pygame.font.Font(None, 56)
        mono = pygame.font.match_font("dejavusansmono,liberationmono,couriernew,monospace")
        self.font_mono = pygame.font.Font(mono, 16) if mono else self.font_xs
        self.sound = Sound()
        self.progress = load_progress()
        self.lang = self.progress.get("lang", "de")
        for a in args:
            if a.startswith("--lang="):
                self.lang = a.split("=", 1)[1]
        if self.lang not in LANGS:
            self.lang = "de"
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = MenuScene(self) if "lang" in self.progress and os.path.exists(SAVE_FILE) else LanguageScene(self)
        self.update_viewport()

    def t(self, key):
        return T[self.lang].get(key, T["en"].get(key, key))

    def goto(self, scene):
        self.scene = scene

    def award(self, mission, stars):
        best = self.progress["stars"].get(mission, 0)
        self.progress["stars"][mission] = max(best, stars)
        save_progress(self.progress)

    def update_viewport(self):
        sw, sh = self.screen.get_size()
        self.scale = min(sw / float(W), sh / float(H))
        vw, vh = int(W * self.scale), int(H * self.scale)
        self.offset = ((sw - vw) // 2, (sh - vh) // 2)
        self.view_size = (vw, vh)

    def to_logical(self, pos):
        return (int((pos[0] - self.offset[0]) / self.scale), int((pos[1] - self.offset[1]) / self.scale))

    def present(self):
        if self.view_size == (W, H) and self.offset == (0, 0):
            self.screen.blit(self.canvas, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
            self.screen.blit(pygame.transform.scale(self.canvas, self.view_size), self.offset)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                pos = self.to_logical(event.pos) if hasattr(event, "pos") else None
                self.scene.handle(event, pos)
            self.scene.update(dt)
            self.scene.draw(self.canvas)
            self.present()
        pygame.quit()


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print("Options: --fullscreen  --size=WxH  --lang=de|fr|it|en")
        return 0
    Game(sys.argv[1:]).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
