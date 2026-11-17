# SkeleBricks Skill

A Claude skill for [Bricks Builder](https://bricksbuilder.io/) (WordPress) that builds sections, pages and templates as paste-ready JSON, styled with the **SkeleBricks** CSS framework: native Bricks Style Manager variables, BEM global classes and a 1rem = 10px root.

It can design from a brief or screenshot, or convert HTML/CSS/JS, React, Vue and Tailwind into native Bricks elements. Output is one `json` code block you paste straight onto the Bricks canvas.

## What it does

- **Closed token set**: every colour, space, font size, radius, shadow and grid uses an existing SkeleBricks variable. No new variables are created; brand differences become value changes to existing ones.
- **BEM global classes**: semantic names like `.hero`, `.hero__container`, `.hero__kicker`, `.hero__heading`, `.hero__img`. Styles live on the classes, set through Bricks' native controls; anything without a control goes in the class's custom CSS targeting `%root%`.
- **Clean structure**: `<section>` → Section, `<div>` → Block (the inner wrapper → Container), `<h1>`–`<h6>` → Heading, `<img>` → Image. Sections are labelled by purpose (Hero, Features, CTA, Pricing) in the structure panel.
- **Verified settings shapes**: settings keys and value formats verified against the Bricks source, so nothing is silently ignored.
- **Validator**: `scripts/validate.py` checks the element tree, class references, value shapes and the SkeleBricks rules before anything is output.

## Install

### Claude.ai (web and desktop)

Requires a plan with Skills and code execution enabled.

1. Download `skelebricks-skill.zip` from the [latest release](../../releases) or zip this repo's folder yourself.
2. **Settings → Capabilities → Skills → Upload skill**, choose the zip.
3. Start a chat and ask for a Bricks section.

### Claude Code

```bash
git clone https://github.com/yo-zubair/skelebricks-skill.git ~/.claude/skills/skelebricks-skill
```

Update later with `git -C ~/.claude/skills/skelebricks-skill pull`.

## Examples

```text
/skelebricks-skill Recreate the attached screenshot as a Bricks section.
```

```text
/skelebricks-skill Build a SaaS landing page: hero with product image, logo strip, 3-column features, pricing with a featured plan, FAQ and a final CTA.
```

```text
/skelebricks-skill Convert this HTML/CSS into a Bricks section:
<paste markup>
```

```text
/skelebricks-skill Convert this React + Tailwind component into a Bricks section. Resolve the utility classes first.
<paste component>
```

```text
/skelebricks-skill Rebuild the hero and features sections of https://example.com as Bricks sections, using placeholder images.
```

```text
/skelebricks-skill Team grid from the ACF repeater `team_members` (photo, name, role, linkedin_url) as a query loop.
```

```text
/skelebricks-skill Filterable blog archive: live search, category filter, sort by date and AJAX pagination.
```

```text
/skelebricks-skill Header template with logo, nav with a Services dropdown, a CTA button and a mobile offcanvas menu.
```

```text
/skelebricks-skill This JSON won't paste correctly, find and fix the problems:
<paste JSON>
```

```text
/skelebricks-skill The brand colour is #16a34a. Build a CTA section and list the Style Manager value changes needed.
```

## Structure

```
SKILL.md                  entry point: modes, workflow, rules, routing
framework/PROFILE.md      SkeleBricks rules: styling, BEM, labels, delivery
framework/tokens.md       the closed list of variables + snapping table
references/               Bricks reference docs (elements, style shapes, loops, filters, popups, …)
patterns/                 example JSON; skelebricks-hero.json is the SkeleBricks reference
scripts/validate.py       validator (use --upstream for the non-SkeleBricks patterns)
SOURCES.md                credits and merge decisions
```

## Credits

Built on two MIT-licensed projects:

- [wpgaurav/bricks-skills](https://github.com/wpgaurav/bricks-skills): source-verified Bricks references and patterns
- [iamfilipp/html2bricks](https://github.com/iamfilipp/html2bricks): HTML→Bricks conversion approach

See [SOURCES.md](SOURCES.md) for what came from where and how conflicts between them were resolved.

## License

MIT. See [LICENSE](LICENSE). Bricks Builder is a proprietary product of its owners and is not included.
