# Before and after

Two fictional products. Rowan Clay is a studio selling one bowl. Harbor is a deploy tool. Neither is a real company. Do not file them in `taste/references/`.

Open the HTML in a browser. The before file is a specimen of the skeleton. The after files are the system's own examples, built from `tokens/quiet-luxury.DESIGN.md` and `tokens/precise-technical.DESIGN.md`.

| File | What it is |
| --- | --- |
| `rowan-before.html` | Negative specimen. Same studio, generic landing. |
| `rowan-after.html` | Quiet luxury. The page is the bowl and the facts of this firing. |
| `harbor-after.html` | Precise technical. The page is the revision list. The filter runs in the page. |

## Rowan, critiqued

Job: reserve a specific bowl from this firing.
Direction: `quiet-luxury`
Reference: `aesop` for the factual column. Not for their catalog, their font, or their 12px body.
Structure: the specimen is a centered hero, two filled buttons, a fake logo row, and three icon cards.

Scores, on `rowan-before.html` only (ignore the yellow banner; it is a label, not the layout):

- Hierarchy: 2 — `chrome.two-primaries` and `hierarchy.center-is-ceremonial`. "Shop the drop" and "Learn more" are both filled, and every block is centered. The bowl is absent, so `hierarchy.first-screen` fails.
- Spacing: 2 — `spacing.section-jump`. Hero, logos, and cards sit in one even stack. The cards repeat the same padding as their gap.
- Uniqueness: 1 — `skeleton.saas-landing` and `content.abstract-verbs`. "Elevate your everyday rituals" could sell anything. `content.fake-proof` ("10,000+ design-led homes").
- Restraint: 1 — `color.aurora` (gradient text), `color.indigo-default` (Inter, indigo, gray page), `material.icon-tile`, `material.gray-card-shadow`, `chrome.sparkle`.
- Accessibility: 2 — `a11y.contrast`. The headline is gradient-clipped text. The logo row and the footer are `#94a3b8` on `#f8fafc`, about 2.5:1. There is no focus ring. The banner is not part of the layout.
- Product fit: 1 — `product.direction-serves-job`. A single object was given a SaaS homepage.

Required changes:

1. Element: the whole first viewport, including the three cards and the logo row.
   Rule: `uniqueness.refuse-skeleton`
   Now: centered gradient headline, two filled buttons, proof row, three icon tiles.
   Change: delete the cards, the logo row, the second button, and the gradient. Build one spread. A still of Bowl 18 on a warm ground. Beside it, a start-aligned column: one kicker, a factual title, one paragraph, the price, one text action.
   Leave: the studio name.

2. Element: headline and dek.
   Rule: `uniqueness.specific-copy`
   Now: "Elevate your everyday rituals" and a sentence with Seamless, next-gen, and Unlock.
   Change: "Ash glaze, eighteen centimetres." Body states wheel, place, glaze, width, volume, and when it ships.
   Leave: the price, rewritten next to the action.

3. Element: page surface, type, buttons.
   Rule: `color.indigo-default`
   Now: slate page, Inter, indigo pills.
   Change: warm paper `#f3efe6`, ink `#1c1915`, Newsreader for the name and the title only, Public Sans elsewhere. One underlined action. Oxide `#7a3e2e` appears only as the glaze line in the drawing.
   Leave: nothing indigo.

4. Element: headline contrast and focus.
   Rule: `a11y.contrast`
   Now: gradient text, no focus ring.
   Change: solid ink type. A 2px offset focus ring on every link.
   Leave: the specimen banner, which is outside the design.

Refused while fixing: `color.gold-on-black`, `type.avoid-tells` (no Playfair, no Instrument Serif), `motion.stagger-fade`, a filled accent button.

The result is `rowan-after.html`.

Job: reserve Bowl 18 from this firing.
Direction: `quiet-luxury`
Reference: `aesop`
Structure: this page is the bowl, with the facts of the firing in a narrow column.

- Hierarchy: 5 — `hierarchy.one-primary-action`. One text action, "Reserve from this firing", beside the price. The still is the subject.
- Spacing: 4 — `spacing.section-jump`. The spread's gap is 64px; the essay sits 96px below. The definition list is tighter than both.
- Uniqueness: 5 — `uniqueness.one-idea`. The drawing is not a photograph, and it does not pretend to be one. The glaze line is the single detail.
- Restraint: 5 — `color.accent-rarity`. Oxide is the glaze, not the button. Two families, with roles.
- Accessibility: 4 — `a11y.names`. The action says which firing. The skip link and the focus ring are present. Muted ink `#5c564c` on `#f3efe6` clears 4.5:1.
- Product fit: 5 — `product.sentence`. It feels like Aesop's label column because the object is physical and the copy is factual, not because the page borrowed a skincare palette.

Still failing after this pass: none at a 2. The drawing is a diagram, so a real studio would replace it with a photograph of the bowl on the same ground and keep the column. That is `uniqueness.diverge-from-reference` in the right direction: the structure stays, the material becomes theirs.

## Harbor

A dashboard costume for the same tool would be a sidebar, four cards (deploys today, success rate, p95, active users), a chart, and then the table. That fails `layout.dashboard-costume` and `density.match-job`. The job is "see which revision failed."

`harbor-after.html` skips the costume.

- The first screen is the list. Status is a word (`a11y.not-color-alone`): Shipped, Building, Failed.
- Rows share one grid (`density.repeat-rhythm`). No card, no shadow, 4px radius only on the filter field.
- Mono is the sha (`type.roles`). The title is IBM Plex Sans at 20px.
- The filter has a visible label. Typing `failed` or `proxy` hides the other rows and can show "No revisions match that filter."
- Green, rust, and amber are status words, not a primary button. This screen does not need a filled button, and it does not pretend to switch environments. The line under the title says which environment the list is.
