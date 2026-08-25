# patina-light

A [Yazi](https://github.com/sxyazi/yazi) flavor from the **Patina** theme,
**Light** variant.

![preview](./preview.png)

Background `#ddd7c4`, foreground `#393a34`, accent `#33644d`.

## Install

```sh
ya pkg add lmarkmann/patina-theme:patina-light
```

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
light = "patina-light"
```

Icons need a Nerd Font in your terminal; the flavor sets colours, not glyphs.

## Contents

- `flavor.toml` UI colours (file list, mode, status, tabs, which, help, notify)
- `tmtheme.xml` syntax colours for the file-preview pane

Generated from `palette/patina-light.toml` in the Patina repo. MIT licensed.
