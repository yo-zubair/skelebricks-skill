# SkeleBricks Framework Profile

The SkeleBricks CSS framework and the build rules this skill follows. **This file overrides every default in SKILL.md and references/.** Fields still marked `TODO` use the fallback in their row; say so in the final message when a fallback was used.

---

## 1. Framework identity

| Field | Value |
|-------|-------|
| Framework | **SkeleBricks**: native Bricks Style Manager + a fixed set of custom properties ([tokens.md](tokens.md)) |
| Framework classes | None ship as CSS. Every class is a **Bricks global class** created in the JSON (`globalClasses` + `_cssGlobalClasses`) |
| Utility classes | None. Don't use `_cssClasses` for styling |

## 2. Units and breakpoints

| Field | Value | Fallback while TODO |
|-------|-------|---------------------|
| Root font size | **1rem = 10px** (tokens scale from 36rem = 360px) | |
| Screen range | `--min-screen-width` 360px → `--max-screen-width` 1440px | |
| Breakpoint mode | TODO | desktop-first |
| Breakpoint keys | TODO | `tablet_portrait` 991, `mobile_landscape` 767, `mobile_portrait` 478 |
| Fluid sizing | Built into the tokens. Don't write your own `clamp()` for spacing or type | |

## 3. Tokens: closed set

- Use **only** the variables in [tokens.md](tokens.md). **Never create a new variable or rename one.**
- **Snap every value to the nearest existing token** (cheat sheet at the bottom of tokens.md). No raw px/rem spacing, font sizes, radii or colours where a token can stand in.
- If the design's brand differs (e.g. a green primary), **change the value of the existing variable**, never the name. List those changes after the JSON as "Style Manager value changes", e.g. `--primary: hsl(152, 60%, 40%)`. Derived shades (`-l-*`, `-d-*`, `-t-*`) follow the same hue.
- Accepted exceptions (not tokens): `0`, `auto`, `100%`, `1fr`, `ch` widths for prose (`65ch`), line-height and letter-spacing numbers, aspect ratios, z-index, transition timings.

How to write them in Bricks settings:

| Need | Setting |
|------|---------|
| Any colour | `{ "raw": "var(--primary)" }` |
| Spacing | `"_padding": { "top": "var(--space-2xl)", "bottom": "var(--space-2xl)" }`, `"_rowGap": "var(--space-m)"` |
| Font size | `"_typography": { "font-size": "var(--text-xl)", "color": { "raw": "var(--text-title)" } }` |
| Radius | `"_border": { "radius": { "top": "var(--radius-m)", "right": "var(--radius-m)", "bottom": "var(--radius-m)", "left": "var(--radius-m)" } }` |
| Grid columns | `"_display": "grid", "_gridTemplateColumns": "var(--grid-3)"`, responsive `"_gridTemplateColumns:mobile_portrait": "var(--grid-1)"` |
| Shadow | Tokens are full `box-shadow` values, and the `_boxShadow` control can't take one. Use custom CSS (formatted per §4a): `box-shadow: var(--shadow-m);` inside a `%root% { … }` rule |
| Max width | `"_widthMax": "var(--max-screen-width)"` |

Colour roles: headings `--text-title`, body copy `--text-body`, page background `--bg-body`, cards/panels `--bg-surface`, dividers/borders `--border`, subtle fills `--muted` or `*-t-1/2`, hover of primary `--primary-d-1`. Text on photos or always-dark panels uses `--always-light`.

## 4. Styling strategy

| Rule | Value |
|------|-------|
| Where styles live | **On the BEM global class.** Use the class's native UI controls (`_padding`, `_margin`, `_typography`, `_background`, `_border`, `_gridTemplateColumns`, …) |
| Element settings | **Content and structure only**: `text`, `tag`, `image`, `link`, `icon`, `_cssGlobalClasses`, `_cssId` (anchors), `_attributes`, `_conditions`, `_interactions`, `hasLoop`/`query`, nestable `_hidden` classes |
| Properties without a UI control | In the class's **Custom CSS** (`_cssCustom`), targeting **`%root%`** (e.g. a `box-shadow` token, `%root%::before`, `%root%:hover .card__icon`), **formatted per §4a** |
| Modifiers | Separate class stacked after the base (class ids `["crd001", "crdftd"]` → `.card .card--featured`), listed later in `globalClasses` so it wins |
| Bricks theme styles / button `style` | Don't rely on them. Omit `style` on buttons; style via the button's BEM class |

## 4a. Custom CSS formatting

Custom CSS must be readable in the Bricks Custom CSS editor: **one declaration per line**, never minified onto a single line.

