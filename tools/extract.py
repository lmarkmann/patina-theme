#!/usr/bin/env python3
"""One-shot migration: derive palette/*.toml and tools/keymap.toml from the
hand-maintained vscode/*.json and themes/patina.json.

A token is an equivalence class of theme keys: two keys belong to the same
token when they hold the same colour in all six variants. Keys whose value is
another token's colour plus an alpha suffix become references ("accent/60")
so that retuning the base colour carries the translucent variants with it.

Run once, check that generate.py reproduces the inputs byte for byte, then
delete this file.
"""

import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
VARIANTS = [
    "patina-dark",
    "patina-dark-soft",
    "patina-moss",
    "patina-light",
    "patina-lichen",
    "patina-stellar",
]
ZED_NAMES = [
    "Patina Dark",
    "Patina Dark Soft",
    "Patina Moss",
    "Patina Light",
    "Patina Lichen",
    "Patina Stellar",
]
MISSING = "-"

# Curated names for the classes that carry meaning. Keyed by a member label
# ("surface:key"); the first entry whose label is present wins, so order is
# precedence.
CANON = [
    ("ui:editor.background", "bg"),
    ("ui:sideBar.background", "sidebar"),
    ("ui:editorWidget.background", "widget"),
    ("ui:dropdown.background", "surface"),
    ("ui:input.background", "input"),
    ("ui:editor.lineHighlightBackground", "line_highlight"),
    ("ui:tab.inactiveBackground", "tab_inactive"),
    ("ui:tab.unfocusedHoverBackground", "tab_hover_dim"),
    ("ui:list.hoverBackground", "hover"),
    ("ui:list.activeSelectionBackground", "selected"),
    ("ui:editor.selectionBackground", "selection"),
    ("ui:terminal.selectionBackground", "selection_dim"),
    ("ui:list.inactiveSelectionBackground", "selected_inactive"),
    ("ui:quickInputList.focusBackground", "picker_focus"),
    ("ui:statusBarItem.prominentBackground", "prominent"),
    ("ui:panel.border", "border"),
    ("ui:dropdown.border", "border_strong"),
    ("ui:textBlockQuote.border", "border_quote"),
    ("ui:editorIndentGuide.background", "guide"),
    ("ui:editorIndentGuide.activeBackground", "guide_active"),
    ("ui:focusBorder", "transparent"),
    ("ui:foreground", "fg"),
    ("ui:editorLineNumber.activeForeground", "linenr_active"),
    ("ui:tab.inactiveForeground", "fg_inactive"),
    ("ui:breadcrumb.foreground", "fg_faint"),
    ("ui:editorLineNumber.foreground", "linenr"),
    ("ui:editorGutter.foldingControlForeground", "gutter"),
    ("ui:editorInlayHint.foreground", "inlay"),
    ("ui:gitDecoration.ignoredResourceForeground", "ignored"),
    ("ui:button.background", "accent"),
    ("ui:button.hoverBackground", "accent_hover"),
    ("ui:terminal.ansiRed", "red"),
    ("ui:terminal.ansiYellow", "yellow"),
    ("ui:terminal.ansiBlue", "blue"),
    ("ui:terminal.ansiMagenta", "magenta"),
    ("ui:terminal.ansiCyan", "cyan"),
    ("ui:terminal.ansiBlack", "ansi_black"),
    ("ui:terminal.ansiWhite", "ansi_white"),
    ("ui:editorBracketHighlight.foreground3", "orange"),
    ("ui:editorBracketHighlight.foreground4", "olive"),
    ("ui:editorBracketHighlight.foreground6", "teal"),
    ("ui:editorError.foreground", "error"),
    ("ui:editorWarning.foreground", "warning"),
    ("ui:editorInfo.foreground", "info"),
    ("ui:editorHint.foreground", "hint"),
    # syntax
    ("tc:comment", "comment"),
    ("tc:variable", "variable"),
    ("tc:punctuation", "punctuation"),
    ("tc:keyword.operator", "operator"),
    ("tc:keyword.operator.relational", "operator_relational"),
    ("tc:keyword.operator.quantifier.regexp", "regexp_quantifier"),
    ("tc:variable.parameter", "parameter"),
    ("tc:entity.other.attribute-name", "attribute"),
    ("tc:constant", "constant"),
    ("tc:string variable", "string"),
    ("tc:string", "string_plain"),
    ("tc:punctuation.definition.string", "string_punctuation"),
    ("tc:punctuation.support.type.property-name", "parameter_punctuation"),
    # zed-only
    ("zed:element.hover", "element_hover"),
    ("zed:element.selected", "element_selected"),
    ("zed:element.active", "element_active"),
    ("zed:conflict", "conflict"),
    ("zed:drop_target.background", "accent_wash"),
    ("zed:terminal.ansi.dim_black", "dim_black"),
    ("zed:terminal.ansi.dim_red", "dim_red"),
    ("zed:terminal.ansi.dim_green", "dim_green"),
    ("zed:terminal.ansi.dim_yellow", "dim_yellow"),
    ("zed:terminal.ansi.dim_blue", "dim_blue"),
    ("zed:terminal.ansi.dim_magenta", "dim_magenta"),
    ("zed:terminal.ansi.dim_cyan", "dim_cyan"),
    ("zed:terminal.ansi.dim_white", "dim_white"),
    ("accent:1", "olive_bright"),
]

