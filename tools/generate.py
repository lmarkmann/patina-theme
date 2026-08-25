#!/usr/bin/env python3
"""Generate every published theme file from palette/*.toml.

palette/<variant>.toml holds the colours; tools/keymap.toml holds the mapping
from each target's keys onto those tokens. Nothing else in the repo is a
colour source. Run after editing a palette:

  just generate
"""

import json
import tomllib
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
VARIANTS = [
    "patina-dark",
    "patina-dark-soft",
    "patina-moss",
    "patina-light",
    "patina-lichen",
    "patina-stellar",
]
SECTIONS = ("ground", "ink", "accent", "syntax", "status", "zed", "extra")


def load_keymap():
    return tomllib.loads((BASE / "tools" / "keymap.toml").read_text())


def load_palette(variant):
    p = tomllib.loads((BASE / "palette" / f"{variant}.toml").read_text())
    tok = {}
    for section in SECTIONS:
        tok.update(p.get(section, {}))
    for name, ref in p.get("alpha", {}).items():
        target, alpha = ref.rsplit("/", 1)
        tok[name] = tok[target] + alpha
    return p["name"], p["base"], tok


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def build_vscode(name, base, tok, km):
    theme = {"name": name, "base": base, "colors": {}}
    for key, token in km["vscode"]["colors"].items():
        if token in tok:
            theme["colors"][key] = tok[token]
    theme["semanticHighlighting"] = True
    theme["semanticTokenColors"] = {
        k: tok[t] for k, t in km["vscode"]["semanticTokenColors"].items() if t in tok
    }
    rules = []
    for rule in km["vscode"]["tokenColors"]:
        settings = {}
        for field in rule["settings_order"]:
            if field == "fontStyle":
                settings["fontStyle"] = rule["fontStyle"]
            elif rule.get(field) in tok:
                settings[field] = tok[rule[field]]
        rules.append({"scope": rule["scope"], "settings": settings})
    theme["tokenColors"] = rules
    return theme


def build_zed(palettes, km):
    z = km["zed"]
    themes = []
    for variant in VARIANTS:
        name, base, tok = palettes[variant]
        style = {}
        for key in z["order"]:
            if key == "accents":
                style["accents"] = [tok[t] for t in z["accents"]["tokens"]]
            elif key == "players":
                style["players"] = [
                    {f: tok[t] for f, t in player.items()} for player in z["players"]
                ]
            elif key == "syntax":
                syntax = {}
                for scope, spec in z["syntax"].items():
                    entry = {}
                    for field in spec["order"]:
                        if field == "color":
                            entry["color"] = tok.get(spec.get("color"))
                        else:
                            entry[field] = spec.get(field)
                    syntax[scope] = entry
                style["syntax"] = syntax
            else:
                token = z["style"][key]
                if token in tok:
                    style[key] = tok[token]
        themes.append(
            {
                "name": name,
                "appearance": "dark" if base == "vs-dark" else "light",
                "style": style,
            }
        )
    return {
        "$schema": "https://zed.dev/schema/themes/v0.2.0.json",
        "name": "Patina",
        "author": "Patina Theme",
        "themes": themes,
    }


ANSI_KEYS = [
    "terminal.ansiBlack",
    "terminal.ansiRed",
    "terminal.ansiGreen",
    "terminal.ansiYellow",
    "terminal.ansiBlue",
    "terminal.ansiMagenta",
    "terminal.ansiCyan",
    "terminal.ansiWhite",
    "terminal.ansiBrightBlack",
    "terminal.ansiBrightRed",
    "terminal.ansiBrightGreen",
    "terminal.ansiBrightYellow",
    "terminal.ansiBrightBlue",
    "terminal.ansiBrightMagenta",
    "terminal.ansiBrightCyan",
    "terminal.ansiBrightWhite",
]

ITERM_KEYS = [f"Ansi {i} Color" for i in range(16)]


def terminal_palette(tok, km):
    """The terminal colours, read through the same keymap VS Code uses, so the
    two can never disagree again."""
    look = lambda key: tok[km["vscode"]["colors"][key]]
    return {
        "ansi": [look(k) for k in ANSI_KEYS],
        "background": look("editor.background"),
        "foreground": look("terminal.foreground"),
        "selection": look("terminal.selectionBackground"),
    }


def hex_to_floats(h):
    h = h.lstrip("#")[:6]
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def gen_ghostty(name, pal):
    lines = [f"# {name} theme for Ghostty", ""]
    lines += [f"palette = {i}={c}" for i, c in enumerate(pal["ansi"])]
    lines += [
        "",
        f"background = {pal['background']}",
        f"foreground = {pal['foreground']}",
        f"cursor-color = {pal['foreground']}",
        f"cursor-text = {pal['background']}",
        f"selection-background = {pal['selection']}",
        f"selection-foreground = {pal['foreground']}",
    ]
    return "\n".join(lines) + "\n"


