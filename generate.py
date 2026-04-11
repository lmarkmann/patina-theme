#!/usr/bin/env python3
"""Generate terminal color scheme files from palette definitions.

Outputs:
  terminals/alacritty/<name>.toml
  terminals/kitty/<name>.conf
  terminals/iterm2/<name>.itermcolors   (covers Ghostty + WezTerm via iTerm2-Color-Schemes)

Run after changing any palette:
  python3 generate.py
"""

from pathlib import Path
# Each palette defines the 20 colors that matter for terminals.
# ansi: indices 0-7 (normal), 8-15 (bright) as a flat list of 16 hex strings.
PALETTES = {
    "patina-dark": {
        "background": "#121212",
        "foreground": "#dbd7ca",
        "cursor_bg":  "#dbd7ca",
        "cursor_fg":  "#121212",
        "selection_bg": "#42403d",
        "selection_fg": "#dbd7ca",
        "ansi": [
            "#2e2e2e", "#cb7676", "#4d9375", "#e6cc77",
            "#6db3c2", "#c98a7d", "#5da9a7", "#dbd7ca",
            "#585858", "#cb7676", "#4d9375", "#e6cc77",
            "#6db3c2", "#c98a7d", "#5da9a7", "#dbd7ca",
        ],
    },
    "patina-dark-soft": {
        "background": "#1a1a1a",
        "foreground": "#dbd7ca",
        "cursor_bg":  "#dbd7ca",
        "cursor_fg":  "#1a1a1a",
        "selection_bg": "#3a3835",
        "selection_fg": "#dbd7ca",
        "ansi": [
            "#2e2e2e", "#cb7676", "#4d9375", "#e6cc77",
            "#6db3c2", "#c98a7d", "#5da9a7", "#dbd7ca",
            "#585858", "#cb7676", "#4d9375", "#e6cc77",
            "#6db3c2", "#c98a7d", "#5da9a7", "#dbd7ca",
        ],
    },
    "patina-light": {
        "background": "#ddd7c4",
        "foreground": "#2e2a24",
        "cursor_bg":  "#2e2a24",
        "cursor_fg":  "#ddd7c4",
        "selection_bg": "#bfb8a3",
        "selection_fg": "#2e2a24",
        "ansi": [
            "#2e2a24", "#9b3b3b", "#34644c", "#6e5817",
            "#2f626f", "#7a4f47", "#2e6260", "#5a5248",
            "#6a6258", "#b64747", "#3d764c", "#81651a",
            "#3a7280", "#8e5b51", "#357270", "#393a34",
        ],
    },
    "patina-stellar": {
        "background": "#f5f2ed",
        "foreground": "#2e2a24",
        "cursor_bg":  "#2e2a24",
        "cursor_fg":  "#f5f2ed",
        "selection_bg": "#dbd5c5",
        "selection_fg": "#2e2a24",
        "ansi": [
            "#2e2a24", "#a84040", "#3a7055", "#6e5817",
            "#2f626f", "#8a5a50", "#3a7a78", "#5a5248",
            "#6a6258", "#bf3c3c", "#3e7a5e", "#826743",
            "#3f7381", "#9d594b", "#337675", "#393a34",
        ],
    },
}

ANSI_NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def hex_to_floats(h: str) -> tuple[float, float, float]:
    r, g, b = hex_to_rgb(h)
    return r / 255, g / 255, b / 255


def generate_alacritty(name: str, p: dict) -> str:
    ansi = p["ansi"]
    lines = [f"# Patina {name.replace('patina-', '').replace('-', ' ').title()} theme for Alacritty\n"]

    lines += [
        "[colors.primary]",
        f'background = "{p["background"]}"',
        f'foreground = "{p["foreground"]}"',
        "",
        "[colors.cursor]",
        f'text = "{p["cursor_fg"]}"',
        f'cursor = "{p["cursor_bg"]}"',
        "",
        "[colors.selection]",
        f'text = "{p["selection_fg"]}"',
        f'background = "{p["selection_bg"]}"',
        "",
        "[colors.normal]",
    ]
    for i, label in enumerate(ANSI_NAMES):
        lines.append(f'{label} = "{ansi[i]}"')
    lines += ["", "[colors.bright]"]
    for i, label in enumerate(ANSI_NAMES):
        lines.append(f'{label} = "{ansi[8 + i]}"')
    return "\n".join(lines) + "\n"