SECTIONS = [
    ("ground", ["bg", "sidebar", "widget", "surface", "input", "line_highlight",
                "tab_inactive", "tab_hover_dim", "hover", "selected", "selection",
                "selection_dim", "selected_inactive", "picker_focus", "prominent",
                "border", "border_strong", "border_quote", "guide", "guide_active",
                "transparent"]),
    ("ink", ["fg", "linenr_active", "fg_inactive", "fg_faint", "linenr", "gutter",
             "inlay", "ignored"]),
    ("accent", ["accent", "accent_hover", "red", "yellow", "blue", "magenta",
                "cyan", "orange", "olive", "olive_bright", "teal", "conflict",
                "ansi_black", "ansi_white"]),
    ("syntax", ["comment", "variable", "punctuation", "operator",
                "operator_relational", "parameter", "attribute", "constant",
                "string", "string_plain", "regexp_quantifier"]),
    ("status", ["error", "warning", "info", "hint"]),
    ("zed", ["element_hover", "element_selected", "element_active",
             "dim_black", "dim_red", "dim_green", "dim_yellow", "dim_blue",
             "dim_magenta", "dim_cyan", "dim_white"]),
]


# Helix predates the 1.3.0 syntax retune, so a dozen of its slots no longer
# resolve against the current palette. These are pinned to the token the VS
# Code theme uses for the equivalent scope, which is the released surface.
HELIX_OVERRIDES = {
    ("string", 0): "string",
    ("string.special", 0): "constant",
    ("constant", 0): "constant",
    ("constant.character", 0): "string",
    ("constant.builtin", 0): "constant",
    ("constant.builtin.boolean", 0): "constant",
    ("label", 0): "string",
    ("markup.link.text", 0): "string",
    ("warning", 0): "yellow",
    ("diagnostic.warning", 0): "yellow",
    ("ui.menu.selected", 0): "fg",
    ("ui.menu.selected", 1): "selected",
    ("ui.selection.primary", 0): "selection",
    ("ui.bufferline", 0): "fg_inactive",
    ("ui.bufferline", 1): "tab_inactive",
    ("ui.statusline.inactive", 0): "fg_inactive",
    ("ui.statusline.inactive", 1): "tab_inactive",
    ("ui.statusline.insert", 1): "magenta",
}
HELIX_TRUST = ["patina-light", "patina-lichen", "patina-dark"]


def emit_helix(km, values):
    """Turn helix-editor/patina_light.toml into a token template. Each colour
    is resolved by intersecting the tokens that match it in the three variants
    whose Helix files still agree with the palette."""
    import re

    src = {
        v: (BASE / "helix-editor" / f"{v.replace('-', '_')}.toml").read_text().splitlines()
        for v in HELIX_TRUST
    }
    km.append("# Helix theme as a token template; %token% is substituted per variant.")
    km.append("[helix]")
    templates, unresolved = [], []
    for i, line in enumerate(src["patina-light"]):
        hexes = {v: re.findall(r"#[0-9a-fA-F]{6}", src[v][i]) for v in HELIX_TRUST}
        key_m = re.match(r'"([^"]+)"', line.strip())
        key = key_m.group(1) if key_m else ""
        out, pos = line, 0
        for j in range(len(hexes["patina-light"])):
            token = HELIX_OVERRIDES.get((key, j))
            if token is None:
                cands = None
                for v in HELIX_TRUST:
                    c = {t for t, x in values[v].items() if x == hexes[v][j].lower()}
                    cands = c if cands is None else (cands & c)
                if len(cands) == 1:
                    token = next(iter(cands))
                else:
                    unresolved.append((key, j, sorted(cands)))
                    token = "fg"
            out = out.replace(hexes["patina-light"][j], f"%{token}%", 1)
        templates.append(out)
    km.append("template = [")
    for t in templates:
        km.append(f"  {json.dumps(t)},")
    km.append("]")
    km.append("")
    if unresolved:
        print(f"  helix: {len(unresolved)} unresolved slots {unresolved[:5]}")


