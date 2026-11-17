# SkeleBricks Tokens

The complete, closed list of SkeleBricks variables (built on the Bricks Style Manager). **Use only these names.** Never add a variable, never rename one. A design is adapted to these tokens; if a brand needs different values, change the *value* of an existing variable (see PROFILE.md §3).

`scripts/validate.py` reads this file to check every `var(--…)` in the JSON.

Root font size: **1rem = 10px** (the fluid scales are built between `36rem` = 360px and 1440px).

## Colors

```css
--primary: hsl(235, 63%, 62%);
--secondary: hsl(0, 0%, 41%);
--bg-body: hsl(0, 0%, 95%);
--bg-surface: hsl(0, 0%, 100%);
--light: hsl(0, 0%, 100%);
--always-light: hsl(0, 0%, 100%);
--dark: hsl(0, 0%, 0%);
--always-dark: hsl(0, 0%, 0%);
--text-title: hsl(0, 0%, 0%);
--text-body: hsl(0, 0%, 25%);
--border: hsla(0, 0%, 50%, 0.5);
--shadow: hsla(0, 0%, 0%, 0.15);
--muted: hsla(0, 0%, 50%, 0.25);
--info: hsl(190, 91%, 49%);
--success: hsl(152, 69%, 31%);
--warning: hsl(45, 99%, 51%);
--danger: hsl(354, 70%, 54%);
--info-t-1: hsla(190, 88%, 90%, 0.2);
--info-t-2: hsla(190, 88%, 80%, 0.4);
--info-t-3: hsla(190, 88%, 69%, 0.6);
--info-t-4: hsla(190, 88%, 59%, 0.8);
--success-t-1: hsla(152, 31%, 86%, 0.2);
--success-t-2: hsla(152, 31%, 72%, 0.4);
--success-t-3: hsla(152, 31%, 59%, 0.6);
--success-t-4: hsla(152, 38%, 45%, 0.8);
--warning-t-1: hsla(45, 99%, 90%, 0.2);
--warning-t-2: hsla(45, 99%, 80%, 0.4);
--warning-t-3: hsla(45, 99%, 71%, 0.6);
--warning-t-4: hsla(45, 99%, 61%, 0.8);
--danger-t-1: hsla(354, 70%, 91%, 0.2);
--danger-t-2: hsla(354, 70%, 82%, 0.4);
--danger-t-3: hsla(354, 70%, 72%, 0.6);
--danger-t-4: hsla(354, 70%, 63%, 0.8);
--primary-l-1: hsl(235, 63%, 70%);
--primary-l-2: hsl(235, 63%, 77%);
--primary-l-3: hsl(235, 63%, 85%);
--primary-l-4: hsl(235, 63%, 92%);
--primary-d-1: hsl(235, 39%, 50%);
--primary-d-2: hsl(235, 39%, 37%);
--primary-d-3: hsl(235, 39%, 25%);
--primary-d-4: hsl(235, 39%, 12%);
--primary-t-1: hsla(235, 63%, 92%, 0.2);
--primary-t-2: hsla(235, 63%, 85%, 0.4);
--primary-t-3: hsla(235, 63%, 77%, 0.6);
--primary-t-4: hsla(235, 63%, 70%, 0.8);
--secondary-l-1: hsl(0, 0%, 53%);
--secondary-l-2: hsl(0, 0%, 65%);
--secondary-l-3: hsl(0, 0%, 76%);
--secondary-l-4: hsl(0, 0%, 88%);
--secondary-d-1: hsl(0, 0%, 33%);
--secondary-d-2: hsl(0, 0%, 25%);
--secondary-d-3: hsl(0, 0%, 16%);
--secondary-d-4: hsl(0, 0%, 8%);
--secondary-t-1: hsla(0, 0%, 88%, 0.2);
--secondary-t-2: hsla(0, 0%, 76%, 0.4);
--secondary-t-3: hsla(0, 0%, 65%, 0.6);
--secondary-t-4: hsla(0, 0%, 53%, 0.8);
--light-t-1: hsla(0, 0%, 100%, 0.2);
--light-t-2: hsla(0, 0%, 100%, 0.4);
--light-t-3: hsla(0, 0%, 100%, 0.6);
--light-t-4: hsla(0, 0%, 100%, 0.8);
--dark-t-1: hsla(0, 0%, 80%, 0.2);
--dark-t-2: hsla(0, 0%, 60%, 0.4);
--dark-t-3: hsla(0, 0%, 40%, 0.6);
--dark-t-4: hsla(0, 0%, 20%, 0.8);
--always-dark-t-1: hsla(0, 0%, 80%, 0.2);
--always-dark-t-2: hsla(0, 0%, 60%, 0.4);
--always-dark-t-3: hsla(0, 0%, 40%, 0.6);
--always-dark-t-4: hsla(0, 0%, 20%, 0.8);
--always-light-t-1: hsla(0, 0%, 100%, 0.2);
--always-light-t-2: hsla(0, 0%, 100%, 0.4);
--always-light-t-3: hsla(0, 0%, 100%, 0.6);
--always-light-t-4: hsla(0, 0%, 100%, 0.8);
```

