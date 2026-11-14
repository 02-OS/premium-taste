# Taste Principles

Premium is a set of refusals that leave one idea visible. Cheap UI is every habit applied at once: a card for every thought, a color for every state, a font for every role, a gradient so the page looks "designed."

This file is the judgment layer. It does not ship components and it does not license one look. The checkable form of every rule id below lives in [`principles.yaml`](principles.yaml). Named failures live in [`anti-patterns.yaml`](anti-patterns.yaml). Directions live in [`directions.yaml`](directions.yaml).

Apply the rules in order. Name the job of the screen. Pick one direction. Decide what the page *is*. Then set type, space, and color. Then run [`skills/critique-ui.md`](../skills/critique-ui.md). Do not start from a palette.

**Precedence.** The user's explicit instruction and the product's real content win. The product's own `DESIGN.md` or brand guide wins on color and type families. These principles win on hierarchy, spacing, restraint, accessibility, and the refusal of generic skeletons. See `product.precedence`.

Latin-script type advice below does not transfer tracking and case to other writing systems. Hierarchy, proximity, contrast, and restraint do.

## Quick card

1. Name the job and one direction.
2. One primary action.
3. Hierarchy from size, weight, and space. Three levels.
4. The section gap is obviously larger than the item gap.
5. One color temperature. One accent, rare. No aurora, no gradient text.
6. Two families at most. Real size jumps. A reading measure.
7. Density matches the job.
8. Flat, or one shadow on a real overlay. No nested cards.
9. Motion explains a change. Nothing performs on load.
10. One structural idea. Specific words. Refuse the SaaS skeleton.
11. Contrast, focus, labels, reduced motion.
12. Critique. Change the structure before the colors.

---

## Judgment

A finished screen can be described without the words modern, clean, or premium. "A bowl on a warm ground, with the clay, the volume, and one way to reserve it." "Eight revisions in one aligned list, the failed one readable as a word." If the only description is "a hero and some cards," there is no idea yet.

The work of taste is subtraction. Add a detail only after the structure is visible in grayscale, at a squint, with the copy read out loud.

Start each screen by writing one sentence: *This is a [job] for [who], and it should feel like [one reference], because [the structural reason].* If the reason is "it looks expensive," pick again.

---

## Visual hierarchy

Hierarchy is the order a stranger's eye takes. Build it with position, scale, weight, and space. Color may confirm the order. Color must not be the only thing holding it up.

Three levels are enough for a screen: the subject, the support, the meta. A fourth level means you are writing a document. Use a heading and a rule, not another font weight.

The first screen answers three questions: where am I, what is this, what do I do. Anything that does not serve those can wait below the fold or leave.

### `hierarchy.one-job`

The screen has one job. Everything on the first screen either performs that job or identifies the place.

**Test:** Say the job in one sentence with a verb. If you need "and" twice, the screen is two screens.

**Fix:** Split the view, or move the second job to a quieter region below.

### `hierarchy.one-primary-action`

One primary action per view. A second action is a text button, a link, or an item in an overflow. Two filled buttons mean the page has not chosen.

**Test:** Count filled buttons in the first screen. More than one fails. A filled button beside a text button passes.

**Fix:** Keep the action that completes the job. Demote the other to text.

### `hierarchy.three-levels`

Subject, support, meta. Subject is the largest or heaviest. Support is readable body. Meta is one step quieter (size or weight, not a wash of gray).

**Test:** Mark each text node as subject, support, or meta. A node that needs a fourth category is noise or a heading you have not acknowledged.

**Fix:** Promote a real heading into the document structure, or delete the extra style.

### `hierarchy.first-screen`

The first viewport shows the place name, the subject, and the primary action. A stranger can point at all three in five seconds.

**Test:** Cover the page below 700px of height. If the subject or the action is gone, the hero is decoration.

**Fix:** Move the action up. Shorten the introduction. Cut the logo strip.

### `hierarchy.alignment`

One start edge for a column of text. Numbers in a column share a decimal or a right edge. Icons, if they exist, share a column. The eye should travel in a straight line down the main content.

**Test:** Draw the start edge. If titles, body, and buttons each start in a different place without a grid reason, it fails.

