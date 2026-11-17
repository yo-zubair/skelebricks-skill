# Sources and merge decisions

This skill combines two MIT-licensed projects (snapshots taken 2026-11-17):

| Repo | Version | What it contributed |
|------|---------|--------------------|
| [wpgaurav/bricks-skills](https://github.com/wpgaurav/bricks-skills) (commit `aa729a8`) | verified against Bricks 2.3.6 theme source | The backbone: all `references/*.md` except html-conversion.md, all `patterns/`, the workflow, rules and validation approach |
| [iamfilipp/html2bricks](https://github.com/iamfilipp/html2bricks) (h2b v4.0.0) | tested on a live Bricks 2.3.5 site over MCP | HTML→Bricks conversion workflow, tag→element map, JS handling tiers, pseudo-class guidance, native parallax keys, image-gallery load-more, `loadMoreGallery` action, the `%root%` caveat for live writes |

New in this merge: `framework/PROFILE.md` + `framework/tokens.md` (the SkeleBricks framework and build rules), `scripts/validate.py` (tree integrity, both repos' "silent failure" lists, and SkeleBricks checks), `patterns/skelebricks-hero.json`, mode routing in SKILL.md.

## SkeleBricks overrides of upstream defaults

| Topic | Upstream | SkeleBricks |
|-------|----------|-------------|
| Output | save a `.json` file, not inline | one ```json code block, validated first, no file |
| Class custom CSS | literal selector (`.card`) | `%root%` |
| `<div>` mapping | Container / Block / Div by role | Block, except the section's inner wrapper → Container |
| Missing token | raw value + suggest a new variable | snap to nearest existing token; brand changes = value changes to existing variables |
| Styles | class or element | always on BEM global classes; elements carry content only |

## Where the two disagreed

bricks-skills reads the Bricks PHP source directly; h2b tested by writing through an API. When they conflicted, the source-verified shape was kept unless h2b's finding was about a specific write path.

| Topic | h2b said | bricks-skills said | Kept |
|-------|----------|-------------------|------|
| Gradients | `_background.gradient` as a CSS string | `_gradient` with `colors: [{color, stop}]` | bricks-skills |
| Box shadow | flat array of `{offsetX, offsetY, …}` | object with offsets under `values` | bricks-skills (h2b's own example fails this) |
| Gap on layout elements | doesn't work, use `_cssCustom` | `_columnGap` / `_rowGap` on layout elements, `_gap` on others | bricks-skills; h2b was testing the wrong key |
| `_cssCustom` selector | `#brxe-{id}`, `%root%` "does nothing via API" | `%root%` | `%root%` for paste/import (ids are regenerated); `#brxe-{id}` only for live writes where `%root%` is shown not to resolve |
| Border radius | also `_borderRadius` | `_border.radius` only | bricks-skills |
| Pseudo-classes | every pseudo works on every key | only registered pseudo-classes; defaults are hover/active/focus | bricks-skills, with h2b's examples kept as "register first" |
| JS→interactions examples | `toggleClass`, `showElement`, `onShow`, `playAnimation` | `toggleAttribute` (key `class`), `show`, `enterView`, `startAnimation` | bricks-skills; h2b's names don't exist |

Both agreed on: flat tree, 6-char ids, `_typography.text-align` (not `_textAlign`), `_widthMax` naming, `_cssClasses` as a string, `_interactions` over the deprecated `_animation`, element conditions as OR-of-AND arrays.

## Updating from upstream

To pull upstream changes later, diff the upstream repos against this folder. Changes made to upstream files are limited to:
- `references/style-settings.md`: `%root%` vs `#brxe-` note, native parallax section, extra rows in Common Mistakes
- `references/interactions.md`: `loadMoreGallery` row
- `references/elements.md`: image-gallery load-more block
- `references/components-classes.md`: class `_cssCustom` uses `%root%`
- `references/html-conversion.md` is new to this skill (based on h2b): React/Vue/Tailwind step, SkeleBricks tag map and token snapping
- `patterns/INDEX.md`: SkeleBricks note + skelebricks-hero row