Naming: `-l-1…4` lighter shades, `-d-1…4` darker shades, `-t-1…4` transparent tints (1 = faintest). `--light`/`--dark` may flip in a dark mode; `--always-light`/`--always-dark` never flip, so use them on fixed-colour surfaces (image overlays, buttons on photos).

## Layout, radius, shadow, grid

```css
--max-screen-width: 1440px;   /* applied to Containers globally by the SkeleBricks theme styles; don't set it in JSON */
--min-screen-width: 360px;
--radius-xs: clamp(0.4rem,calc(0vw + 0.4rem),0.4rem);
--radius-s: clamp(0.6rem,calc(0.19vw + 0.54rem),0.8rem);
--radius-m: clamp(1rem,calc(0.19vw + 0.94rem),1.2rem);
--radius-l: clamp(1.6rem,calc(0.37vw + 1.48rem),2rem);
--radius-xl: clamp(2.6rem,calc(0.56vw + 2.42rem),3.2rem);
--radius-full: 999rem;
/* --shadow-*: reference values only. Shadows are set with the Bricks _boxShadow control using these values (PROFILE.md §3) */
--shadow-xs: 0 1px 2px var(--shadow);
--shadow-s: 0 1.5px 3px var(--shadow);
--shadow-m: 0 2px 6px var(--shadow);
--shadow-l: 0 3px 12px var(--shadow);
--shadow-xl: 0 6px 48px var(--shadow);
--grid-1: repeat(1, minmax(0, 1fr));
--grid-2: repeat(2, minmax(0, 1fr));
--grid-3: repeat(3, minmax(0, 1fr));
--grid-4: repeat(4, minmax(0, 1fr));
--grid-5: repeat(5, minmax(0, 1fr));
--grid-6: repeat(6, minmax(0, 1fr));
--grid-7: repeat(7, minmax(0, 1fr));
--grid-8: repeat(8, minmax(0, 1fr));
--grid-9: repeat(9, minmax(0, 1fr));
--grid-10: repeat(10, minmax(0, 1fr));
--grid-11: repeat(11, minmax(0, 1fr));
--grid-12: repeat(12, minmax(0, 1fr));
--grid-1-2: minmax(0, 1fr) minmax(0, 2fr);
--grid-2-1: minmax(0, 2fr) minmax(0, 1fr);
--grid-1-3: minmax(0, 1fr) minmax(0, 3fr);
--grid-3-1: minmax(0, 3fr) minmax(0, 1fr);
--grid-2-3: minmax(0, 2fr) minmax(0, 3fr);
--grid-3-2: minmax(0, 3fr) minmax(0, 2fr);
--grid-1-4: minmax(0, 1fr) minmax(0, 4fr);
--grid-4-1: minmax(0, 4fr) minmax(0, 1fr);
--grid-3-4: minmax(0, 3fr) minmax(0, 4fr);
--grid-4-3: minmax(0, 4fr) minmax(0, 3fr);
```

