# HTML / CSS / JS → Bricks Conversion

Use this when the input is existing markup (a static page, a Tailwind or Webflow export, a CodePen, a component from another builder) rather than a design brief. Adapted from html2bricks (h2b v4.0.0) and corrected against the source-verified shapes in style-settings.md.

**SkeleBricks first:** read framework/PROFILE.md and framework/tokens.md before mapping any CSS. Every value is snapped to an existing token (never a new variable), every styled element gets a BEM global class, and styles go on that class.

## 0. React, Vue, Svelte, JSX, Tailwind: resolve first

Don't convert framework code directly. First produce clean semantic HTML + standard CSS, then run the workflow below on that.

1. **Render the markup mentally**: replace components with the HTML they output, props with their values, `{items.map(...)}` / `v-for` with the repeated markup (use the real data if given, otherwise 3 representative items), conditionals with the default visible branch. Drop `key`, `ref`, event handlers, `className` → `class`, `v-*` / `:bind` / `@event` attributes.
2. **Expand utility classes to CSS properties**: `py-4 px-6` → `padding: 16px 24px` (Tailwind's scale: `1` = 4px), which at SkeleBricks' 10px root is `1.6rem 2.4rem`, `grid-cols-3` → `grid-template-columns: repeat(3, …)`, `md:` / `lg:` prefixes → media queries, `hover:` → `:hover`, `dark:` → note it, `text-gray-600` → its colour. Convert all px with SkeleBricks' 1rem = 10px.
3. **Rename into BEM**: discard the utility class names entirely and give each element a semantic BEM class (`.hero__heading`), carrying the resolved CSS.
4. **State and behaviour** (`useState`, `v-model`, toggles, modals, tabs) → Bricks equivalents in the JavaScript tiers below (interactions, nestable elements, popups). Data fetching → query loops / dynamic data or a Tier 2–4 note.
5. Continue with the workflow, snapping the resolved CSS to tokens (`2.4rem` padding → `var(--space-l)`, `text-gray-600` → `var(--text-body)`).

## Workflow

1. **Parse** the HTML into a DOM tree. Note every class name, id, inline style and `<script>`.
2. **Map tags to elements** (table below). Pick by role, not by tag alone: a `<div>` can be a `block`, `div` or `container` depending on what it does.
3. **Generate ids** (6-char lowercase alphanumeric, unique in the file) and **flatten** the tree into `content` with reciprocal `parent` / `children`.
4. **Name BEM classes**: every styled element gets a semantic BEM global class (`.hero`, `.hero__container`, `.hero__kicker`). Source class names are renamed to BEM if they aren't already; utility classes are discarded after their CSS is resolved.
5. **Convert CSS to native settings on the class** using the property map below, with every value snapped to a SkeleBricks token.
6. **Pseudo-classes and states** → `key:pseudo` suffixes (`_background:hover`). Pseudo-elements and complex selectors → `_cssCustom`.
7. **Media queries** → breakpoint suffixes. Translate the source's min/max widths to the nearest Bricks breakpoint key (and the site's mobile-first / desktop-first mode from the profile).
8. **Residual CSS** (anything without a native UI control, e.g. `::before`, `mask-image`, `@keyframes`, `.block:hover .block__icon`) → the class's `_cssCustom`, targeting `%root%` and formatted one declaration per line (framework/PROFILE.md §4a).
9. **JavaScript** → the tiers below, `_interactions` first.
10. **Assets** → absolute URLs, see external-assets.md.
11. **Label** every section by purpose (`Hero`, `Features`, `CTA`) and other elements by role.
12. **Assemble** the clipboard wrapper, validate with `scripts/validate.py`, output in one ```json block.

## Tag → element map

| HTML | Bricks element | Notes |
|------|----------------|-------|
| `<section>`, top-level `<header>` / `<main>` / `<footer>` band | **Section** | set `tag` to the semantic tag; `label` = purpose (`Hero`) |
| the section's inner max-width wrapper (`.container`, `.wrapper`, `max-w-7xl mx-auto`) | **Container** | class `.{block}__container` |
| any other `<div>` | **Block** | including decorative/absolute pieces |
| `<article>`, `<aside>`, `<nav>`, `<figure>`, `<ul>` wrapper | **Block** with `tag` | `tag: "custom"` + `customTag` for `ul`, `li`, etc. |
| `<h1>`–`<h6>` | **Heading** | `tag` = the original level |
| `<p>` (plain) | `text-basic` | `tag: "p"` |
| `<p>` with inline markup, or several paragraphs / lists | `text` | rich HTML in `text` |
| `<span>` eyebrow / label | `text-basic` | `tag: "span"` |
| `<a>` inline/text link | `text-link` | |
| `<a class="btn">`, `<button>` | `button` | `tag: "button"` for non-navigation actions; omit `style` when the framework styles buttons |
| `<img>` | **Image** | `altText`, `loading` |
| `<picture>` / `srcset` | `image` | use the largest candidate URL |
| `<video>` / YouTube / Vimeo iframe | `video` | `media: file / youtube / vimeo` |
| `<audio>` | `audio` | |
| inline `<svg>` | `svg` (`source: "code"`) or `icon` (`library: "svg"`) | |
| `<i class="fa-…">` / icon font | `icon` | map to the library the site loads |
| `<hr>` | `divider` | |
| `<form>` | `form` | rebuild fields; see forms.md |
| `<nav>` with links/dropdowns | `nav-nested` | see elements.md nestables |
| `<details>` / FAQ lists | `accordion-nested` | needs the `_hidden` structural classes |
| tab UI | `tabs-nested` | |
| slider/carousel markup (Swiper, Slick, etc.) | `slider-nested` | rebuild slides as blocks; drop the old library |
| `<iframe>` (maps, other embeds) | `map` / `map-leaflet` or `html` | |
| anything that can't be expressed natively | `html` (`html` setting) or `code` | last resort; flag it |

## CSS → native settings map

| CSS | Bricks setting |
|-----|----------------|
| `display:flex; flex-direction` on a layout element | `_direction` (layout elements are flex already) |
| `flex-direction` on a non-layout element | `_display: "flex"` + `_flexDirection` |
| `gap` on layout element | `_columnGap` / `_rowGap` |
| `gap` on non-layout element | `_gap` |
| `display:grid; grid-template-columns` | `_display: "grid"`, `_gridTemplateColumns`, `_gridGap` |
| `grid-column: span 2` (child) | `_gridItemColumnSpan: "span 2"` |
| `max-width` / `min-height` | `_widthMax` / `_heightMin` |
| `padding` / `margin` | `_padding` / `_margin` per-side object |
| `font-*`, `line-height`, `letter-spacing`, `text-align`, `text-transform`, `color` | `_typography` with CSS property names |
| `background-color` | `_background.color` |
| `background-image: url()` | `_background.image.url` + `size` / `position` / `repeat` |
| `background-image: linear-gradient()` | `_gradient` with `colors: [{color, stop}]` |
| `border`, `border-radius` | `_border` (`width`, `style`, `color`, `radius`) |
| `box-shadow` | `_boxShadow` control on the class, values snapped to the nearest `--shadow-*` preset (framework/PROFILE.md §3), colour `var(--shadow)`. Never custom CSS |
| `max-width` on the section's inner wrapper | drop it: SkeleBricks theme styles set the Container width globally |
| `transform` (single functions) | `_transform` |
| `transform` (chained, order matters) | `_cssCustom` |
| `filter` | `_cssFilters` |
| `transition` | `_cssTransition` (list properties, not just `all`) |
| `position`, `top/right/bottom/left`, `z-index` | `_position`, `_top`…, `_zIndex` |
| `overflow`, `opacity`, `cursor`, `aspect-ratio`, `object-fit` | `_overflow`, `_opacity`, `_cursor`, `_aspectRatio`, `_objectFit` |
| `mix-blend-mode`, `pointer-events`, `isolation` | `_mixBlendMode`, `_pointerEvents`, `_isolation` |
| CSS custom property (`var(--x)`) | keep as `{ "raw": "var(--x)" }` for colors, plain string for lengths |
| `@keyframes`, `::before/::after` content, attribute selectors, `.parent:hover .child` | `_cssCustom` |

Every value is a string. Snap to tokens: colours → `{"raw": "var(--…)"}`, spacing → `var(--space-*)`, font sizes → `var(--text-*)`, radii → `var(--radius-*)`, grid columns → `var(--grid-*)`. Leftover raw lengths use 1rem = 10px.

## Pseudo-classes

Grammar: `_{key}[:{breakpoint}]:{pseudo}`, e.g. `_background:hover`, `_typography:mobile_portrait:hover`.

- `:hover`, `:active`, `:focus` work everywhere by default.
- Any other pseudo (`:focus-visible`, `:focus-within`, `:first-child`, `:nth-child(2n)`, `:checked`, `::before`) must exist in the site's pseudo-class registry (`bricks_global_pseudo_classes`). Template import creates missing ones; clipboard paste may not. When unsure, put those rules in `_cssCustom`.
- Always pair state changes with `_cssTransition`.

```json
{
  "_cssTransition": "background-color 0.2s ease, transform 0.2s ease",
  "_background": { "color": { "raw": "var(--primary)" } },
  "_background:hover": { "color": { "raw": "var(--primary-d-1)" } },
  "_transform:hover": { "translateY": "-2" }
}
```

## JavaScript tiers

Pick the lowest tier that does the job.

**Tier 1, native `_interactions` (most cases).** Corrected action names (h2b's examples used names that don't exist):

| Source JS | Bricks interaction |
|-----------|--------------------|
| `el.classList.toggle('is-open')` on click | `{ "trigger": "click", "action": "toggleAttribute", "actionAttributeKey": "class", "actionAttributeValue": "is-open", "target": "custom", "targetSelector": ".menu" }` |
| show a hidden element on click | `{ "trigger": "click", "action": "show", "target": "custom", "targetSelector": "#modal" }` |
| IntersectionObserver fade-in | `{ "trigger": "enterView", "action": "startAnimation", "animationType": "fadeInUp", "animationDuration": "0.6s", "runOnce": true, "rootMargin": "0px 0px -80px 0px" }` |
| scroll-to anchor | `{ "trigger": "click", "action": "scrollTo", "target": "custom", "targetSelector": "#pricing" }` |
| open modal | build it as a popup template, then `{ "trigger": "click", "action": "show", "target": "popup", "templateId": 123 }` |
| hamburger / drawer | `offcanvas` + `toggle` elements, no JS |
| accordion / tabs / slider scripts | the nestable elements, no JS |
| scroll parallax | `_motionElementParallax` keys (style-settings.md) |

Every interaction needs its own unique 6-char `id`. Full schema: interactions.md.

**Tier 2, extract a script.** Calculations, fetches, stateful widgets. Put the JS in a separate `.js` file next to the JSON and say where it should load (page settings `customScriptsBodyFooter`, child theme enqueue, or the framework's JS location from the profile). Avoid `code` elements with `executeCode`.

**Tier 3, library.** GSAP, Chart.js, etc. Note the library + version and where it is enqueued. Call it from an interaction with `action: "javascript"`, `jsFunction`, `jsFunctionArgs: [{ "id": "...", "jsFunctionArg": "%brx%" }]`.

**Tier 4, WordPress-side setup.** CPTs, ACF fields, hooks: write the setup steps and PHP (hooks.md) as part of the delivery.

## Text element choice

- `heading`: plain text only, semantic `h1`–`h6`. One `h1` per page.
- `text-basic`: one paragraph or span of plain text.
- `text`: rich HTML (inline `<strong>`, links, several paragraphs, lists).

## Output

One clipboard JSON in a single ```json code block, plus companion files when tiers 2–4 were used (`scripts/*.js`, setup notes). In the final message, list anything that was approximated or dropped.
