"""Generate per-variant preview cards: a syntax-highlighted code panel
stacked above the palette card, like Gruvbox-Material's preview grid.

Run:
  uvx --from prev_gen python generate_previews.py

Outputs (one pair per vscode/*.json variant):
  assets/preview-<slug>.png
  assets/palette-<slug>.png
"""

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from prev_gen import Color, Previewer, Settings

from generate import PALETTES

ANSI_NAMES = [
    "Black",
    "Red",
    "Green",
    "Yellow",
    "Blue",
    "Magenta",
    "Cyan",
    "White",
    "Br Black",
    "Br Red",
    "Br Green",
    "Br Yellow",
    "Br Blue",
    "Br Magenta",
    "Br Cyan",
    "Br White",
]

CODE = """\
# Compute the nth Fibonacci number recursively.
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


result = fibonacci(10)
print(f"fib(10) = {result}")  # -> 55
"""

PY_KEYWORDS = (
    "def return if else elif for while class import from as in not and or is "
    "None True False lambda yield with try except raise pass break continue"
).split()

TOKEN_RE = re.compile(
    r"(?P<comment>\#[^\n]*)"
    r"|(?P<string>f?\"[^\"\n]*\"|f?\'[^\'\n]*\')"
    rf"|(?P<keyword>\b(?:{'|'.join(PY_KEYWORDS)})\b)"
    r"|(?P<number>\b\d+(?:\.\d+)?\b)"
    r"|(?P<function>[A-Za-z_]\w*(?=\s*\())"
    r"|(?P<ws>\s+)"
    r"|(?P<plain>\S)"
)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "/System/Library/Fonts/SFNSMono.ttf",
]


def load_mono(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def find_scope(theme: dict, *needles: str) -> str | None:
    for rule in theme.get("tokenColors", []):
        scope = rule.get("scope", "")
        if isinstance(scope, list):
            scope = ", ".join(scope)
        for n in needles:
            if n in scope:
                fg = rule.get("settings", {}).get("foreground")
                if fg:
                    return fg
    return None


def token_colors(theme: dict) -> dict[str, str]:
    fg = theme["colors"]["editor.foreground"]
    return {
        "comment": find_scope(theme, "comment,") or fg,
        "string": find_scope(theme, "string, ", '"string"') or fg,
        "keyword": find_scope(theme, "keyword.control,", "keyword,") or fg,
        "number": find_scope(theme, "constant.numeric") or fg,
        "function": find_scope(theme, "entity.name.function") or fg,
        "plain": fg,
        "ws": fg,
    }


def render_code(theme: dict, target_width: int) -> Image.Image:
    bg = theme["colors"]["editor.background"]
    colors = token_colors(theme)
    font_size = 22
    font = load_mono(font_size)
    line_height = int(font_size * 1.55)
    pad_y = 28

    lines = CODE.splitlines()
    max_w = max(int(font.getlength(line)) for line in lines)
    canvas_h = line_height * len(lines) + 2 * pad_y
    pad_x = max(28, (target_width - max_w) // 2)

    img = Image.new("RGB", (target_width, canvas_h), bg)
    draw = ImageDraw.Draw(img)

    x, y = pad_x, pad_y
    for line in lines:
        for m in TOKEN_RE.finditer(line):
            kind = m.lastgroup
            text = m.group()
            if kind != "ws":
                draw.text(
                    (x, y), text, font=font, fill=colors.get(kind, colors["plain"])
                )
            x += font.getlength(text)
        y += line_height
        x = pad_x

    return img


def render_palette(name: str, p: dict) -> Image.Image:
    settings = Settings(
        file_name="_unused",
        grid_width=240,
        grid_height=180,
        font_name="Nunito",
        name_size=28,
        hex_size=22,
        hex_offset=28,
    )
    surfaces = [
        Color(p["background"], "Background"),
        Color(p["foreground"], "Foreground"),
        Color(p["cursor_bg"], "Cursor"),
        Color(p["selection_bg"], "Selection"),
    ]
    rows = [
        [Color(p["ansi"][i + j], ANSI_NAMES[i + j]) for j in range(4)]
        for i in range(0, 16, 4)
    ]
    grid = [settings, surfaces, *rows]
    img = Previewer(grid, show=False, save=False)
    return img.convert("RGB")


def render_strip(name: str, p: dict, out_dir: Path) -> None:
    """One row of rounded swatch blocks, the theme's unique accent colors.

    Used in the README header. Deduped so variants whose bright ANSI
    colors equal the normal ones do not show twins.
    """
    accents = p["ansi"][1:7] + p["ansi"][9:15]
    seen: set[str] = set()
    colors = [c for c in accents if not (c.lower() in seen or seen.add(c.lower()))]

    scale = 2  # supersample for smooth corners
    block, gap, radius = 120 * scale, 30 * scale, 36 * scale
    w = len(colors) * block + (len(colors) - 1) * gap
    img = Image.new("RGBA", (w, block), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i, c in enumerate(colors):
        x = i * (block + gap)
        draw.rounded_rectangle((x, 0, x + block, block), radius=radius, fill=c)
    img = img.resize((w // scale, block // scale), Image.Resampling.LANCZOS)
    img.save(out_dir / f"strip-{name}.png")


def composite(name: str, palette: dict, theme: dict, out_dir: Path) -> None:
    pal = render_palette(name, palette)
    code = render_code(theme, target_width=pal.width)
    card = Image.new(
        "RGB",
        (pal.width, code.height + pal.height),
        theme["colors"]["editor.background"],
    )
    card.paste(code, (0, 0))
    card.paste(pal, (0, code.height))
    card.save(out_dir / f"preview-{name}.png")
    pal.save(out_dir / f"palette-{name}.png")


def main() -> None:
    base = Path(__file__).parent
    out = base / "assets"
    out.mkdir(exist_ok=True)
    for name, palette in PALETTES.items():
        theme_path = base / "vscode" / f"{name}.json"
        theme = json.loads(theme_path.read_text())
        composite(name, palette, theme, out)
        render_strip(name, palette, out)
        print(f"  assets/preview-{name}.png")
        print(f"  assets/strip-{name}.png")


if __name__ == "__main__":
    main()