## Spacing (fluid)

```css
--space-4xs: clamp(0.52rem, calc(-0.00018518518518518534 * (100vw - 36rem) + 0.52rem), 0.5rem);
--space-3xs: clamp(0.66rem, calc(0.00037037037037036965 * (100vw - 36rem) + 0.66rem), 0.7rem);
--space-2xs: clamp(0.82rem, calc(0.0015740740740740745 * (100vw - 36rem) + 0.82rem), 0.99rem);
--space-xs: clamp(1.02rem, calc(0.0035185185185185176 * (100vw - 36rem) + 1.02rem), 1.4rem);
--space-s: clamp(1.28rem, calc(0.006481481481481481 * (100vw - 36rem) + 1.28rem), 1.98rem);
--space-m: clamp(1.6rem, calc(0.011111111111111108 * (100vw - 36rem) + 1.6rem), 2.8rem);
--space-l: clamp(2rem, calc(0.01814814814814815 * (100vw - 36rem) + 2rem), 3.96rem);
--space-xl: clamp(2.5rem, calc(0.0287037037037037 * (100vw - 36rem) + 2.5rem), 5.6rem);
--space-2xl: clamp(3.13rem, calc(0.04435185185185185 * (100vw - 36rem) + 3.13rem), 7.92rem);
--space-3xl: clamp(3.91rem, calc(0.0674074074074074 * (100vw - 36rem) + 3.91rem), 11.19rem);
--space-4xl: clamp(4.88rem, calc(0.10138888888888888 * (100vw - 36rem) + 4.88rem), 15.83rem);
```

## Typography (fluid)

```css
--text-xs: clamp(1.02rem, calc(0.0010185185185185173 * (100vw - 36rem) + 1.02rem), 1.13rem);
--text-s: clamp(1.28rem, calc(0.002037037037037037 * (100vw - 36rem) + 1.28rem), 1.5rem);
--text-m: clamp(1.6rem, calc(0.003703703703703703 * (100vw - 36rem) + 1.6rem), 2rem);
--text-l: clamp(2rem, calc(0.0062037037037037035 * (100vw - 36rem) + 2rem), 2.67rem);
--text-xl: clamp(2.5rem, calc(0.00972222222222222 * (100vw - 36rem) + 2.5rem), 3.55rem);
--text-2xl: clamp(3.13rem, calc(0.014907407407407411 * (100vw - 36rem) + 3.13rem), 4.74rem);
--text-3xl: clamp(3.91rem, calc(0.022222222222222216 * (100vw - 36rem) + 3.91rem), 6.31rem);
--text-4xl: clamp(4.88rem, calc(0.03277777777777778 * (100vw - 36rem) + 4.88rem), 8.42rem);
```

## Snapping cheat sheet (min → max at 1rem = 10px)

| Token | Range | Token | Range |
|-------|-------|-------|-------|
| `--space-4xs` | ~5px | `--text-xs` | 10–11px |
| `--space-3xs` | 7px | `--text-s` | 13–15px |
| `--space-2xs` | 8–10px | `--text-m` | 16–20px (body) |
| `--space-xs` | 10–14px | `--text-l` | 20–27px |
| `--space-s` | 13–20px | `--text-xl` | 25–36px |
| `--space-m` | 16–28px | `--text-2xl` | 31–47px |
| `--space-l` | 20–40px | `--text-3xl` | 39–63px |
| `--space-xl` | 25–56px | `--text-4xl` | 49–84px |
| `--space-2xl` | 31–79px | `--radius-xs/s/m/l/xl` | 4 / 6–8 / 10–12 / 16–20 / 26–32px |
| `--space-3xl` | 39–112px | `--radius-full` | pills, circles |
| `--space-4xl` | 49–158px | `--shadow-xs … xl` | 1px … 48px blur |

Snap a source value to the token whose **max** (desktop) end is closest; for small UI details compare against the min end.
