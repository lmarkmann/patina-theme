# patina-dark

A [Yazi](https://github.com/sxyazi/yazi) flavor from the **Patina** theme,
**Dark** variant.

![preview](./preview.png)

Background `#121212`, foreground `#dbd7ca`, accent `#4d9375`.

## Install

```sh
ya pkg add lmarkmann/patina-theme:patina-dark
```

Then in `~/.config/yazi/theme.toml`:

```toml
[flavor]
dark = "patina-dark"
```

Icons need a Nerd Font in your terminal; the flavor sets colours, not glyphs.

## Contents

- `flavor.toml` UI colours (file list, mode, status, tabs, which, help, notify)
- `tmtheme.xml` syntax colours for the file-preview pane

Generated from `palette/patina-dark.toml` in the Patina repo. MIT licensed.
