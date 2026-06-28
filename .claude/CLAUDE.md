# Patina Theme

Warm, muted color theme with earthy tones. Six variants: Dark, Dark Soft (daily driver), Moss, Light, Lichen, Stellar.

## Release surfaces (exhaustive)

Only these four targets are officially released and maintained. Do not add new targets without explicit approval; keeping the surface small protects time for actual theme design.

| # | Surface | Format | Distribution |
|---|---------|--------|--------------|
| 1 | **VS Code Marketplace** | `.vsix` from `package.json` + `vscode/*.json` | GitHub Actions on `v*` tag; secret `VSCE_PAT` |
| 2 | **Open VSX Registry** (Cursor, VSCodium, Gitpod, Theia, etc.) | Same `.vsix` | GitHub Actions on `v*` tag; secret `OVSX_PAT` |
| 3 | **Ghostty** | Key-value config files in `terminals/ghostty/` | Manual install / upstream contrib |
| 4 | **Zed** | JSON theme in `themes/patina.json` + `extension.toml` at repo root | Zed extension registry (`zed-industries/extensions`) on tag bumps |

Everything else in the repo (Helix, and the iTerm2 schemes under `contrib/`) is community or upstream contribution work, not a release we own. `generate.py` produces the Ghostty configs and the `contrib/iterm2-color-schemes/` files from the palette definitions; Helix and VS Code themes are maintained by hand.

## Decided against (do not re-propose)

These have been considered and rejected to keep maintenance low:

- **More editor/terminal targets** beyond the four above
- **CONTRIBUTING.md / CODE_OF_CONDUCT.md** governance scaffolding
- **NPM palette package** or separate color repo
- **CI beyond publish** (linting, validation workflows)
- **Theme customization API** (settings.json overrides, contrast toggles)

If a user requests a port, point them to `generate.py` palettes as the source of truth; don't add a release target.

## Quality bar for releases

- **README**: badge row (version, installs, license), one screenshot per variant showing real code, palette swatch table with hex values
- **Marketplace description**: keyword-rich (warm, muted, earthy, dark, light, oxidized, teal, amber); repeat key terms across README and `package.json` keywords
- **Screenshots**: `assets/` should have one per variant; use Python or Rust source for consistency
- **Palette source of truth**: `generate.py` PALETTES dict. When changing a color, change it there first, then propagate to VS Code JSON, Zed JSON, and Ghostty output

## GitHub secrets

Both publishing tokens live in 1Password and are mirrored as GitHub repo secrets for CI:

- `VSCE_PAT` — Azure DevOps PAT with Marketplace > Manage scope
- `OVSX_PAT` — Open VSX access token

To publish manually outside CI, inject via `op read` inline; never print or assign tokens to visible variables.

## Publisher names (do not "normalize")

The two registries use different publisher IDs for historical reasons:

- **VS Code Marketplace**: `LuisCMarkmann.patina-theme` (mixed case; original publisher from v0.9.0)
- **Open VSX Registry**: `lmarkmann.patina-theme` (lowercase; namespace created later)

`package.json` holds `"publisher": "lmarkmann"` because `ovsx publish` has no namespace override flag and consumes whatever's in the .vsix. The VS Code workflow `sed`-patches the publisher to `LuisCMarkmann` before packaging. Do not change `package.json` to `LuisCMarkmann` — it would break Open VSX. Do not try to rename either publisher; Marketplace doesn't allow renames and the existing `LuisCMarkmann` listing carries the install history.

## Build and release

```bash
python3 generate.py          # regenerate terminal themes from palettes
pnpm dlx @vscode/vsce package -o patina-theme.vsix   # package for both registries
```

Tag-push workflow: bump version in `package.json` and `CHANGELOG.md`, commit, `git tag v<version>`, push with `--tags`. Both CI workflows trigger on `v*` tags and also support `workflow_dispatch`.

## Variants

- **Dark Soft**: daily driver, start here when editing themes
- **Dark**: higher contrast alternative
- **Moss**: dark, moss-tinted ground
- **Light**: warm light theme
- **Lichen**: light, cool grey-green stone
- **Stellar**: brightest light variant

## Theme calibration notes

### Lightness deltas as a calibration probe

A hover state needs at least +6 L-points of delta from its surface at low luminance (Weber-Fechner: dark surfaces need larger absolute differences). One Dark Pro uses +6.5 at L=13; Gruvbox Light uses -5.5 at L=82. Current deltas: Dark +7.8, Dark Soft +6.5, Light -6.1, Stellar -8.6. Each variant steps cleanly: hover < selected < active, ~4-5 L-points apart. Stellar needs the strongest delta because its `elevated_surface.background` equals its `background`, so popup rows need more contrast to feel like "rows" at all.

### Ghost element rules (Zed)

Picker rows are ghost elements; they should be transparent at rest (`#00000000`) and only paint on hover/active/selected. Setting `ghost_element.background` to the editor background creates a collision when that background happens to equal `elevated_surface.background` (as it did in Dark Soft), resulting in zero delta and no visible hover.

`ghost_element.hover/active/selected` should mirror their `element.*` counterparts (One Dark's canonical pattern). Do not tie them to `elevated_surface`, which is the colliding surface itself.

### Element state stepping

`element.hover`, `element.selected`, and `element.active` must all be distinct values. Collapsing any two states removes visual emphasis when both states apply simultaneously (e.g. a keyboard-selected row that the mouse hovers over). The hierarchy should step cleanly: hover < selected < active.

### Schema parity

Every status group (error, warning, info, success, …) should have the full triple of `background`, `border`, and `text`. If one is missing, add it. `unreachable` was the only group missing `background` and `border`; it now has both.

## Project structure

```
vscode/             VS Code theme JSON files (6 variants, hand-maintained)
terminals/ghostty/  Ghostty config files (generated by generate.py)
themes/             Zed theme JSON (hand-maintained; required at repo root for Zed extension registry)
extension.toml      Zed extension manifest (required at repo root)
helix-editor/       Helix TOML themes (community, not a release target)
contrib/iterm2-color-schemes/  iTerm2 schemes, Title Case (generated; mirrors upstream iTerm2-Color-Schemes)
assets/             icon.png + preview-*.png (README/marketplace); palette-*/strip-*.png are generate_previews.py output
docs/               GitHub Pages landing page (index.html)
.github/workflows/  CI for VS Code Marketplace + Open VSX publishing
generate.py         Palette definitions + Ghostty/iTerm2 generator
generate_previews.py  Renders assets/preview-*.png from the vscode/ themes
```