**Fix:** Snap the column to one edge. Center only what `hierarchy.center-is-ceremonial` allows.

### `hierarchy.center-is-ceremonial`

Centering is for one ceremonial moment: a film title, a wordmark on a cover, an empty state with a single sentence. Product UI, forms, lists, and prose are aligned to a start edge.

**Test:** If more than one block in a row is centered, and the page is not a poster, it fails.

**Fix:** Left-align (or align to the writing system's start edge). Keep at most one centered moment.

### `hierarchy.grayscale-test`

Hierarchy survives the removal of color.

**Test:** Imagine the screen in grayscale. If the primary action and the title disappear, color was doing the work.

**Fix:** Give the action weight, position, or a filled ink button. Give the title size. Then add color back as confirmation.

---

## Spacing rhythm

Space is how elements claim to be related. Premium spacing is uneven on purpose: tight inside a unit, wide between units. Even padding everywhere is how a stack of boxes happens.

Use a scale and mean it. A practical scale is 4, 8, 12, 16, 24, 32, 48, 64, 96. Most products need about five of those values. Inside a control, 8 or 12. Between related items, 16 or 24. Between sections, 48, 64, or 96. Quiet and editorial pages use the top of that range between sections. Tools use the middle.

### `spacing.scale`

Spacing values come from a small scale. Off-scale values are optical corrections (a 1–2px nudge), not new steps.

**Test:** List the distinct gaps on the screen. More than seven, or a value like 13 or 22 with no optical reason, fails.

**Fix:** Map each gap to the nearest scale step. Keep one optical correction if type sits high in its line box.

### `spacing.proximity`

A label sits closer to its field than to the previous field. A card's internal padding is smaller than the gap between cards. The gap between cards is smaller than the gap between sections.

**Test:** Measure those three relationships. If any outer gap is less than or equal to the inner gap, grouping has collapsed.

**Fix:** Tighten inside, open outside. Do not add a box to recreate a group that space can make.

### `spacing.section-jump`

The jump from "items in a group" to "groups on a page" is visible at a glance. A section gap that equals the card padding is not a section.

**Test:** Squint. If the page reads as one even stack of similar rectangles, it fails.

**Fix:** Increase the section gap by at least 2× the in-group gap, or remove the rectangles.

### `spacing.nested-padding`

Do not pad the page, the section, and the card with the same number. Nested equal padding is the boxed look.

**Test:** If page padding, section padding, and card padding are the same value, it fails.

**Fix:** Let the page own the margin. Let the group own a smaller inset. Remove the card if it has no job.

### `spacing.measure`

Prose has a measure. About 60–75 characters for body. A form field is narrower than the page. A heading may be shorter than the body (about 12–20 words) and must not stretch across a 1400px canvas.

**Test:** A body line longer than ~80 characters, or a one-line headline spanning the viewport, fails.

**Fix:** Cap the column. Let the margin be empty. Empty margin is part of the design.

### `spacing.full-bleed`

An element that touches the viewport edge does so on purpose: a photograph, a rule, a full-bleed band. Everything else sits inside the margin.

**Test:** Find anything cut off by the edge that is not a deliberate bleed. That is a bug, not a style.

**Fix:** Restore the margin, or commit to a full-bleed and align the caption to the content column.

---

## Color restraint

A complete palette is a surface, an ink, a muted ink, a hairline, and one accent. A second accent needs a job that is not "interest": destructive, or a data series. Status colors are part of the language, used the same way everywhere, and they are duller than default framework green and red.

Neutrals are tinted. Warm stone, cool graphite, green-black, paper. Pick a temperature and hold it. A warm card on a cool page looks accidental.

Dark mode is a separate palette, not an inversion. Surfaces lift in small lightness steps. Primary text is off-white. Pure white is for the rare title, if at all. Accents are desaturated or lightened until they stop vibrating. Pure `#000` against pure `#fff` is a cultural choice (a night listing, a poster), not the default for reading.

### `color.budget`

The palette is surface, ink, muted ink, hairline, and one accent, plus semantic colors that already have a meaning.

**Test:** Count hues that are not neutrals. More than one accent plus the semantic set fails.

**Fix:** Recast extras as neutrals or delete them. Keep semantic colors only where a state needs one.

### `color.temperature`

Every neutral shares a temperature. Warm paper stays warm in its borders and its muted text. Cool gray stays cool.

**Test:** Place the background, the border, and the muted text side by side. If one looks blue and another looks yellow, it fails.

**Fix:** Mix the muted ink and the hairline from the surface and the ink, not from a second gray scale.

### `color.accent-rarity`

The accent is rare. It marks the thing you must find: one action, or one state, or the selection. It does not mark every icon, every link, and every heading.

**Test:** Count accent-colored elements in the first screen. More than three fails unless each is a repeated instance of the same state (a list of errors).

**Fix:** Return links and icons to ink. Keep the accent on the one element that needs to be found.

### `color.no-aurora`

No purple-to-blue mesh backgrounds, no gradient text, no glow behind cards, no "AI" aurora. A gradient is allowed when it is light on a real material: a photograph, a sky, a product render, a single fade with a light source.

**Test:** If you can remove the gradient and the brand still reads, the gradient was costume. If the gradient is the brand, it fails.

**Fix:** Flat surface. Put the color in the content.

### `color.dark-surfaces`

A dark screen is built from a few lifted surfaces, off-white text, and content that supplies the color. It is not a light layout with the hex values flipped, and it is not a black field with a neon accent added so it feels alive.

**Test:** If the dark page is the light page inverted, or the only color is a glow, it fails.

**Fix:** Redesign surfaces for night. Let the still, the poster, or the status word carry color. Soften pure white body text.

### `color.contrast`

Body text meets WCAG AA (4.5:1). Large text and meaningful boundaries meet 3:1. Muted means "one step quieter," not gray-400 on white.

**Test:** Check the muted color against its surface. Below 4.5:1 for body-size text fails. Below 3:1 for a border that is the only separator of a control fails.

**Fix:** Darken the muted ink, or reduce emphasis with size and weight while keeping the ratio.

### `color.semantic-quiet`

Success, warning, and danger are recognizable and quiet. A saturated pill behind every status is a template. Danger is reserved for destruction and real errors, not for decoration.

**Test:** If status is a rainbow of filled pills, or red is used as a brand accent and as an error, it fails.

**Fix:** Use a word plus a small mark. Keep one hue per state. Put the word in the same column every time.

---

## Typography

Type is the voice of the product. Two families are the maximum: one for reading and UI, and one for a defined second role (display, or mono for identifiers). One family in a few weights is often better. A third family means you are making a poster. Do that once, on purpose, on a cover.

Pair by role.

- **Quiet luxury.** A neutral grotesk does almost all the work, set small and at regular weight, on warm paper. A serif appears on a single line, or not at all. This is the Aesop lesson: luxury here is not a Didot.
- **Cinematic dark.** A grotesk with a point of view (a heavy cut, a cap line, a tight measure). Credits may use a second, quieter face. Do not set the interface in a script or a high-contrast fashion serif.
- **Precise technical.** One grotesk for the UI. One mono for code, hashes, and columns of figures. Mono is not a heading face and not a vibe.
- **Editorial print.** A text serif for prose, a sans for captions and chrome. Or the reverse, if the product is a sans-first paper. Long UI labels are never display-serif.

If a commercial face is not licensed in the project, say so and use an open substitute or a system stack. Do not pretend Söhne, Suisse Int'l, or Riforma is available.

Open faces that do not currently read as a costume, when the layout is also specific: Newsreader, Public Sans, Source Serif 4, Source Sans 3, IBM Plex Sans, IBM Plex Serif, IBM Plex Mono, Literata, Schibsted Grotesk. Any of them becomes a tell on the generic skeleton. System stacks when you should not add a webfont: `system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` and `Iowan Old Style, Palatino, "Palatino Linotype", Georgia, serif` and `ui-monospace, "SF Mono", Menlo, Consolas, monospace`.

Faces that, in 2024–2026, usually mean "an agent styled this": Inter, Geist, Space Grotesk, Satoshi, Cabinet Grotesk, Clash Display, Plus Jakarta Sans, DM Sans, Instrument Serif, Instrument Sans, Playfair Display, Cormorant Garamond. They are allowed when the product already uses them as a real brand. They are not a way to buy taste.

### `type.two-families`

At most two families. Weights are not families. Italic is not a second brand voice.

**Test:** Count families. Three or more fails.

**Fix:** Give the extra role to a weight, a size, or small caps of a family you already use.

### `type.roles`

Each family has a written role. Display type does not appear in buttons, labels, or long text. Mono does not appear in marketing sentences.

**Test:** Find the family in a place outside its role. That fails.

**Fix:** Restyle that text in the family that owns the role.

### `type.scale-jumps`

The scale has visible jumps. A run of 14, 16, 18, 20, 22 is not a scale. Quiet pages often need something like 13 meta, 16 body, 28 title. Tools often live between 12 and 20. Editorial body on screen wants about 18px serif, with captions smaller, not a 72px headline as the only idea.

**Test:** If adjacent text styles are within 2px and the same weight, they are the same style. Collapse them or separate them by at least one clear step.

**Fix:** Delete the intermediate style. Make the subject actually larger, or keep one size and change weight only once.

### `type.leading-and-measure`

UI labels use a line-height around 1.25–1.4. Body uses 1.45–1.6. Display can sit between 0.95 and 1.2. Body never uses 1.0. Headings never use 2.0. Measure follows `spacing.measure`.

**Test:** A heading with loose leading, or body with tight leading, fails. So does a paragraph wider than the measure.

**Fix:** Set leading for the role. Cap the line length.

### `type.weight-budget`

Two or three weights in the product. Regular and medium cover most UI. Bold is emphasis, not the default heading treatment. Hairline weights below 16px fail on screens.

**Test:** Count weights. Four or more fails. A light weight under 16px fails.

**Fix:** Map extra weights back to regular or medium. Set display in regular or medium before you reach for bold.

### `type.tracking`

Large grotesk headlines may use slight negative tracking (about -0.02em at 40px and above). Positive tracking belongs to one eyebrow or a small-caps credit, not to every label. All-caps tracked labels on every field are a template.

**Test:** Count tracked or all-caps labels in the first screen. More than one eyebrow fails.

**Fix:** Sentence case. Save the tracked line for a single kicker, or delete it.

### `type.numbers`

Columns of numbers use tabular figures. Prose may use oldstyle figures if the family has them and the product is editorial. A list of prices aligns.

**Test:** A numeric column that jitters horizontally when the digits change fails.

**Fix:** `font-variant-numeric: tabular-nums` on that column, and right-align or decimal-align it.

### `type.license`

Do not ship a commercial font the project has not licensed. Name the substitute.

**Test:** The stylesheet names a commercial family with no license note and no files in the repo. That fails.

**Fix:** Use the open or system substitute and record the intended voice in one sentence.

### `type.avoid-tells`

Do not reach for a face on the costume list above unless it is already the product's brand.

**Test:** The family is on that list and the brand guide does not already specify it. That fails.

**Fix:** System stack or one of the quieter open faces, and spend the effort on structure.

---

## Density

Density is a decision about how many decisions fit on the screen. It follows the job.

A film title can be sparse: one still, one title, one action. A settings list is medium: grouped rows. A log or a ledger is dense: consistent rows, mono figures, almost no cards. Sparse is not a small card in a void. Dense is not cramped. Cramped means uneven padding, touching lines, and no group separation.

### `density.match-job`

The density matches the job named for this screen. A tool is not given marketing density (a giant headline and three claims). A brand homepage is not given tool density (a table of 12px metadata) unless the table is the brand.

**Test:** Compare the screen to the direction's density line in `directions.yaml`. A mismatch fails.

**Fix:** Change the structure to the job. Do not only scale the type down.

### `density.not-cramped`

Dense layouts still have a consistent row height, an aligned start edge, and a group gap from the scale. Lines of text do not touch.

**Test:** Rows vary in height for no content reason, or padding inside a row differs from row to row. That fails.

**Fix:** One row height. One horizontal inset. Wrap or truncate with a rule, and expose the full value another way.

### `density.not-empty`

Space belongs to a subject. A viewport whose content is a small centered card, three adjectives, and a gradient is empty, not sparse.

**Test:** If you removed the card chrome and the gradient, would a subject remain that deserves the margin? If not, it fails.

**Fix:** Bring in the real subject (image, text, list) at a size that holds the page, or reduce the viewport's ambition and make it a simple document.

### `density.repeat-rhythm`

Repeated objects share a template: same row height or same image ratio, same alignment, same meta position. Variation is in the content, not in the chrome.

**Test:** Sibling items differ in padding, radius, or title size. That fails.

**Fix:** One template. Let titles wrap to a fixed number of lines or reflow in the same grid.

### `density.no-bento-default`

A bento of uneven tiles is allowed when the content truly has different weights (one film and three credits). A bento of four equal marketing claims is a card grid in costume.

**Test:** The tiles could be reordered without changing meaning, and they say similar things. That fails.

**Fix:** One column of claims, or one strong tile and a plain list. Equal claims do not need tiles.

---

## Material and depth

Depth comes from one system. Tone steps, or a hairline, or a real material (paper, metal, a photograph). Not from stacking shadow, blur, and border.

The default surface is flat. A 1px hairline or a single tone step separates regions. A shadow appears when something is actually raised over the work: a menu, a dialog, a drag preview. One shadow style in the product, soft, low, tinted toward the surface temperature. Warm paper throws a warm shadow, not pure black.

Glass and blur are for a surface floating over moving or photographic content, such as a playback bar on a still. Glass on a flat gray page is costume.

Imagery is a material. If you have no photograph, no product, and no data, you have type and space. Do not invent a 3D blob, a gradient orb, or an abstract render to fill the hole.

Radius is a language. Quiet luxury and editorial work are square or barely rounded (0–2px). Tools round controls slightly (4–6px) and keep rows square. Cinematic work is square; the image is the shape. A large radius on every container (the `rounded-2xl` habit) makes a tool look like a toy.

### `material.one-system`

The screen uses one depth system. Flat plus hairline, or flat plus tone steps, or a photograph as the ground. Not all three plus shadow.

**Test:** Count devices used to separate regions (border, background step, shadow, blur). More than two fails.

**Fix:** Keep the one that matches the direction. Delete the others.

### `material.shadow-budget`

At most one shadow style, used only on overlays and dragged objects.

**Test:** A card, a button, and a page section all have shadows. That fails.

**Fix:** Remove shadows from in-flow elements. Keep one shadow on the menu or dialog.

### `material.no-nested-cards`

Do not put a card inside a card inside a modal unless each layer is a real navigation layer (a dialog over a page, a menu over a dialog).

**Test:** Two bordered, padded containers nested for decoration. That fails.

**Fix:** Flatten. Use a heading and a hairline.

### `material.radius`

One radius language, matching the direction. Controls may differ from the page, but sibling containers match each other.

**Test:** A button, a card, an input, and an image each have a different radius with no rule. That fails.

**Fix:** Set page geometry in the direction (usually square) and one control radius.

### `material.image-or-type`

Decorative abstract art is not a stand-in for content. Illustration is allowed when it is the product's actual voice and it is specific.

**Test:** A gradient orb, isometric blob, or generic 3D shape occupies the subject slot. That fails.

**Fix:** Use a real image, a real diagram of this product, or type and space.

### `material.hairline-before-box`

Prefer space, then a 1px hairline, then a background step. A full box is for a true object (a file, a product tile with an image) or an overlay.

**Test:** Every group is a bordered card and the groups are not repeated objects. That fails.

**Fix:** Remove the box. Separate with space or a hairline.

---

## Motion

Motion explains a change of state: where something came from, what opened, what updated. It is not a personality. A page that is still until someone acts feels more expensive than a page that performs on arrival.

Durations: 120–180ms for hover, press, and toggles. 200–320ms for a menu, drawer, or dialog. 400–700ms only when the motion is the content (a still crossfading, a title). Nothing loops unless it is live status or playback.

Easing: ease-out for entrances, ease-in for exits. No bounce, no elastic, no overshoot on product UI. A single spring is allowed on a physical control you drag.

Hover changes color, underline, or a hairline. It does not lift, scale, and shadow a card. Do not stagger a fade-up of every section on load. The content is readable immediately.

Respect `prefers-reduced-motion`. When it is set, do not transform and do not parallax. Opacity changes, if any, stay under 150ms. Essential information is never only in motion.

Custom cursors, magnetic buttons, and cursor trails are refused unless the product is explicitly an experiment and that effect is the point.

### `motion.purpose`

Every animation answers a state change. If nothing changed, nothing moves.

**Test:** An element moves on load or on a timer without representing live data. That fails.

**Fix:** Remove it. If the motion was hiding a slow load, use a skeleton that matches the final layout.

### `motion.timing`

State changes sit in the ranges above. Loops are reserved for live status and playback.

**Test:** A transition longer than 320ms on a menu, or a bouncing easing, fails.

**Fix:** Shorten and use ease-out or ease-in.

### `motion.no-load-theater`

The page does not introduce itself with staggered fades, slides, or typewriter text.

**Test:** Content is invisible until an entrance finishes. That fails.

**Fix:** Render the content. Animate only the next user-caused change.

### `motion.reduced`

`prefers-reduced-motion: reduce` removes transforms and long fades.

**Test:** No media query or equivalent, and the page animates. That fails.

**Fix:** Gate motion behind the media query. Keep state changes instant or under 150ms opacity.

### `motion.hover`

Hover is a color, an underline, or a border change. Not a lift, a scale, and a shadow together.

**Test:** `:hover` sets `transform` or `box-shadow` on in-flow cards. That fails.

**Fix:** Change ink or hairline only.

---

## Uniqueness

Uniqueness comes from the product's own material: its objects, its data, its words, its one structural idea. It does not come from a new gradient on the shared layout.

Have one idea per page. A full-bleed still with a caption column. A list that is the navigation. A prose column with a margin note. A table that is the product. Not a tour of every layout trick you know.

Agents share a skeleton. Refuse it unless the user explicitly asks for a conventional marketing page, and even then break the hero and the feature row.

```
skeleton.saas-landing
1. Nav: logo left, links center or right, filled button at the end
2. Centered hero, gradient or oversized headline, dek, two buttons
3. Logo cloud ("trusted by")
4. Three feature cards, each an icon in a tinted square, a title, a sentence
5. Bento of more features
6. Testimonials with avatars
7. Pricing trio, middle column highlighted
8. FAQ accordion
9. Footer with four columns of links
```

A dashboard costume is the other shared skeleton: left sidebar, four statistic cards, a chart, a table, a greeting ("Good morning, Alex"). Use that structure only when the user monitors those numbers every day, and give the numbers a real unit and a real source.

Before you style, write the sentence the page is allowed to say. Use words from the domain. "Ash glaze, 18 cm, ships in a week." "Retry delay on the preview proxy." Not "Seamless workflows for modern teams."

Load one reference, then change three things that belong to this product: the structure of the content, the material (photo, data, or type role), and the density. Copying the reference's palette onto a card grid is a costume.

One memorable detail is enough. A numeral style. A caption rule. A specific empty state. Details compound. Effects do not.

### `uniqueness.one-idea`

The page has one structural idea, nameable in a sentence.

**Test:** You cannot finish "This page is ___." without listing features. That fails.

**Fix:** Choose the idea that serves the job. Delete sections that do not serve it.

### `uniqueness.refuse-skeleton`

The screen does not follow `skeleton.saas-landing` or `layout.dashboard-costume` unless that structure is honestly the product, and even then the hero or the stat row is rebuilt from real content.

**Test:** Check the first screen against the list above. A match on the hero plus the three feature cards fails.

**Fix:** Replace the structure using the direction's `first_screen` recipe. Then add back only the content you still need.

### `uniqueness.specific-copy`

Copy uses concrete nouns from this product. It does not rely on Elevate, Unlock, Seamless, Next-gen, "your workflow," or "delightful experience."

**Test:** Read the headline and the first paragraph out loud. If they could sit on a hundred other sites, they fail.

**Fix:** Replace them with the fact a customer would use to decide.

### `uniqueness.one-detail`

One crafted detail, related to the product. Not a handful of effects.

**Test:** List the "special" moves (gradient, blob, custom cursor, staggered motion, unusual font, glow). Two or more fails.

**Fix:** Keep the one that carries meaning. Delete the rest.

### `uniqueness.diverge-from-reference`

The reference supplies a structure. The product supplies the content and at least one decision the reference would not make (a different density, a different material, a different action).

**Test:** Swapping the logo and the palette is the only change from the reference, or from a template. That fails.

**Fix:** Rebuild around this product's object or data. Keep the lesson, drop the costume.

---

## Product fit

The direction serves the job. Quiet luxury fits objects, places, and slow reading. It makes a bad log viewer: there is nowhere for the rows to go. Cinematic dark fits works in a room. It makes a bad form: fields, errors, and labels drown. Precise technical fits instruments. It makes a bad perfume page if it turns the bottle into a table. Editorial print fits an essay. It makes a bad settings screen.

A product can use two registers. A quiet catalog page and a precise order list may share temperature and type, and they should not share density. Do not paste the homepage hero into the app.

Voice matches the UI. A blunt tool does not whisper in tracked small caps. A slow object does not shout with badges.

### `product.sentence`

You can write: "This is a [job] for [who], and it should feel like [reference], because [structural reason]."

**Test:** The because-clause mentions only a mood word (premium, modern, cinematic, clean). That fails.

**Fix:** Name a structure. "Because the bowl is the subject and the facts sit in a narrow column."

### `product.direction-serves-job`

The chosen direction's jobs list includes this screen's job, or the mismatch is deliberate and written down.

**Test:** A form or a data table in cinematic-dark, or a film still treated as a precise-technical admin row with no still, fails the unexamined case.

**Fix:** Switch direction for this screen, or state why the mismatch is the product (a night-time listing can be dense and dark; that is Resident Advisor, and it is still a listing).

### `product.two-registers`

Marketing and the working product may differ in density. They share temperature and type family. They do not share the hero.

**Test:** The app's first screen is the marketing hero, shrunk. That fails.

**Fix:** Start the app on the repeating object or the document. Leave the manifesto on the marketing page.

### `product.precedence`

Follow the precedence at the top of this document. Brand tokens do not excuse a broken hierarchy. These principles do not repaint a brand that was explicitly requested.

**Test:** You overrode an explicit brand color, or you kept a gradient hero because the brand guide showed one and the user asked you to remove it. Either one fails.

**Fix:** Restore the winner named in the precedence list. Say which rule you followed.

---

## Accessibility

Accessibility is part of finish. Low-contrast gray, tiny tracked navigation, and hover-only actions read as careless, not as refined. The references include a few famous small sizes (Aesop's label-like body). Do not import those. On screen, reading text stays at least 14px, long-form at 16–18px.

### `a11y.contrast`

Same bar as `color.contrast`. Placeholder text, disabled text, and text on images included. Text on a photograph has a solid panel or a scrim that actually hits the ratio, not a vague dark gradient.

**Test:** Muted text, placeholder, and text-on-image below the ratios fail.

**Fix:** Darken, add a solid ground behind the type, or move the type off the image.

### `a11y.focus`

A visible focus ring, at least 2px, offset from the control, in ink or the accent. Designed once and reused. Never remove an outline without a replacement.

**Test:** Tab through the screen. Any control that does not show focus fails.

**Fix:** `:focus-visible` with a 2px offset ring. Do not rely on color change alone.

### `a11y.targets`

Pointer targets are at least 24px, and 40px for a primary touch control. Dense tool rows may be 32px tall when a keyboard path exists and the type still meets `a11y.size`.

**Test:** A clickable row or icon under 24px fails.

**Fix:** Expand the hit area, even if the visible glyph stays small.

### `a11y.size`

Reading text is at least 14px. Long-form is at least 16px. Meta can be 12–13px only with contrast at or above 4.5:1 and never for the primary action.

**Test:** A paragraph under 14px, or an action under 14px, fails.

**Fix:** Raise the size. Shorten the line if the column feels loud.

### `a11y.not-color-alone`

State is a word or a mark plus color. Sold out, failed, selected, and required are readable in grayscale.

**Test:** Hiding the color leaves a state ambiguous. That fails.

**Fix:** Add the word or a marker in the same place every time.

### `a11y.names`

Buttons say what they do. "Reserve from this firing", not "Continue" for everything. Icon-only buttons have an accessible name. Placeholder text is not the only label.

**Test:** A control whose accessible name is "button", an icon, or a placeholder fails.

**Fix:** Visible label, or an accessible name that matches the visible text.

### `a11y.errors`

Errors sit at the field, say what to do, and are not color alone. The message is specific.

**Test:** A red border with no message, or a toast that says "Something went wrong", fails when you know the cause.

**Fix:** "The firing is full. Join the next one." next to the field.

### `a11y.order`

Reading order and tab order follow the visual order. CSS reordering that breaks the sequence fails.

**Test:** Tab through the page with the stylesheet's visual order in mind. A jump fails.

**Fix:** Put the DOM in the visual order. Use layout that does not reorder meaning.

---

## Anti-patterns

Each id is specified in [`anti-patterns.yaml`](anti-patterns.yaml). The catalog below is the short form. If a screen matches one, the critique names it and replaces the structure. Do not "polish" it with a new font.

| Id | What you see | The move |
| --- | --- | --- |
| `skeleton.saas-landing` | The numbered skeleton in Uniqueness | Rebuild from the direction's first screen |
| `layout.dashboard-costume` | Sidebar, four stat cards, chart, table, greeting | Start from the repeating object |
| `layout.equal-cards` | Every idea in an identical card | One column, or a list of real objects |
| `layout.nested-cards` | Card inside card | Heading and a hairline |
| `layout.center-stack` | Every block centered | One start edge |
| `layout.bento-claims` | Uneven tiles of similar sentences | A list or one strong tile |
| `color.aurora` | Mesh, gradient text, glow | Flat surface, color in the content |
| `color.indigo-default` | Indigo on white, Inter or Geist, no other idea | Change the structure first |
| `color.gold-on-black` | Gold rules, Didot or Playfair, pure black | A real material, or a night room with a real work |
| `color.rainbow-pills` | Saturated status badges | A word and a quiet mark |
| `type.three-voices` | Display, serif, mono, and a script | Two families, with roles |
| `type.all-caps-everything` | Tracked caps on every label | One kicker, or none |
| `type.tiny-gray` | Gray body "for elegance" | Mute one step, keep 4.5:1 |
| `material.gray-card-shadow` | `gray-50` page, white `rounded-2xl` cards, `shadow-sm` | Flat paper, hairlines, real margin |
| `material.glass-on-flat` | Blur card on a flat gradient | Delete the glass |
| `material.icon-tile` | Icon in a tinted rounded square, title, sentence | A sentence, or a real object |
| `motion.stagger-fade` | Sections fade up on load | Content is there immediately |
| `motion.hover-lift` | Cards scale and shadow on hover | Recolor or underline |
| `content.fake-proof` | Gray logo cloud, "10,000+ teams", stock praise | A real fact, or nothing |
| `content.abstract-verbs` | Elevate, Unlock, Seamless, Next-gen | Nouns from the domain |
| `chrome.two-primaries` | Two filled buttons | One filled, one text |
| `chrome.badge-pile` | New, AI, Pro, Beta on one title | One fact, in the title or under it |
| `chrome.sparkle` | A sparkle icon as the concept | The product's object |
| `a11y.placeholder-label` | Placeholder is the only label | A visible label |
| `a11y.focus-removed` | No focus ring | A 2px offset ring |

---

## How to use this on a real change

1. Write `product.sentence`.
2. Pick one direction. Read its `first_screen`.
3. Read one reference. Write down the one decision you are stealing, and one you are not.
4. Lay out the subject, the support, and the action before you choose a color.
5. Check the anti-pattern table against the first screen.
6. Run the critique skill. Apply structural fixes first.
7. Stop when each critique dimension is at least 4, or after two revision passes. Then report what still fails.

Tokens, if you need them, come last. Example identities for two directions are in [`tokens/`](../tokens/).
