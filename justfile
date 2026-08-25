# Regenerate every target from palette/*.toml
generate:
    python3 tools/generate.py

# Watch the palette and live-reload the Zed theme while tuning colours
dev:
    watchexec -w palette -e toml -- 'python3 tools/generate.py && cp themes/patina.json ~/.config/zed/themes/'

# Render assets/preview-*.png (local only; needs Input and Nunito installed)
previews:
    uvx --from prev_gen --with 'multimethod<2' python tools/previews.py

# WCAG contrast floors and surface-ramp deltas
contrast:
    python3 tools/contrast.py

# Validate the generated Yazi flavors
check-yazi:
    #!/usr/bin/env bash
    set -euo pipefail
    for f in patina-*.yazi/flavor.toml; do
        crgx taplo-cli check --schema https://yazi-rs.github.io/schemas/theme.json "$f"
    done
    python3 -c "import plistlib,glob; [plistlib.load(open(f,'rb')) for f in glob.glob('patina-*.yazi/tmtheme.xml')]"

# Fail if any generated file is out of date with the palette
verify: generate
    git diff --exit-code -- vscode themes helix-editor terminals contrib 'patina-*.yazi'

# Copy the Zed theme into ~/.config/zed/themes for live testing
test-zed: generate
    cp themes/patina.json ~/.config/zed/themes/

# Copy the Yazi flavors into ~/.config/yazi/flavors for live testing
test-yazi: generate
    mkdir -p ~/.config/yazi/flavors
    cp -R patina-*.yazi ~/.config/yazi/flavors/

# Package the .vsix locally (CI does this on tag push)
package:
    pnpm dlx @vscode/vsce package -o patina-theme.vsix

# Bump the version, commit, tag. Push manually to trigger the release workflows.
release version:
    python3 tools/bump.py {{version}}
    git add package.json extension.toml CHANGELOG.md
    git commit -m "v{{version}}"
    git tag v{{version}}
    @echo "now: git push && git push --tags"
