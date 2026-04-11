# Patina

A warm, muted color theme inspired by oxidized copper. Teal verdigris meets amber warmth on deep, quiet backgrounds.

![Patina Preview](./assets/preview.gif)

## Variants

| Variant              | Background | Character                          |
| -------------------- | ---------- | ---------------------------------- |
| **Patina Dark**      | `#121212`  | Full contrast, deep black          |
| **Patina Dark Soft** | `#1a1a1a`  | Reduced contrast, gentler on eyes  |
| **Patina Light**     | `#ddd7c4`  | Warm parchment                     |
| **Patina Stellar**   | `#f5f2ed`  | Bright, airy                       |

Patina Dark, Light, and Stellar pass WCAG AA contrast (4.5:1) on every syntax token except `markup.ignored`, which is intentionally blended with the background. Patina Dark Soft intentionally softens four tokens slightly below strict AA for reduced eye strain during long sessions.

## Syntax Highlighting

![Patina Python](./assets/screenshot-python.png)

![Patina Rust](./assets/screenshot-rust.png)

## Install

Search for **Patina** in the VS Code Extensions panel, or:

```
ext install LuisCMarkmann.patina-theme
```

## Recommended pairings

- **File icons:** [Carbon Icons](https://marketplace.visualstudio.com/items?itemName=AntFu.icons-carbon)
- **Font:** [Input](https://input.djr.com/) (Mono Narrow, Light weight)

## Also available for

| Editor / Terminal | Files | Install |
| --- | --- | --- |
| [Helix](https://helix-editor.com/) | `helix-editor/*.toml` (dark, dark_soft, light, stellar) | Copy to `~/.config/helix/themes/` |
| [Alacritty](https://alacritty.org/) | `terminals/alacritty/` | Import in `~/.config/alacritty/alacritty.toml` |
| [Kitty](https://sw.kovidgoyal.net/kitty/) | `terminals/kitty/` | `include` in `~/.config/kitty/kitty.conf` |
| [iTerm2 / Ghostty / WezTerm](https://github.com/mbadolato/iTerm2-Color-Schemes) | `terminals/iterm2/*.itermcolors` | Import via iTerm2-compatible loader |

## Regenerating terminal files

Terminal color schemes are generated from a single palette dict in `generate.py`:

```
python3 generate.py
```

## License

MIT