def generate_kitty(name: str, p: dict) -> str:
    ansi = p["ansi"]
    title = name.replace("patina-", "").replace("-", " ").title()
    lines = [f"# Patina {title} theme for Kitty\n"]
    lines += [
        f'background {p["background"]}',
        f'foreground {p["foreground"]}',
        "",
        f'cursor {p["cursor_bg"]}',
        f'cursor_text_color {p["cursor_fg"]}',
        "",
        f'selection_background {p["selection_bg"]}',
        f'selection_foreground {p["selection_fg"]}',
        "",
        "# ANSI colors",
    ]
    for i in range(8):
        lines.append(f"color{i} {ansi[i]}")
    lines += ["", "# Bright colors"]
    for i in range(8):
        lines.append(f"color{8 + i} {ansi[8 + i]}")
    return "\n".join(lines) + "\n"


def _iterm_color_entry(key: str, h: str) -> list[str]:
    r, g, b = hex_to_floats(h)
    return [
        f"\t<key>{key}</key>",
        "\t<dict>",
        "\t\t<key>Color Space</key>",
        "\t\t<string>sRGB</string>",
        f"\t\t<key>Red Component</key>",
        f"\t\t<real>{r:.10f}</real>",
        f"\t\t<key>Green Component</key>",
        f"\t\t<real>{g:.10f}</real>",
        f"\t\t<key>Blue Component</key>",
        f"\t\t<real>{b:.10f}</real>",
        "\t</dict>",
    ]


ITERM_ANSI_KEYS = [
    "Ansi 0 Color", "Ansi 1 Color", "Ansi 2 Color", "Ansi 3 Color",
    "Ansi 4 Color", "Ansi 5 Color", "Ansi 6 Color", "Ansi 7 Color",
    "Ansi 8 Color", "Ansi 9 Color", "Ansi 10 Color", "Ansi 11 Color",
    "Ansi 12 Color", "Ansi 13 Color", "Ansi 14 Color", "Ansi 15 Color",
]


def generate_iterm2(_name: str, p: dict) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">',
        '<plist version="1.0">',
        "<dict>",
    ]
    for i, key in enumerate(ITERM_ANSI_KEYS):
        lines += _iterm_color_entry(key, p["ansi"][i])
    lines += _iterm_color_entry("Background Color", p["background"])
    lines += _iterm_color_entry("Foreground Color", p["foreground"])
    lines += _iterm_color_entry("Cursor Color", p["cursor_bg"])
    lines += _iterm_color_entry("Cursor Text Color", p["cursor_fg"])
    lines += _iterm_color_entry("Selection Color", p["selection_bg"])
    lines += _iterm_color_entry("Selected Text Color", p["selection_fg"])
    lines += ["</dict>", "</plist>"]
    return "\n".join(lines) + "\n"


def main():
    root = Path(__file__).parent / "terminals"
    dirs = {
        "alacritty": root / "alacritty",
        "kitty":     root / "kitty",
        "iterm2":    root / "iterm2",
    }
    for d in dirs.values():
        d.mkdir(parents=True, exist_ok=True)

    for name, palette in PALETTES.items():
        (dirs["alacritty"] / f"{name}.toml").write_text(generate_alacritty(name, palette))
        (dirs["kitty"]     / f"{name}.conf").write_text(generate_kitty(name, palette))
        (dirs["iterm2"]    / f"{name}.itermcolors").write_text(generate_iterm2(name, palette))
        print(f"  {name}")

    print("done")


if __name__ == "__main__":
    main()
