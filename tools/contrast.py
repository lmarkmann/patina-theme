#!/usr/bin/env python3
"""Contrast audit: WCAG floors for text, plus the surface-ramp deltas.

The ramp check is the one the README's claims and .claude/CLAUDE.md's
calibration notes rest on: a hover state needs enough lightness separation
from the surface it sits on to be visible at all, and hover, selected and
active must stay distinct and ordered. Patina shipped an invisible hover in
1.2.1 because nothing enforced this.

Floors: 4.5 for editor and terminal body text; 3.0 for syntax tokens, UI
chrome, and ANSI 1-7 / 9-15 (0 and 8 are background and dim roles).
Ramp: first step >= 6 L* from the surface, then strictly increasing.

  just contrast
"""

import json
import sys

from generate import VARIANTS, load_keymap, load_palette, terminal_palette, BASE

ANSI_NAMES = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright black", "bright red", "bright green", "bright yellow",
    "bright blue", "bright magenta", "bright cyan", "bright white",
]
DIM_SCOPES = {"markup.ignored", "markup.untracked"}
UI_PAIRS = [
    ("status bar", "statusBar.foreground", "statusBar.background"),
    ("side bar", "sideBar.foreground", "sideBar.background"),
    ("active tab", "tab.activeForeground", "tab.activeBackground"),
    ("selected row", "list.activeSelectionForeground", "list.activeSelectionBackground"),
    ("button", "button.foreground", "button.background"),
]
RAMP = ["element_hover", "element_selected", "element_active"]
# The project panel renders ordinary entries in the muted ink and git-status
# entries in their status colours. If the muted ink is dimmer than `ignored`,
# tracked files read as less important than ignored ones, which is backwards.
PANEL_FLOOR = 4.0
# A hover below this many L* from its surface is not perceptible; between the
# two thresholds it is thin but visible. The absolute numbers in
# .claude/CLAUDE.md were measured in OKLCH, so they are not comparable to the
# CIE L* used here; what gates publishing is perceptibility and ordering.
RAMP_FLOOR = 2.0
RAMP_WARN = 4.0


def hex_to_rgb(h):
    h = h.lstrip("#")[:6]
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lin(v):
    c = v / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(h):
    r, g, b = hex_to_rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def lstar(h):
    y = luminance(h)
    return 116 * (y ** (1 / 3)) - 16 if y > 0.008856 else 903.3 * y


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def composite(fg, bg):
    h = fg.lstrip("#")
    if len(h) != 8:
        return "#" + h[:6]
    a = int(h[6:8], 16) / 255
    out = [round(a * f + (1 - a) * b) for f, b in zip(hex_to_rgb(fg), hex_to_rgb(bg))]
    return "#{:02x}{:02x}{:02x}".format(*out)


def pairs(tok, km, theme):
    bg = tok["bg"]
    pal = terminal_palette(tok, km)
    yield ("editor text", tok["fg"], bg, 4.5, True)
    yield ("terminal text", pal["foreground"], pal["background"], 4.5, True)
    # Not every ANSI slot is text. Index 8 is the dim role in both appearances,
    # and the ground end is black on dark variants, white on light ones.
    ground = (0, 8) if lstar(bg) < 50 else (7, 8, 15)
    for i, name in enumerate(ANSI_NAMES):
        if i not in ground:
            yield (f"ansi {name}", pal["ansi"][i], pal["background"], 3.0, True)
    for label, fg_key, bg_key in UI_PAIRS:
        c = theme["colors"]
        if fg_key in c and bg_key in c:
            yield (label, c[fg_key], c[bg_key], 3.0, True)
    seen = set()
    for rule in km["vscode"]["tokenColors"]:
        name = rule.get("foreground")
        if not name or name in seen:
            continue
        seen.add(name)
        fg = tok[name]
        scope = rule["scope"]
        scopes = [scope] if isinstance(scope, str) else scope
        opaque = len(fg.lstrip("#")) == 6
        dim = all(s in DIM_SCOPES for s in scopes)
        yield (f"token {scopes[0]}", composite(fg, bg), bg, 3.0, opaque and not dim)


def check_panel(tok):
    """Muted ink must be readable and must outrank the receding roles."""
    surface = tok["surface"]
    muted = ratio(tok["fg_muted"], surface)
    failed = []
    if muted < PANEL_FLOOR:
        failed.append(f"fg_muted is {muted:.2f}:1 on the panel, floor is {PANEL_FLOOR}")
    for name in ("ignored", "fg_inactive"):
        if ratio(tok[name], surface) >= muted:
            failed.append(
                f"{name} ({ratio(tok[name], surface):.2f}) is not dimmer than "
                f"fg_muted ({muted:.2f})"
            )
    return muted, failed


def check_ramp(tok):
    """Surface ramp: each state must clear the floor and stay ordered."""
    base = lstar(tok["surface"])
    steps = [(name, abs(lstar(tok[name]) - base)) for name in RAMP]
    failed, warned = [], []
    if steps[0][1] < RAMP_FLOOR:
        failed.append(f"{RAMP[0]} is {steps[0][1]:.1f} L* from surface, floor is {RAMP_FLOOR}")
    elif steps[0][1] < RAMP_WARN:
        warned.append(f"{RAMP[0]} is a thin {steps[0][1]:.1f} L* from surface")
    for (an, a), (bn, b) in zip(steps, steps[1:]):
        if b <= a:
            failed.append(f"{bn} ({b:.1f}) does not step past {an} ({a:.1f})")
    return steps, failed, warned


def main():
    km = load_keymap()
    failed = False
    for variant in VARIANTS:
        name, _, tok = load_palette(variant)
        theme = json.loads((BASE / "vscode" / f"{variant}.json").read_text())
        print(name)
        for label, fg, bg, floor, gates in pairs(tok, km, theme):
            r = ratio(fg, bg)
            if not gates:
                mark = "info"
            elif r < floor:
                mark, failed = "FAIL", True
            elif r < 4.5:
                mark = "warn"
            else:
                mark = "ok"
            print(f"  {r:5.2f}  {mark:4}  {label}")
        muted, panel_failed = check_panel(tok)
        print(f"  panel fg_muted {muted:.2f}:1  ignored {ratio(tok['ignored'], tok['surface']):.2f}:1")
        for msg in panel_failed:
            print(f"  FAIL  panel: {msg}")
            failed = True
        steps, ramp_failed, ramp_warned = check_ramp(tok)
        print("  ramp  " + "  ".join(f"{n.removeprefix('element_')} +{d:.1f}" for n, d in steps))
        for msg in ramp_warned:
            print(f"  warn  ramp: {msg}")
        for msg in ramp_failed:
            print(f"  FAIL  ramp: {msg}")
            failed = True
        print()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