- Selector and opening brace on one line: `%root% {`
- Each declaration on its own line, indented **2 spaces**, ending with `;`
- Closing brace `}` alone on its own line, at the selector's indent
- One **blank line** between rules
- A value with several comma-separated layers (multiple gradients, `transition`, `mask-image`, `box-shadow` lists, `font-family` stacks longer than the line) puts the property name on its own line and each layer on its own line, indented 4 spaces, with the final layer ending in `;`
- Rules inside `@media` / `@supports` / `@container` are indented one more level (2 spaces)
- Spaces, not tabs; no trailing whitespace; no comments unless they explain something non-obvious

In the JSON string, line breaks are `\n`. What the editor should show:

```css
%root% {
  display: block;
  aspect-ratio: 1;
  pointer-events: none;
}

%root%:hover .trust__icon {
  transform: rotate(8deg);
}

%root% {
  background-image:
    linear-gradient(7deg, transparent 47%, var(--warning-t-3) 47% 49%, transparent 49%),
    repeating-linear-gradient(90deg, transparent 0 9%, var(--light) 9% 9.5%);
  mask-image: linear-gradient(to bottom, transparent 0%, black 25%, black 75%, transparent 100%);
}

@media (max-width: 767px) {
  %root% {
    display: none;
  }
}
```

The same `_cssCustom` value in JSON:

```json
"_cssCustom": "%root% {\n  display: block;\n  aspect-ratio: 1;\n  pointer-events: none;\n}\n\n%root%:hover .trust__icon {\n  transform: rotate(8deg);\n}"
```

Group all declarations for the same selector into one rule rather than repeating `%root% {` blocks.

## 5. Naming conventions (BEM)

- **Always BEM**: `block`, `block__element`, `block--modifier`, `block__element--modifier`. Lowercase, hyphens inside words (`feature-grid__item`).
- **Names are semantic, from the section's purpose**: `.hero`, `.hero__container`, `.hero__kicker`, `.hero__heading`, `.hero__text`, `.hero__actions`, `.hero__btn`, `.hero__img`. Never `.section-1`, `.box`, `.wrapper2`, `.blue-text`.
- **The Container element's class is always `{block}__container`** (`.hero__container`, `.pricing__container`). Never `__inner`, `__wrapper` or `__wrap`.
- **Common element names**: `__container` (the Container element), `__header`, `__kicker` (eyebrow), `__heading`, `__subheading`, `__text`, `__actions`, `__btn`, `__img`, `__media`, `__grid`, `__list`, `__item`, `__card`, `__icon`, `__meta`, `__footer`.
- Nested repeating components get their own block: inside `.features`, a card is `.feature-card` with `.feature-card__icon`, `.feature-card__heading`.
- **Class ids** (the `id` of the global class object) are 6-char alphanumeric, unique; the `name` is the BEM name.
- Before creating a class, check whether the same BEM name already exists in this JSON. Bricks merges pasted classes by name, so reuse names deliberately across sections (`.btn`-style shared blocks) and never reuse a name for different styling.

## 6. Structure and labels

| Rule | Value |
|------|-------|
| Section skeleton | `section` (`.hero`) → `container` (`.hero__container`) → blocks / content |
| `<section>` | **Section** element, `tag` set to the semantic tag |
| `<div>` | **Block** element. The section's inner max-width wrapper is the exception: **Container** |
| `<h1>`–`<h6>` | **Heading** with matching `tag` |
| `<img>` | **Image** |
| Other tags | per references/html-conversion.md |
| **Section labels** | Every section's `label` is its human name: `Hero`, `Features`, `CTA`, `Pricing`, `Testimonials`, `FAQ`, `Footer`. Never "Section" |
| Other labels | Readable role names for the structure panel: `Container`, `Kicker`, `Heading`, `Actions`, `Card`… (match the BEM element) |
| Container width | Section/container max width from `--max-screen-width` unless the Style Manager already sets it |
| Icons | TODO | fallback: inline SVG (`svg` element / icon `library: "svg"`) |
| Animations | TODO | fallback: none unless the design asks; then subtle `enterView` reveals |

## 7. Delivery

| Field | Value |
|-------|-------|
| Final output | **One single ```json code block** in the chat containing the complete clipboard JSON, ready to paste onto the Bricks canvas. No .json file is written to the project |
| Before printing | Write the JSON to a temp file in the scratchpad, run `scripts/validate.py` on it, fix until `OK`, then print exactly that JSON |
| After the code block | Short notes only: Style Manager value changes (if any), TODO fallbacks used, anything approximated |
| Format | Clipboard (`bricksCopiedElements`) with every referenced class in `globalClasses` |
| Bricks version | TODO | 2.3.6 |

## 8. Input handling

- **React / Vue / Svelte / JSX / Tailwind**: first resolve to clean semantic HTML + standard CSS (expand utility classes to real property values, unroll `map()` loops into repeated markup, drop framework-only attributes and state), then convert that HTML as usual and snap the CSS to tokens. See references/html-conversion.md §0.