def _iterm_entry(key, h):
    r, g, b = hex_to_floats(h)
    return [
        f"\t<key>{key}</key>",
        "\t<dict>",
        "\t\t<key>Color Space</key>",
        "\t\t<string>sRGB</string>",
        "\t\t<key>Red Component</key>",
        f"\t\t<real>{r:.10f}</real>",
        "\t\t<key>Green Component</key>",
        f"\t\t<real>{g:.10f}</real>",
        "\t\t<key>Blue Component</key>",
        f"\t\t<real>{b:.10f}</real>",
        "\t</dict>",
    ]


def gen_iterm2(pal):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
        '<plist version="1.0">',
        "<dict>",
    ]
    for i, key in enumerate(ITERM_KEYS):
        lines += _iterm_entry(key, pal["ansi"][i])
    lines += _iterm_entry("Background Color", pal["background"])
    lines += _iterm_entry("Foreground Color", pal["foreground"])
    lines += _iterm_entry("Cursor Color", pal["foreground"])
    lines += _iterm_entry("Cursor Text Color", pal["background"])
    lines += _iterm_entry("Selection Color", pal["selection"])
    lines += _iterm_entry("Selected Text Color", pal["foreground"])
    lines += ["</dict>", "</plist>"]
    return "\n".join(lines) + "\n"


def gen_helix(tok, km):
    out = []
    for line in km["helix"]["template"]:
        for name, value in tok.items():
            line = line.replace(f"%{name}%", value)
        out.append(line)
    return "\n".join(out) + "\n"


def gen_yazi(name, tok, lines):
    out = []
    for line in lines:
        line = line.replace("%NAME%", name)
        line = line.replace("%SHORT%", name.removeprefix("Patina "))
        for token, value in tok.items():
            line = line.replace(f"%{token}%", value)
        out.append(line)
    return "\n".join(out) + "\n"


YAZI_README = """# {slug}

A [Yazi](https://github.com/sxyazi/yazi) flavor from the **Patina** theme,
**{short}** variant.

![preview](./preview.png)

Background `{bg}`, foreground `{fg}`, accent `{accent}`.

## Install

```sh
ya pkg add lmarkmann/patina-theme:{slug}
```

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
{mode} = "{slug}"
```

Icons need a Nerd Font in your terminal; the flavor sets colours, not glyphs.

## Contents

- `flavor.toml` UI colours (file list, mode, status, tabs, which, help, notify)
- `tmtheme.xml` syntax colours for the file-preview pane

Generated from `palette/{slug}.toml` in the Patina repo. MIT licensed.
"""


def main():
    km = load_keymap()
    palettes = {v: load_palette(v) for v in VARIANTS}

    for variant in VARIANTS:
        name, base, tok = palettes[variant]
        theme = build_vscode(name, base, tok, km)
        write(
            BASE / "vscode" / f"{variant}.json",
            json.dumps(theme, indent=2, ensure_ascii=False) + "\n",
        )

    write(
        BASE / "themes" / "patina.json",
        json.dumps(build_zed(palettes, km), indent=2, ensure_ascii=False) + "\n",
    )

    for variant in VARIANTS:
        name, _, tok = palettes[variant]
        pal = terminal_palette(tok, km)
        write(BASE / "terminals" / "ghostty" / variant, gen_ghostty(name, pal))
        write(
            BASE / "contrib" / "iterm2-color-schemes" / f"{name}.itermcolors",
            gen_iterm2(pal),
        )
        write(
            BASE / "helix-editor" / f"{variant.replace('-', '_')}.toml",
            gen_helix(tok, km),
        )

        flavor_dir = BASE / f"{variant}.yazi"
        write(flavor_dir / "flavor.toml", gen_yazi(name, tok, km["yazi"]["flavor"]))
        write(flavor_dir / "tmtheme.xml", gen_yazi(name, tok, km["yazi"]["tmtheme"]))
        write(
            flavor_dir / "README.md",
            YAZI_README.format(
                slug=variant,
                short=name.removeprefix("Patina "),
                bg=tok["bg"],
                fg=tok["fg"],
                accent=tok["accent"],
                mode="dark" if palettes[variant][1] == "vs-dark" else "light",
            ),
        )
        write(flavor_dir / "LICENSE", (BASE / "LICENSE").read_text())

    print(f"vscode/*.json ({len(VARIANTS)}), themes/patina.json, "
          f"terminals/ghostty/*, contrib/iterm2-color-schemes/*, helix-editor/*, "
          f"patina-*.yazi/*")


if __name__ == "__main__":
    main()
