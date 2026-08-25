# patina-lichen

A [Yazi](https://github.com/sxyazi/yazi) flavor from the **Patina** theme,
**Lichen** variant.

![preview](./preview.png)

Background `#cdd1c6`, foreground `#393a34`, accent `#33644d`.

## Install

```sh
ya pkg add lmarkmann/patina-theme:patina-lichen
```

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
light = "patina-lichen"
```

Icons need a Nerd Font in your terminal; the flavor sets colours, not glyphs.

## Contents

- `flavor.toml` UI colours (file list, mode, status, tabs, which, help, notify)
- `tmtheme.xml` syntax colours for the file-preview pane

Generated from `palette/patina-lichen.toml` in the Patina repo. MIT licensed.
