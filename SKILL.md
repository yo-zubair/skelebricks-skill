---
name: skelebricks-skill
description: The SkeleBricks skill for Bricks Builder (WordPress). Builds Bricks sections, pages and templates as paste-ready clipboard JSON, and converts HTML/CSS/JS, React, Vue or Tailwind into native Bricks elements, always using the SkeleBricks CSS framework (fixed Style Manager variables, BEM global classes, 1rem = 10px). Use for any Bricks task on a SkeleBricks site: sections, pages, headers/footers, HTML-to-Bricks conversion, global classes, query loops, ACF/dynamic data, filters, conditions, interactions, popups, forms, WooCommerce, custom elements or hooks.
---

# SkeleBricks Skill

Build Bricks designs as JSON that pastes onto the canvas cleanly the first time, styled with the SkeleBricks framework.

Combined from two open-source skills (details in SOURCES.md): **bricks-skills** (source-verified shapes, references, patterns) and **html2bricks** (HTML→Bricks conversion), with the SkeleBricks framework and rules on top.

## Step 0: load the framework

**Read [framework/PROFILE.md](framework/PROFILE.md) and [framework/tokens.md](framework/tokens.md) before writing any JSON.** They override every default in this file and in references/.

## Pick the mode

| Input | Mode | Start with |
|-------|------|-----------|
| Brief, idea, screenshot, Figma description, reference URL | **Author** | layout-recipes.md, patterns/ for structure only |
| HTML / CSS / JS | **Convert** | [references/html-conversion.md](references/html-conversion.md) |
| React, Vue, Svelte, JSX, Tailwind | **Convert**, after resolving to plain HTML + CSS first | html-conversion.md §0 |
| JSON that doesn't paste or renders wrong | **Fix** | `scripts/validate.py`, then style-settings.md |
| A live site connected over MCP (Bricks abilities) | **Live** | the installed `bricks-*` skills handle the write path; SkeleBricks still decides tokens, classes, labels |

## Workflow

