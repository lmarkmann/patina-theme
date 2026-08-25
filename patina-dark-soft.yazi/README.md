# patina-dark-soft

A [Yazi](https://github.com/sxyazi/yazi) flavor from the **Patina** theme,
**Dark Soft** variant.

![preview](./preview.png)

Background `#1a1a1a`, foreground `#c8c4b8`, accent `#4f9073`.

## Install

```sh
ya pkg add lmarkmann/patina-theme:patina-dark-soft
```

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
dark = "patina-dark-soft"
```

Icons need a Nerd Font in your terminal; the flavor sets colours, not glyphs.

## Contents

- `flavor.toml` UI colours (file list, mode, status, tabs, which, help, notify)
- `tmtheme.xml` syntax colours for the file-preview pane

Generated from `palette/patina-dark-soft.toml` in the Patina repo. MIT licensed.
