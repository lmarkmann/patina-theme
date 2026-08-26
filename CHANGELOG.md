# Changelog

## 1.4.0

- **Colours now live in `palette/*.toml`**, one file per variant, and every theme file is generated from them by `tools/generate.py`. Previously `generate.py`'s `PALETTES` dict was documented as the source of truth but had not been updated since 1.2.2, so three targets shipped colours from before the 1.3.0 retune.
- **Fix Ghostty, iTerm2 and Helix**, which were emitting pre-1.3.0 colours. Dark Soft's Ghostty ANSI 0 was `#2e2e2e` against `#333333` in VS Code and Zed; Helix's `ui.text` was `#dbd7ca` against `#c8c4b8`. The terminal targets now read their ANSI slots through the same mapping VS Code uses, so they cannot diverge again. VS Code and Zed are unchanged: both regenerate byte for byte.
- **Add Yazi flavors** for all six variants, installable with `ya pkg add lmarkmann/patina-theme:patina-dark-soft`. This replaces the standalone `patina-dark-soft.yazi` repo, which carried only one variant.
- Re-render the previews in [Input](https://input.djr.com/), with a Rust sample that exercises eight syntax colours instead of five.
- Re-enable the Zed publish workflow on tags now that [zed-industries/extensions#6470](https://github.com/zed-industries/extensions/pull/6470) has merged.
- Add a CI check that regenerates every target and fails if anything drifts from the palette.

### Colour corrections

- **Sidebar hierarchy.** Zed's project panel draws ordinary entries in `text.muted` and git-status entries in their status colours. `text.muted` resolved to a token sitting at 1.75-2.39:1 against the panel, while `ignored` sat at 2.88-3.54, so tracked files rendered dimmer than ignored and untracked ones. The muted ink is split in two: `fg_muted` at 4.5:1 for text that is read, `fg_inactive` at 3.0:1 for disabled and placeholder. `ignored` drops to 2.2:1 so ignored paths recede by about 2x rather than 1.3x.
- **Rebuild Patina Lichen.** It reused Light's accent values on a darker ground, leaving every role about 0.35 below its Light counterpart, and ten roles had collapsed into greys or onto their neighbours: `string`, `string_plain`, `operator`, `operator_relational`, `regexp_quantifier`, `attribute`, `variable`, `olive`, `conflict` and `hint`. Strings and operators were the same colour. The ground moves `#cdd1c6` to `#d5dace` and every chromatic role now takes Light's hue and chroma with lightness solved for Lichen's own ground.
- **Retune yellow in the three light variants.** It was the one role never brought into the 1.3.0 retune, sitting at 1.6-2.2:1 where every sibling accent was tuned to roughly 4.75:1. It now clears 3.8:1.
- **Picker ramp parity.** Hover is now 5 L\* from its surface, selected 9.5, active 14, in every variant except Dark, which keeps a wider spread. Moss was at 2.5 L\* and Light at 2.9, the same imperceptible hover fixed in 1.2.2. `quickInputList.focusBackground` is reclassified as a selection rather than a hover.
- **Error salience.** An error must be at least as visible as ordinary red; Moss's was dimmer than its own red (3.78 against 4.69).
- **Punctuation at AA.** `punctuation` and `operator_relational` sat at 3.94:1 in Dark Soft and Moss against 4.7-4.8 in the light variants.
- **Dark Soft's primary accent** was 4.27:1, the dimmest colour in its own variant, while carrying buttons, links and the activity-bar indicator. Now 4.62.
- `tools/contrast.py` gates all of the above: WCAG floors, the surface-ramp deltas, and the panel hierarchy.

## 1.3.1

- README: remove the duplicate hero preview and arrange the six variant previews as a named three-column grid.
- Project page: add a favicon, remove the duplicate hero, and label each variant preview.

## 1.3.0

- Add two new variants, bringing the family to six: **Patina Moss** (dark, moss-tinted ground `#20231f`) and **Patina Lichen** (light, cool grey-green stone ground `#cdd1c6`).
- Retune all four original variants (**Dark Soft**, **Dark**, **Light**, **Stellar**) to reduce long-session eye fatigue (color-interaction fixes grounded in Albers/Itten and OKLCH measurement). The two light variants were the worst offenders: every accent had been tuned to a single contrast ratio, which on a fixed ground forced them all to one luminance (accent lightness span 0.02), so adjacent tokens were separated by hue alone. The same six moves applied to every variant:
  - Demote `operator`, `keyword.operator`, and `punctuation.special` from red to a warm grey; red is now reserved for control flow, exceptions, and escapes (Itten contrast-of-extension).
  - Move `function` in lightness so it separates from `keyword` by value, not just hue.
  - Cut `comment` chroma so comments recede instead of competing in the green cluster.
  - Calm `variable` toward neutral to quiet the highest-frequency colored token.
  - Separate `string` from `constant` by value; merge `boolean` into `constant`.
  - Net effect on the light variants: accent lightness span widened from 0.02 to 0.07.
- Regenerate Ghostty and iTerm2 terminal palettes for all six variants.

## 1.2.2

- Fix invisible hover and selection states across Zed and VS Code/Cursor pickers, lists, menus, and autocomplete.
- Zed: set `ghost_element.background` transparent and mirror `ghost_element.hover/active/selected` to their `element.*` counterparts (canonical Zed pattern); separate `element.hover` from `element.selected` so hover, selected, and active step distinctly. Add missing `unreachable.background` and `unreachable.border`.
- VS Code: recalibrate `list.*` hover/selection backgrounds and `tab.hoverBackground` / `tab.unfocusedHoverBackground` so they no longer collide with their surrounding surface.
- VS Code: add 25 missing keys per variant covering `editorSuggestWidget.*`, `editorHoverWidget.*`, `menu.*`, `menubar.*`, `peekViewResult.selection*`, `commandCenter.*`, `statusBarItem.hoverBackground/activeBackground`, plus `list.focusForeground`, `tab.hoverForeground`, `tab.unfocusedHoverForeground`, and `quickInputList.focusForeground`.

## 1.2.1

- Fix VS Code Marketplace publish: workflow now patches `package.json` publisher to `LuisCMarkmann` (Marketplace ID) before packaging, while Open VSX continues to use `lmarkmann` (its namespace).

## 1.2.0

- Narrow official release scope to four surfaces: VS Code Marketplace, Open VSX, Ghostty, and Zed.
- Add GitHub Actions workflows for automated publishing to VS Code Marketplace (`VSCE_PAT`) and Open VSX (`OVSX_PAT`) on `v*` tags.
- Add Zed editor theme (`zed/patina.json`) covering all four variants.
- Add Ghostty terminal config files (`terminals/ghostty/`) generated from the canonical palette.
- Remove Alacritty, Kitty, iTerm2, and WezTerm terminal configs from the maintained set.
- README rewritten to reflect the four-surface scope.

## 1.1.0

- Fix WCAG AA contrast failures in Patina Light and Patina Stellar; all syntax tokens now meet 4.5:1 except `markup.ignored` (intentionally near-background).
- Add Helix themes for Patina Light and Patina Stellar (previously dark variants only).
- Darken ANSI palette for Patina Light and Patina Stellar terminal configs so colored text passes 4.5:1 on the parchment background.
- Trim `.vscodeignore` so the published VSIX no longer bundles terminal, Helix, or generator sources.

## 1.0.0

- Make UI borders more explicit across all variants.

## 0.9.0

- Initial release: Patina Dark, Dark Soft, Light, Stellar for VS Code plus ports for Helix and common terminals.
