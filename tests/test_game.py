# -*- coding: utf-8 -*-
"""Headless smoke test: plays every mission to completion.
Run: SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy python tests/test_game.py [screenshot_dir]
"""
from __future__ import print_function, unicode_literals
import os, sys, tempfile
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ["HOME"] = tempfile.mkdtemp()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game"))
import pygame
import cubeit_game as cg

shots = sys.argv[1] if len(sys.argv) > 1 else None

def key(game, k):
    game.scene.handle(pygame.event.Event(pygame.KEYDOWN, key=k, mod=0, unicode=""), None)

def tick(game, seconds):
    for _ in range(int(seconds * 30)):
        game.scene.update(1 / 30.0)
    game.scene.draw(game.canvas)

def shot(game, name):
    game.scene.draw(game.canvas)
    if shots:
        pygame.image.save(game.canvas, os.path.join(shots, name + ".png"))

for lang in cg.LANGS:
    g = cg.Game(["--lang=" + lang])
    g.progress["stars"] = {}
    g.goto(cg.MenuScene(g)); shot(g, lang + "_0_menu")
    # Mission 1: wrong first, then correct
    g.goto(cg.BuildScene(g)); s = g.scene
    key(g, pygame.K_p); assert s.fails == 1 and s.boot is None
    s.cursor = [2, 2]; key(g, pygame.K_1); key(g, pygame.K_RETURN)   # power left of brain
    s.cursor = [4, 2]; key(g, pygame.K_2); key(g, pygame.K_RETURN)   # display right
    s.cursor = [3, 3]; key(g, pygame.K_4); key(g, pygame.K_RETURN)   # audio below
    s.cursor = [3, 4]; key(g, pygame.K_3); key(g, pygame.K_RETURN)   # usb below audio (chained)
    shot(g, lang + "_1_build")
    key(g, pygame.K_p); assert s.boot is not None, "boot should start"
    tick(g, 5); assert s.done; shot(g, lang + "_1_boot")
    key(g, pygame.K_RETURN); assert g.progress["stars"]["m1"] == 2
    # loose cube detection
    g.goto(cg.BuildScene(g)); s = g.scene
    s.grid[(0, 0)] = "power"; s.press_power(); assert s.message == g.t("loose")
    # Mission 2: solve each maze with the optimal program from BFS
    g.goto(cg.RoboScene(g)); r = g.scene
    solutions = [list("FFFRFFLFF"), list("FFFFFRFFRFFFFF"), list("RFFLFFLFFRFFRFFLF")]
    for lvl, prog in enumerate(solutions):
        assert r.level == lvl
        for c in prog: r.command(c)
        r.command("RUN"); tick(g, 0.45 * len(prog) + 1)
        assert r.state == "win", (lvl, r.state, r.pos)
        assert r.optimal <= len(prog)
        shot(g, "{0}_2_robo_{1}".format(lang, lvl))
        key(g, pygame.K_RETURN)
    assert "m2" in g.progress["stars"]
    # crash path
    g.goto(cg.RoboScene(g)); r = g.scene
    for c in "LF": r.command(c)
    r.command("RUN"); tick(g, 2); assert r.state == "crash"; shot(g, lang + "_2_crash")
    # Mission 3: set bits for each target
    g.goto(cg.BinaryScene(g)); b = g.scene
    for rnd in range(b.ROUNDS):
        t = b.targets[b.round]
        for i, bit in enumerate(b.BITS):
            if t & bit: key(g, pygame.K_1 + i)
        if rnd == 1: shot(g, lang + "_3_binary")
        tick(g, 1.5)
    assert b.finished; shot(g, lang + "_3_done")
    key(g, pygame.K_RETURN); assert g.progress["stars"]["m3"] == 3
    pygame.quit()
    print("OK", lang)
print("ALL OK")