1. **Clarify** only what the input and profile don't answer (which content is real vs placeholder; a reference URL to fetch for assets).
2. **Plan the structure**: one Section per band, labelled by purpose (`Hero`, `Features`, `CTA`…), `section → container → blocks`. Pick elements from [elements.md](references/elements.md).
3. **Name the BEM classes** for every styled element: `.hero`, `.hero__container`, `.hero__kicker`, `.hero__heading`, `.hero__img`. The Container element's class is always `{block}__container`, never `__inner`.
4. **Style the classes** with native UI-control settings using exact shapes from [style-settings.md](references/style-settings.md), values snapped to SkeleBricks tokens. Anything without a control → the class's `_cssCustom` with `%root%`, formatted one declaration per line (PROFILE.md §4a).
5. **Wire data**: dynamic tags, loops, filters, conditions, interactions (routing table).
6. **Validate**: write the JSON to a scratchpad temp file, run `python3 scripts/validate.py <file>`, fix until it prints `OK` and no `_cssCustom` formatting warnings remain.
7. **Deliver**: the complete JSON in **one single ```json code block**, nothing else inside it. After the block: Style Manager value changes (if the brand needs different colours), fallbacks used, anything approximated.

## Format

Clipboard format, always:

```json
{
  "content": [ /* flat array of element nodes */ ],
  "source": "bricksCopiedElements",
  "sourceUrl": "https://example.com",
  "version": "2.3.6",
  "globalClasses": [ /* full object for every id used in _cssGlobalClasses */ ],
  "globalElements": []
}
```

Element: `{ "id": "hro001", "name": "section", "parent": 0, "children": ["hrc001"], "settings": { "tag": "section", "_cssGlobalClasses": ["clhero"] }, "label": "Hero" }`

Class: `{ "id": "clhero", "name": "hero", "settings": { "_padding": { "top": "var(--space-3xl)", "bottom": "var(--space-3xl)" }, "_background": { "color": { "raw": "var(--bg-body)" } } } }`

- Ids are unique 6-char lowercase alphanumeric. `parent` is `0` at the root. Hierarchy lives only in `parent` + `children`, and both sides must agree.

## Task routing

| Task | Reference |
|------|-----------|
| **Framework rules: styling, BEM, labels, delivery** | [framework/PROFILE.md](framework/PROFILE.md) |
| **Variables (closed list) and snapping table** | [framework/tokens.md](framework/tokens.md) |
| **Converting HTML / React / Vue / Tailwind** | [references/html-conversion.md](references/html-conversion.md) |
| Clipboard / template / postmeta formats | [references/json-formats.md](references/json-formats.md) |
| Element catalog, per-element settings, nestables | [references/elements.md](references/elements.md) |
| Style keys and value shapes, responsive + pseudo grammar, parallax | [references/style-settings.md](references/style-settings.md) |
| Section, grid, card, hero, sticky, overlap recipes | [references/layout-recipes.md](references/layout-recipes.md) |
| Global classes, components | [references/components-classes.md](references/components-classes.md) |
| Theme styles, breakpoints, CSS generation order | [references/theme-styles.md](references/theme-styles.md) |
| Dynamic data tags | [references/dynamic-data.md](references/dynamic-data.md) |
| ACF, Meta Box, JetEngine, Pods, CMB2 | [references/acf-providers.md](references/acf-providers.md) |
| Query loops | [references/query-loops.md](references/query-loops.md) |
| Query filters, AJAX pagination, load more | [references/query-filters.md](references/query-filters.md) |
| Element conditions | [references/conditions.md](references/conditions.md) |
| Interactions and animations | [references/interactions.md](references/interactions.md) |
| Popups | [references/popups.md](references/popups.md) |
| Templates and template conditions | [references/templates.md](references/templates.md) |
| Forms | [references/forms.md](references/forms.md) |
| WooCommerce | [references/woocommerce.md](references/woocommerce.md) |
| External assets from a reference URL | [references/external-assets.md](references/external-assets.md) |
| PHP custom elements / hooks | [references/custom-elements.md](references/custom-elements.md), [references/hooks.md](references/hooks.md) |
| Asset loading, builder permissions | [references/assets-permissions.md](references/assets-permissions.md) |

[patterns/](patterns/INDEX.md) are upstream examples with raw hex values and generic class names. Use them for **structure and settings shapes only**; restyle with BEM + tokens. The `bem-*.json` files are closest to the SkeleBricks approach.

## Non-negotiable rules

1. **Closed token set.** Only variables from tokens.md. Never create or rename a variable; snap values to the nearest token. Brand differences become value changes to existing variables, listed after the JSON.
2. **BEM global classes for all styling.** Semantic names from the section's purpose (`.pricing__card--featured`, not `.box-2`). Elements carry content and structure only.
3. **UI controls first, then `%root%`.** Margin, padding, typography, background, border, grid etc. go in the class's native settings. Only properties without a control go in the class's `_cssCustom`, and that CSS targets `%root%`. Never `#brxe-{id}` in pasted JSON.
4. **Readable custom CSS.** Never minify `_cssCustom` onto one line. `%root% {` on its own line, one declaration per line indented 2 spaces, `}` on its own line, a blank line between rules, multi-layer values split one layer per line (`\n` in the JSON string). See PROFILE.md §4a.
5. **Tag mapping.** `<section>` → Section, `<div>` → Block (the section's inner max-width wrapper → Container), `<h1>`–`<h6>` → Heading, `<img>` → Image; the rest per html-conversion.md.
6. **Labels.** Every section labelled by purpose (`Hero`, `Features`, `CTA`, `Pricing`); never left as "Section". Other elements get readable role labels.
7. **Flat tree integrity.** Every child exists and points back to its parent; no duplicate ids; sections only at the root.
8. **Verified value shapes only.** Colours are objects (`{"raw": "var(--primary)"}`); typography keys are CSS property names; spacing is a per-side object; `_gradient` uses `colors: [{color, stop}]`. Don't invent settings keys.
9. **Layout elements** (`section` `container` `block` `div`) use `_direction`, `_columnGap`, `_rowGap`; `_gap` is for non-layout elements.
10. **Responsive grammar** `key:breakpoint:pseudo` with the profile's breakpoint keys; never `:tablet` / `:mobile`.
11. **Semantic HTML.** `tag` on sections/blocks, one `h1` per page, heading levels in order, alt text on images.
12. **One ```json code block** as the final output, validated first.
13. **External assets by absolute `url`**, never attachment `id`.

## Validation checklist

- [ ] `python3 scripts/validate.py <tmpfile>` prints `OK` (it also checks token names, raw colours, BEM names, section labels, styles on elements, `%root%` usage, one-declaration-per-line CSS formatting)
- [ ] Every value that could be a token is a token
- [ ] Responsive overrides only on the profile's breakpoints
- [ ] Query loops: `hasLoop: true` + `query.objectType`; filters point at a real query element id
- [ ] Every interactive element has a hover/focus state and `_cssTransition` on its class