# The Yazi flavor was written by hand against Dark Soft. One variant cannot
# disambiguate tokens that happen to share a value, so each colour is pinned
# explicitly. The two files need different maps: the same hex is a surface in
# the flavor and a syntax colour in the tmtheme.
YAZI_SOURCE = Path.home() / "Documents/THEMES/patina-dark-soft.yazi"
YAZI_FLAVOR_MAP = {
    "#1a1a1a": "bg", "#1e1e1e": "tab_inactive", "#222222": "surface",
    "#3d3d3d": "border_strong", "#4a4a4a": "fg_inactive", "#4a8a6e": "accent",
    "#4e4e4e": "fg_faint", "#5a9e9c": "cyan", "#65a8b5": "blue",
    "#778073": "hint", "#93b072": "olive", "#af8d62": "orange",
    "#b86e6e": "red", "#c08a7d": "magenta", "#c8c4b8": "fg",
    "#d05060": "error", "#d4bf6e": "yellow",
}
YAZI_TMTHEME_MAP = {
    "#1a1a1a": "bg", "#222222": "surface", "#333333": "guide",
    "#4a8a6e": "accent", "#4a8f87": "teal", "#4e4e4e": "fg_faint",
    "#5a9e9c": "cyan", "#778073": "comment", "#787878": "punctuation",
    "#8d8a82": "operator", "#93b072": "olive", "#ad9e5e": "parameter",
    "#af8d62": "attribute", "#b3a489": "variable", "#b86e6e": "red",
    "#b88068": "constant", "#c48b76": "string", "#c8c4b8": "fg",
    "#d05060": "error",
}


def emit_yazi(km):
    import re

    for field, fname, cmap in (
        ("flavor", "flavor.toml", YAZI_FLAVOR_MAP),
        ("tmtheme", "tmtheme.xml", YAZI_TMTHEME_MAP),
    ):
        text = (YAZI_SOURCE / fname).read_text()
        text = text.replace("Patina Dark Soft", "%NAME%")
        text = text.replace("Dark Soft variant", "%SHORT% variant")
        missing = set()

        def sub(m):
            token = cmap.get(m.group(0).lower())
            if token is None:
                missing.add(m.group(0))
                return m.group(0)
            return f"%{token}%"

        text = re.sub(r"#[0-9a-fA-F]{6}", sub, text)
        if missing:
            print(f"  yazi {fname}: unmapped {sorted(missing)}")
        km.append(f"[yazi]" if field == "flavor" else "")
        km.append(f"{field} = [")
        for line in text.splitlines():
            km.append(f"  {json.dumps(line)},")
        km.append("]")
        km.append("")


def norm(v):
    return v.lower() if isinstance(v, str) else MISSING


def snake(key):
    s = re.sub(r"[.\-]", "_", key)
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()
    return re.sub(r"_+", "_", s)


