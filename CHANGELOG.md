# Changelog

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
