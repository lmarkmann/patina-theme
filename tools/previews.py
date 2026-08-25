"""Render per-variant preview cards: a syntax-highlighted code panel stacked
above the palette card.

Local only. The code panel uses Input, the palette card uses Nunito, and
neither font is present on a CI runner, so this is never wired into a workflow.

Run:
  just previews

Outputs:
  assets/preview-<slug>.png          committed, used by README and marketplace
  patina-<slug>.yazi/preview.png     committed, used by the flavor README
  preview-out/palette-<slug>.png     ignored, on demand
  preview-out/strip-<slug>.png       ignored, on demand
"""

import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from prev_gen import Color, Previewer, Settings

from generate import VARIANTS, load_keymap, load_palette, terminal_palette

BASE = Path(__file__).resolve().parent.parent

ANSI_NAMES = [
    "Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White",
    "Br Black", "Br Red", "Br Green", "Br Yellow", "Br Blue", "Br Magenta",
    "Br Cyan", "Br White",
]

CODE = """\
// Iron rusts away; copper rusts shut.
const STAGES: [(&str, u32); 4] = [
    ("copper", 0),
    ("tarnish", 1),
    ("patina", 17),
    ("verdigris", 30),
];

fn weather(years: u32) -> &'static str {
    let i = STAGES.partition_point(|&(_, since)| since <= years);
    STAGES[i - 1].0
}

fn main() {
    for age in [0, 5, 20, 40] {
        println!("{age:>2} years: {}", weather(age));
    }
}
"""

CONTROL = "for if else match return while loop break continue".split()
KEYWORDS = (
    "const fn let mut pub use mod struct impl enum trait static ref where as in "
    "self crate move dyn type unsafe"
).split()
PRIMITIVES = "u8 u16 u32 u64 i8 i16 i32 i64 f32 f64 usize isize bool char str".split()

# Order matters: macro before function, so println! is not read as a call.
TOKEN_RE = re.compile(
    r"(?P<comment>//[^\n]*)"
    r"|(?P<string>\"[^\"\n]*\")"
    rf"|(?P<control>\b(?:{'|'.join(CONTROL)})\b)"
    rf"|(?P<keyword>\b(?:{'|'.join(KEYWORDS)})\b)"
    rf"|(?P<type>\b(?:{'|'.join(PRIMITIVES)})\b|\b[A-Z][a-z]\w*\b)"
    r"|(?P<constant>\b[A-Z][A-Z0-9_]{2,}\b)"
    r"|(?P<macro>[A-Za-z_]\w*!)"
    r"|(?P<function>[A-Za-z_]\w*(?=\s*\())"
    r"|(?P<number>\b\d+(?:\.\d+)?\b)"
    r"|(?P<operator>[-+*/%<>=!&|]+)"
    r"|(?P<punctuation>[(){}\[\];:,.])"
    r"|(?P<ws>\s+)"
    r"|(?P<plain>\S)"
)

# Palette token behind each highlight group.
CODE_TOKENS = {
    "comment": "comment",
    "string": "string_plain",
    "control": "red",
    "keyword": "accent",
    "type": "cyan",
    "constant": "constant",
    "macro": "red",
    "function": "olive",
    "number": "teal",
    "operator": "operator",
    "punctuation": "punctuation",
    "plain": "fg",
}

FONT_CANDIDATES = [
    str(Path.home() / "Library/Fonts/Input-Regular_(InputMonoNarrow-Light).ttf"),
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
]
FONT_SIZE = 18


def load_mono(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def render_code(tok: dict, target_width: int) -> Image.Image:
    colors = {group: tok[name] for group, name in CODE_TOKENS.items()}
    font = load_mono(FONT_SIZE)
    line_height = int(FONT_SIZE * 1.55)
    pad_y = 28

    lines = CODE.splitlines()
    max_w = max(int(font.getlength(line)) for line in lines)
    if max_w > target_width - 56:
        raise SystemExit(
            f"code panel is {max_w}px wide but the card is {target_width}px; "
            f"lower FONT_SIZE or shorten the sample"
        )
    canvas_h = line_height * len(lines) + 2 * pad_y
    pad_x = max(28, (target_width - max_w) // 2)

    img = Image.new("RGB", (target_width, canvas_h), tok["bg"])
    draw = ImageDraw.Draw(img)
    x, y = pad_x, pad_y
    for line in lines:
        for m in TOKEN_RE.finditer(line):
            if m.lastgroup != "ws":
                draw.text((x, y), m.group(), font=font, fill=colors[m.lastgroup])
            x += font.getlength(m.group())
        y += line_height
        x = pad_x
    return img


def render_palette(name: str, pal: dict) -> Image.Image:
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
        Color(pal["background"], "Background"),
        Color(pal["foreground"], "Foreground"),
        Color(pal["foreground"], "Cursor"),
        Color(pal["selection"], "Selection"),
    ]
    rows = [
        [Color(pal["ansi"][i + j], ANSI_NAMES[i + j]) for j in range(4)]
        for i in range(0, 16, 4)
    ]
    return Previewer([settings, surfaces, *rows], show=False, save=False).convert("RGB")


def render_strip(slug: str, pal: dict, out: Path) -> None:
    """One row of rounded swatch blocks of the deduped accent colours."""
    accents = pal["ansi"][1:7] + pal["ansi"][9:15]
    seen: set[str] = set()
    colors = [c for c in accents if not (c.lower() in seen or seen.add(c.lower()))]

    scale = 2
    block, gap, radius = 120 * scale, 30 * scale, 36 * scale
    w = len(colors) * block + (len(colors) - 1) * gap
    img = Image.new("RGBA", (w, block), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i, c in enumerate(colors):
        x = i * (block + gap)
        draw.rounded_rectangle((x, 0, x + block, block), radius=radius, fill=c)
    img = img.resize((w // scale, block // scale), Image.Resampling.LANCZOS)
    img.save(out / f"strip-{slug}.png")


def main() -> None:
    km = load_keymap()
    assets = BASE / "assets"
    scratch = BASE / "preview-out"
    assets.mkdir(exist_ok=True)
    scratch.mkdir(exist_ok=True)

    for slug in VARIANTS:
        name, _, tok = load_palette(slug)
        pal = terminal_palette(tok, km)

        card = render_palette(name, pal)
        code = render_code(tok, card.width)
        out = Image.new("RGB", (card.width, code.height + card.height), tok["bg"])
        out.paste(code, (0, 0))
        out.paste(card, (0, code.height))

        out.save(assets / f"preview-{slug}.png")
        card.save(scratch / f"palette-{slug}.png")
        render_strip(slug, pal, scratch)
        shutil.copyfile(assets / f"preview-{slug}.png", BASE / f"{slug}.yazi" / "preview.png")
        print(f"  assets/preview-{slug}.png  ({out.width}x{out.height})")


if __name__ == "__main__":
    main()