def main():
    vs = {v: json.loads((BASE / "vscode" / f"{v}.json").read_text()) for v in VARIANTS}
    zed = json.loads((BASE / "themes" / "patina.json").read_text())
    zstyle = {t["name"]: t["style"] for t in zed["themes"]}

    # signature -> list of (surface, key) members
    members = defaultdict(list)

    ui_order = list(vs["patina-dark"]["colors"])
    for k in ui_order:
        sig = tuple(norm(vs[v]["colors"].get(k, MISSING)) for v in VARIANTS)
        members[sig].append(f"ui:{k}")

    tc_ref = vs["patina-dark"]["tokenColors"]
    for i, rule in enumerate(tc_ref):
        scope = rule["scope"]
        label = rule.get("name") or (scope[0] if isinstance(scope, list) else scope)
        for field in ("foreground", "background"):
            sig = tuple(
                norm(vs[v]["tokenColors"][i]["settings"].get(field, MISSING))
                for v in VARIANTS
            )
            if set(sig) == {MISSING}:
                continue
            prefix = "tc" if field == "foreground" else "tcbg"
            members[sig].append(f"{prefix}:{label}")

    for k in vs["patina-dark"]["semanticTokenColors"]:
        sig = tuple(norm(vs[v]["semanticTokenColors"].get(k, MISSING)) for v in VARIANTS)
        members[sig].append(f"sem:{k}")

    zscalar = [
        k for k in zstyle[ZED_NAMES[0]]
        if all(isinstance(zstyle[n].get(k), (str, type(None))) for n in ZED_NAMES)
    ]
    for k in zscalar:
        sig = tuple(norm(zstyle[n].get(k, MISSING)) for n in ZED_NAMES)
        members[sig].append(f"zed:{k}")

    for n_i, name in enumerate(ZED_NAMES[:1]):
        for i, p in enumerate(zstyle[name]["players"]):
            for field in p:
                sig = tuple(norm(zstyle[n]["players"][i][field]) for n in ZED_NAMES)
                members[sig].append(f"player{i}:{field}")
        for i in range(len(zstyle[name]["accents"])):
            sig = tuple(norm(zstyle[n]["accents"][i]) for n in ZED_NAMES)
            members[sig].append(f"accent:{i}")
        for scope, spec in zstyle[name]["syntax"].items():
            if spec.get("color") is None:
                continue
            sig = tuple(norm(zstyle[n]["syntax"][scope]["color"]) for n in ZED_NAMES)
            members[sig].append(f"zsyn:{scope}")

    # name every class
    names, used = {}, set()
    for canon_label, canon_name in CANON:
        for sig, mem in members.items():
            if sig in names or canon_label not in mem:
                continue
            names[sig] = canon_name
            used.add(canon_name)
            break
    rank = {"ui": 0, "zed": 1, "sem": 2, "tc": 3, "tcbg": 4, "zsyn": 5}
    for sig, mem in sorted(members.items(), key=lambda kv: -len(kv[1])):
        if sig in names:
            continue
        if all(m.startswith("player") for m in mem):
            cand = f"player_{mem[0].split(':')[0][6:]}_wash"
        else:
            best = min(mem, key=lambda m: (rank.get(m.split(":")[0], 9), len(m)))
            cand = snake(best.split(":", 1)[1])
        n, i = cand, 2
        while n in used:
            n, i = f"{cand}_{i}", i + 1
        names[sig] = n
        used.add(n)

    # fold alpha classes onto their base
    by_sig = {s: names[s] for s in members}
    base_lookup = {}
    for sig, name in by_sig.items():
        if all(len(x) == 7 or x == MISSING for x in sig):
            base_lookup[tuple(x[:7] for x in sig)] = name

    refs = {}
    for sig, name in by_sig.items():
        if not any(len(x) == 9 for x in sig):
            continue
        base = tuple(x[:7] for x in sig)
        target = base_lookup.get(base)
        if target and target != name:
            refs[name] = (target, [x[7:] if len(x) == 9 else "" for x in sig])

    # emit palette/<variant>.toml
    order = []
    for _, group in SECTIONS:
        order.extend(group)
    rest = sorted(n for n in by_sig.values() if n not in order and n not in refs)
    ref_names = sorted(refs)

    for vi, variant in enumerate(VARIANTS):
        lines = [
            f'name = "{vs[variant]["name"]}"',
            f'base = "{vs[variant]["base"]}"',
            "",
        ]
        emitted = set()
        for section, group in SECTIONS:
            body = []
            for n in group:
                sig = next((s for s, nm in by_sig.items() if nm == n), None)
                if sig is None or sig[vi] == MISSING or n in refs:
                    continue
                body.append(f'{n} = "{sig[vi]}"')
                emitted.add(n)
            if body:
                lines.append(f"[{section}]")
                lines.extend(body)
                lines.append("")
        body = []
        for n in rest:
            if n in emitted:
                continue
            sig = next(s for s, nm in by_sig.items() if nm == n)
            if sig[vi] == MISSING:
                continue
            body.append(f'{n} = "{sig[vi]}"')
        if body:
            lines.append("[extra]")
            lines.extend(body)
            lines.append("")
        body = []
        for n in ref_names:
            target, alphas = refs[n]
            sig = next(s for s, nm in by_sig.items() if nm == n)
            if sig[vi] == MISSING:
                continue
            body.append(f'{n} = "{target}/{alphas[vi]}"')
        if body:
            lines.append("[alpha]")
            lines.extend(body)
            lines.append("")
        (BASE / "palette" / f"{variant}.toml").write_text("\n".join(lines).lstrip("\n"))

    # emit tools/keymap.toml
    km = ["# Generated by extract.py. Maps every theme key to a palette token.",
          "# Edit when a target gains or loses a key, not when a colour changes.", ""]
    km.append("[vscode.colors]")
    for k in ui_order:
        sig = tuple(norm(vs[v]["colors"].get(k, MISSING)) for v in VARIANTS)
        km.append(f'"{k}" = "{by_sig[sig]}"')
    km.append("")
    for i, rule in enumerate(tc_ref):
        km.append("[[vscode.tokenColors]]")
        km.append(f"scope = {json.dumps(rule['scope'])}")
        km.append(f"settings_order = {json.dumps(list(rule['settings']))}")
        for field in ("foreground", "background"):
            sig = tuple(
                norm(vs[v]["tokenColors"][i]["settings"].get(field, MISSING))
                for v in VARIANTS
            )
            if set(sig) != {MISSING}:
                km.append(f'{field} = "{by_sig[sig]}"')
        if "fontStyle" in rule["settings"]:
            km.append(f'fontStyle = {json.dumps(rule["settings"]["fontStyle"])}')
        km.append("")
    km.append("[vscode.semanticTokenColors]")
    for k in vs["patina-dark"]["semanticTokenColors"]:
        sig = tuple(norm(vs[v]["semanticTokenColors"].get(k, MISSING)) for v in VARIANTS)
        km.append(f'"{k}" = "{by_sig[sig]}"')
    km.append("")
    km.append("[zed]")
    zorder = list(zstyle[ZED_NAMES[0]])
    km.append("order = [")
    for k in zorder:
        km.append(f'  "{k}",')
    km.append("]")
    km.append("")
    km.append("[zed.style]")
    for k in zscalar:
        sig = tuple(norm(zstyle[n].get(k, MISSING)) for n in ZED_NAMES)
        km.append(f'"{k}" = "{by_sig[sig]}"')
    km.append("")
    km.append("[zed.accents]")
    acc = []
    for i in range(len(zstyle[ZED_NAMES[0]]["accents"])):
        sig = tuple(norm(zstyle[n]["accents"][i]) for n in ZED_NAMES)
        acc.append(by_sig[sig])
    km.append(f"tokens = {json.dumps(acc)}")
    km.append("")
    for i, p in enumerate(zstyle[ZED_NAMES[0]]["players"]):
        km.append("[[zed.players]]")
        for field in p:
            sig = tuple(norm(zstyle[n]["players"][i][field]) for n in ZED_NAMES)
            km.append(f'{field} = "{by_sig[sig]}"')
        km.append("")
    for scope, spec in zstyle[ZED_NAMES[0]]["syntax"].items():
        km.append(f'[zed.syntax."{scope}"]')
        present = [f for f in spec if spec[f] is not None or f == "color"]
        km.append(f"order = {json.dumps(present)}")
        if spec.get("color") is not None:
            sig = tuple(norm(zstyle[n]["syntax"][scope]["color"]) for n in ZED_NAMES)
            km.append(f'color = "{by_sig[sig]}"')
        for field in ("font_style", "font_weight"):
            if field in spec:
                km.append(f"{field} = {json.dumps(spec[field])}")
        km.append("")
    values = {}
    for vi, variant in enumerate(VARIANTS):
        values[variant] = {
            name: (sig[vi] if not any(len(x) == 9 for x in sig) else sig[vi])
            for sig, name in by_sig.items()
            if sig[vi] != MISSING
        }
        values[variant] = {n: v for n, v in values[variant].items() if len(v) == 7}
    emit_helix(km, values)
    emit_yazi(km)

    (BASE / "tools" / "keymap.toml").write_text("\n".join(km))

    print(f"classes: {len(members)}  named: {len(set(by_sig.values()))}  alpha refs: {len(refs)}")
    print(f"wrote palette/*.toml ({len(VARIANTS)}) and tools/keymap.toml")


if __name__ == "__main__":
    main()
