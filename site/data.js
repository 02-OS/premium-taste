// Generated from taste/ and tokens/ by scripts/build_site_data.py.
window.PREMIUM_TASTE_DATA = {
  "counts": {
    "principles": 62,
    "antiPatterns": 25,
    "references": 18,
    "directions": 4
  },
  "directions": [
    {
      "id": "quiet-luxury",
      "name": "Quiet Luxury / High-end Minimal",
      "temperature": "warm paper, stone, or graphite. Never pure white with a saturated accent.",
      "density": "sparse to moderate. One object or one short text column earns a large margin.",
      "type": "a quiet grotesk for almost everything. A serif only if a single line needs a literary register. Regular weight. Modest sizes.",
      "material": "square or nearly square corners, hairlines, almost no shadow. Photography or the object carries warmth.",
      "jobs": [
        "object retail",
        "hospitality",
        "culture",
        "studio or personal site",
        "a single product"
      ],
      "refuses": [
        "gold-on-black",
        "Didot or Playfair as a luxury costume",
        "badge stickers",
        "a tinted icon above every sentence",
        "body text below 14px, even if a reference prints smaller"
      ],
      "references": [
        "aesop",
        "cos",
        "are-na",
        "hermes",
        "muji"
      ],
      "first_screen": "A stable header with a wordmark and text links. Then one spread: a large still of the object (or one text column, if the product is an idea) and a narrow column with a factual label, a title at regular weight, one specific paragraph, the price or fact, and one quiet action. No card around that column."
    },
    {
      "id": "cinematic-dark",
      "name": "Cinematic Dark",
      "temperature": "a night room. Black or near-black is the room, not a theme toggle. Color comes from the work (a still, a poster, a red signal), plus at most one action color.",
      "density": "the subject is large. Controls are small and in a stable place. Listings can be dense if each row is a real event.",
      "type": "a grotesk with a point of view (caps, weight, or a heavy cut). A second family only for a credit line. Measure the title hard so it does not span the viewport.",
      "material": "square corners, full-bleed stills, bands or rows. The dark field is flat. Do not add a purple glow to make it \"cinematic\".",
      "jobs": [
        "film or video",
        "music and nightlife",
        "a single listening or watching surface",
        "a catalog of works"
      ],
      "refuses": [
        "a dark-mode form with indigo buttons",
        "gold foil",
        "gradient meshes",
        "glass cards floating on a glow",
        "a black background with no work on it"
      ],
      "references": [
        "mubi",
        "resident-advisor",
        "criterion",
        "sonos"
      ],
      "first_screen": "One work occupies most of the first screen, or the first screen is a night listing whose rows are the works. The title, a credit, and one action sit on the work or in a hard column beside it. Chrome is a wordmark and a few links. If you turn the still off, the page should look like an empty room, not like a dashboard."
    },
    {
      "id": "precise-technical",
      "name": "Precise Technical",
      "temperature": "cool paper or a neutral gray step. Ink is near-black. Status colors are few and they mean a state.",
      "density": "moderate to dense. Repeated objects share a row height. The page is a tool, so margin is padding, not a gallery wall.",
      "type": "one grotesk for UI, one mono for identifiers. Sizes sit in a narrow range (12–20px) with weight and position doing the hierarchy. Links are ink with an underline, not a new hue, unless the product brand already has a link color.",
      "material": "1px hairlines, 0–6px radius on controls only, rows flush. Shadow appears on an overlay, not on every row.",
      "jobs": [
        "repeated decisions",
        "configuration",
        "documentation",
        "a data list or log",
        "a creation tool",
        "writing",
        "a machine you inspect part by part"
      ],
      "refuses": [
        "four KPI cards above a table that repeats the same numbers",
        "a marketing hero on a tool",
        "rainbow status pills",
        "mono used as decoration on marketing sentences"
      ],
      "references": [
        "things-3",
        "figma",
        "stripe-docs",
        "ia-writer",
        "teenage-engineering"
      ],
      "first_screen": "The name of the tool and the name of the collection (Revisions, Layers, Today). Then the repeating object itself, in aligned rows or a document column. A writing surface is the column with the library hidden. An instrument page is one machine and a spec list aligned to it. Status is a word. One filter or one compose control. No stat strip."
    },
    {
      "id": "editorial-print",
      "name": "Editorial Print",
      "temperature": "paper and ink. Photography supplies the other colors. Rules are 1px and the color of the ink or a soft gray.",
      "density": "a spread. Large space, a reading measure, captions smaller than body. An essay gets hierarchy from space. A newspaper front may use headline size, width, and position to rank stories.",
      "type": "a text serif for prose, a sans for captions, navigation, and credits. Ragged right. Body around 18px on screen. Do not justify on the web.",
      "material": "columns, rules, margin notes. No cards around paragraphs. Images bleed or sit in a clear grid. Corners on images are square.",
      "jobs": [
        "essay",
        "magazine story",
        "catalog essay",
        "interview",
        "a newspaper front",
        "a briefing"
      ],
      "refuses": [
        "a hero with a gradient scrim and a centered headline over every story",
        "pull quotes in a colored card",
        "a three-card \"related\" row as the whole idea",
        "drop caps plus three other display tricks on the same page"
      ],
      "references": [
        "cereal",
        "financial-times",
        "new-york-times",
        "monocle"
      ],
      "first_screen": "A masthead in small type. An essay continues as a full image with a factual caption, or a text column of about 65–72 characters with the title only modestly larger than the body. A newspaper front ranks several stories by headline size, column width, and position, on one paper color, with rules instead of cards. Navigation is a section, a search, or a few words, not a product bar of buttons."
    }
  ],
  "references": [
    {
      "id": "aesop",
      "title": "Aesop",
      "url": "https://www.aesop.com",
      "direction": "quiet-luxury",
      "job": "buy a physical good",
      "tags": [
        "retail",
        "paper",
        "photography",
        "square-corners",
        "small-type",
        "grotesk"
      ],
      "summary": "A warm ivory ground and charcoal text. Product photographs do the warming: amber glass, botanicals, a taupe studio wall. Buttons, fields, and product tiles are square. Headlines are not large. Body copy is small, close to a printed label, and it is specific about the formula. Navigation is a store, not a campaign. There is little badge language and little promotional chrome.",
      "steal": [
        "A warm paper surface and an ink that is charcoal, not pure black.",
        "Square geometry.",
        "A grotesk at regular weight, set smaller than a marketing hero. One serif line at most, or none.",
        "A product column that reads like a label: name, form, size, then a paragraph a person could use.",
        "Photography as the only decoration. Consistent grounds, not a new treatment per product."
      ],
      "avoid": [
        "Body sizes at 12px. That is part of their label density and it fails `a11y.size`. Keep the *relationship* (meta smaller than body, body quieter than the picture) and set reading text at 14px or above.",
        "Suisse Int'l, unless you have licensed it. A system grotesk or Public Sans can hold the same role. The role is the lesson.",
        "Their exact ivory hex on a product that is not paper-like. A cold software tool on `#fffef2` looks costume.",
        "A full catalog grid pasted under an unrelated hero. Steal the column, not the whole store."
      ]
    },
    {
      "id": "cos",
      "title": "COS",
      "url": "https://www.cos.com",
      "direction": "quiet-luxury",
      "job": "look at a garment",
      "tags": [
        "fashion",
        "photography",
        "architecture",
        "factual-type",
        "neutrals"
      ],
      "summary": "Garments in a real place. A warehouse, a quarry, a city street, a shoreline. The palette of a given season is narrow (black, navy, stone, brown, the cloth itself) and it changes with the collection, while the chrome stays quiet. Photography is large. Type, when it appears on campaign graphics, is a clean sans set small and factual: season, place, date. The cut and the cloth are the event. There is no decorative monogram doing the work.",
      "steal": [
        "An image-to-type ratio where the picture is the subject and the type is a caption.",
        "A neutral ground so the product's own color is the accent.",
        "Factual microcopy: material, place, season, price. Not a slogan above the picture.",
        "A stable frame, so that when the object changes the page still feels like the same house.",
        "One crafted difference in the object, which means your UI should not add a second crafted difference."
      ],
      "avoid": [
        "A fashion photograph you do not have. An empty beige page with a thin sans is not COS. That fails `density.not-empty`.",
        "\"Scandi minimal\" as a theme: warm gray, a centered logo, three lookbook cards with rounded corners.",
        "Seasonal campaign color dragged into buttons and badges.",
        "Their retail information architecture, unless you are actually selling a collection."
      ]
    },
    {
      "id": "are-na",
      "title": "Are.na",
      "url": "https://www.are.na",
      "direction": "quiet-luxury",
      "job": "collect and connect research",
      "tags": [
        "tool",
        "defaultness",
        "blocks",
        "content-is-the-color",
        "one-family"
      ],
      "summary": "A paper-white field, graphite text, thin boundaries, almost no chrome. Channels are grids of blocks. The color on the page is whatever the members saved. A 2026 capture of the editorial column describes a single type size near 19px, one family, and a rare deep navy used as an accent. The family is Areal, drawn by Dinamo and released in 2025 as a ground-up redraw of Arial.",
      "steal": [
        "A single repeating unit that *is* the layout.",
        "One family, with hierarchy from weight and placement.",
        "A frame so quiet that user content supplies the color.",
        "The discipline of looking almost default, on purpose, when the content is the point.",
        "A short written reason for the default, so later edits do not \"upgrade\" it into a theme."
      ],
      "avoid": [
        "Inter or Inter Tight as a stand-in, dropped onto a marketing skeleton. The substitute is not the lesson. The block grid is the lesson. Those faces are also on the costume list in `type.avoid-tells`.",
        "Emptiness with no unit. Are.na without blocks is a blank page.",
        "Their navy accent, copied as a brand color for a shop. It is rare because the blocks are busy.",
        "Areal itself, unless you license it. Use a system sans and spend the specificity on the structure."
      ]
    },
    {
      "id": "hermes",
      "title": "Hermès",
      "url": "https://www.hermes.com",
      "direction": "quiet-luxury",
      "job": "look at an object from the house",
      "tags": [
        "maison",
        "photography",
        "achromatic-chrome",
        "square-corners",
        "object-color"
      ],
      "summary": "A house shop. Product photographs carry the orange of the box, the ribbon, and the goods. The interface around those photographs stays achromatic: ink, a white or near-white ground, and the carriage drawn as linework. A May 2026 public capture of the live shop describes square corners and one custom face at a regular weight, set small. Campaign layers sit on top of that shop and then leave. In 2026 the house has commissioned illustrated skins for the site rather than leaving every visit as a bare catalog.",
      "steal": [
        "Withhold a signature color from chrome. Let the object, photographed consistently, carry it.",
        "A square, quiet frame: wordmark, a few text links, then the object.",
        "One family, regular weight, smaller than a marketing hero.",
        "A campaign that is clearly a campaign: illustration with a season, then back to the shop. Do not leave the illustration on as the permanent skin."
      ],
      "avoid": [
        "Body type near 12px, if a capture shows it. Keep the relationship (the picture louder than the paragraph) and set reading text at 14px or above (`a11y.size`).",
        "Any unofficial orange hex. Published values disagree, and the house does not give this file a web token. Do not pick one and call it Hermès.",
        "A different \"Hermès design system\" that specifies Inter, or any other grotesk, as the site. That is not hermes.com.",
        "Orange buttons, orange underlines, and an orange wordmark on a white card grid. That is the costume of the decision.",
        "The illustrated homepage as a component kit. It is a commissioned drawing for a moment."
      ]
    },
    {
      "id": "muji",
      "title": "MUJI",
      "url": "https://www.muji.com",
      "direction": "quiet-luxury",
      "job": "choose a plain object",
      "tags": [
        "retail",
        "label",
        "material",
        "no-signature-color",
        "plain-pack"
      ],
      "summary": "Objects named for a material and a use. A polypropylene case, a cotton shirt, a notebook. Packaging is plain and uniform, and it carries a product fact and a price rather than a slogan or a designer credit. Stores put those objects in reach, in bulk, on unadorned fixtures. The company's own account, unchanged in substance since 1980, gives three manufacturing rules: choose the material, cut the process steps that do not change quality, and simplify the package.",
      "steal": [
        "Name the object by material and function, then stop.",
        "One quiet ground. Let the material of the product be the variation between items.",
        "A label, not a badge: what it is, a size, a price.",
        "Removal with a reason. If a step does not change the object, it is not on the page either: no icon tile, no promotional ribbon, no second button."
      ],
      "avoid": [
        "A beige theme on the generic skeleton. Beige is not the lesson. The lesson is that the object states itself.",
        "Emptiness. A page with no object, no material, and no price is not MUJI. It is unfinished.",
        "An invented hex or an invented house font. This file has neither.",
        "Their full catalog grid under an unrelated hero. Steal the label.",
        "Treating \"no logo\" as a reason to remove the name of the product. The product name stays."
      ]
    },
    {
      "id": "mubi",
      "title": "MUBI",
      "url": "https://mubi.com",
      "direction": "cinematic-dark",
      "job": "enter a film journal",
      "tags": [
        "film",
        "bands",
        "stills",
        "square-corners",
        "one-action-color",
        "grotesk"
      ],
      "summary": "Full-bleed bands that alternate between a black room and a white page. Film stills occupy the black bands. Type is one grotesk, Riforma, including uppercase display lines at a regular-to-medium weight. Corners are square. Public captures in 2026 report a deep cobalt near `#001489` used for the action (a join button, an inline link) and a red near `#d71b1d` reserved for the print magazine, not sprinkled through the UI. The stills are saturated. The chrome is black, white, and that one blue.",
      "steal": [
        "Alternating rooms: a night band only where an image is the subject, a paper band where the text is the subject.",
        "One grotesk with a clear display register (case, size) and a quieter text register.",
        "Square tiles and square buttons.",
        "One deep, slightly strange action color, used a few times, not a rainbow of CTAs.",
        "A headline that states the product in plain words, set as type, not as gradient lettering."
      ],
      "avoid": [
        "Riforma, unless licensed. Any plain grotesk can take the role. Do not \"upgrade\" it to a fashion serif.",
        "Uppercase on every heading, button, and label (`type.all-caps-everything`). Keep caps for the display line.",
        "A black page with no still, plus a cobalt button. That is the skeleton in a dark coat.",
        "Their exact cobalt on a product that is not this journal.",
        "The streaming-library pattern of infinite poster shelves, which this note is not recommending. The lesson is the journal band."
      ]
    },
    {
      "id": "resident-advisor",
      "title": "Resident Advisor",
      "url": "https://ra.co",
      "direction": "cinematic-dark",
      "job": "find an event tonight",
      "tags": [
        "nightlife",
        "listings",
        "dense",
        "black",
        "red-signal",
        "type-led"
      ],
      "summary": "A black room, off-white type, and a bright red used as a signal. A third-party brand capture lists the red near `#FF4848` with black and an off-white; treat that as a hint, not a specification. The content is a list: city, date, venue, artist. Editorial pages use heavy grotesk headlines and photography of artists and rooms. Icons are few. The density is high because the night is a schedule, not a poster.",
      "steal": [
        "A night surface justified by the content's context.",
        "Rows with a stable order of facts: time, place, name.",
        "One saturated signal color on a field that is otherwise black and off-white.",
        "Heavy type for the name, quieter type for the metadata, same family.",
        "The courage to be dense when the user is scanning a schedule."
      ],
      "avoid": [
        "Pure `#000` and pure `#fff` as the default dark theme. For anything read at length, lift the black and dim the white (`color.dark-surfaces`). RA accepts the glare as a poster. Your settings screen should not.",
        "Red on every link, icon, and badge. Then it is no longer a signal.",
        "A brutalist listing for a product with nothing to list. Empty rows in a black void fail `density.not-empty`.",
        "Gold, blur, or a glow added \"so it feels premium.\" That undoes the listing.",
        "The brand's red hex on an unrelated product."
      ]
    },
    {
      "id": "criterion",
      "title": "Criterion Collection",
      "url": "https://www.criterion.com",
      "direction": "cinematic-dark",
      "job": "choose a film from a library",
      "tags": [
        "film",
        "library",
        "spine-number",
        "essay",
        "stills",
        "stable-frame"
      ],
      "summary": "A library, not a storefront. A film is a spine number, a title, a still or a poster, a credit, and often an essay. The frame is black and white with the Criterion C. Color comes from the art of that film. Collection graphics made for the Channel are designed per program (a theme, a star, a period) in a 16:9 hero and further crops. The frame stays recognizable. The picture changes with the subject.",
      "steal": [
        "A stable row or spine: identifier, title, one meta line, one image.",
        "An essay or a program note set in a reading column, with the still separate from the text.",
        "Per-item art direction inside a frame you do not restyle every time.",
        "Black and white as the shelf, so the film's own palette stays intact.",
        "An identifier a person can say out loud (\"spine 584\"), if your catalog has a real one."
      ],
      "avoid": [
        "Gold rules, a fake \"EST.\" line, and letterspaced small caps on a SaaS hero. That is `color.gold-on-black` wearing a film costume.",
        "A black theme with no works in it.",
        "The C, the spine device, or their essay voice. Those are the brand. The lesson is \"a catalog has a frame and a text.\"",
        "A carousel of posters with the titles over a scrim, which throws away the frame's alignment.",
        "Treating every customer as a curator. The point of view has to be the product's, in specific words."
      ]
    },
    {
      "id": "sonos",
      "title": "Sonos Now Playing",
      "url": "https://www.sonos.com",
      "direction": "cinematic-dark",
      "job": "see what is playing",
      "tags": [
        "listening",
        "artwork",
        "now-playing",
        "one-work",
        "caution"
      ],
      "summary": "One piece of album art, large, and the name of the track, the artist, and the transport in a stable band. Partner documentation for the app describes that art as square on Now Playing, and it tells partners to keep a default image from disappearing into the app grounds it names: light near `#D8D8D8`, dark near `#262626`. Reporting in July 2026 describes an update that tints the Now Playing background from the album art. The picture remains the picture. The ground, when it takes color, is a sample of that picture.",
      "steal": [
        "One artwork, large enough to identify, with title and artist in a quiet face beside or below it.",
        "A dark field that stays dark when the art is missing. Sample color from the art only while the art is visible, and keep it duller than the art.",
        "Transport as a small, stable row. One primary control (play or pause). The rest are quieter.",
        "Square art, or a consistent crop. Do not invent a new frame per title."
      ],
      "avoid": [
        "The Home screen of service tiles, pinned rows, and sources. That is a hub. It is also the surface people objected to. Do not treat it as taste.",
        "A full-screen gradient or a blurred blow-up that stands in for the sleeve. The art has to remain the art.",
        "Gold, a glow behind the controls, or a second accent for \"music.\"",
        "The partner hexes `#D8D8D8` and `#262626` as a brand palette. They are grounds a default image must not match. They are not tokens to paste.",
        "The whole app as an example of finish. Use this file for the listening room only. For a night listing, load Resident Advisor. For a library of works, load Criterion."
      ]
    },
    {
      "id": "things-3",
      "title": "Things 3",
      "url": "https://culturedcode.com/things/",
      "direction": "precise-technical",
      "job": "see what to do today",
      "tags": [
        "tasks",
        "rows",
        "platform-type",
        "one-compose",
        "section-color"
      ],
      "summary": "A calm light window. Tasks are rows, not cards. A checkbox column aligns down the list. The title is the user's own words, in the platform sans. Tags, dates, and notes sit quieter than the title, on the same row or just under it. Sections have colored headings: Today reads as a warm red, This Evening as a yellow, and later sections step down. Areas can carry a color the user chose. There is one compose control, the plus, rather than a hero button. Completing a task is a small check, not a page transition. The window does not look like a website.",
      "steal": [
        "Rows for repeated text objects. Cards only when the object has a real body (an image, a document).",
        "One compose control.",
        "Color tied to a user-meaningful group, used in the heading, not in a badge on every row.",
        "A platform or system sans for a tool whose content is the user's writing.",
        "A small, specific confirmation when an action completes.",
        "Section gaps that are clearly larger than the gap inside a section."
      ],
      "avoid": [
        "The Today red and the Evening yellow as a brand palette for a bank or a store. Those hues mean time of day inside this app.",
        "A sidebar plus a plus button pasted onto a marketing page (`product.two-registers`).",
        "\"Craft\" as a drop shadow and a blur. Things is flat and aligned.",
        "Their information architecture (Today, Upcoming, Anytime, Someday, Areas) unless the product is actually a personal task list.",
        "A second accent for tags, priorities, and icons. The heading color is already the accent."
      ]
    },
    {
      "id": "figma",
      "title": "Figma editor",
      "url": "https://www.figma.com",
      "direction": "precise-technical",
      "job": "edit a design on a canvas",
      "tags": [
        "tool-chrome",
        "panels",
        "hairline",
        "selection-color",
        "compact-type"
      ],
      "summary": "A neutral gray canvas surrounded by panels: layers on one side, properties on the other, a toolbar along an edge. Panels are separated by tone steps and 1px borders, not by cards. UI type is compact, around the size of a label, in a neutral sans. Icons in the chrome are monochrome and one weight. The accent is the selection color, a clear blue, used when an object is selected and for a few related controls. The work on the canvas is the color. The chrome is there to be ignored until you need a control.",
      "steal": [
        "Tone-on-tone panels and 1px hairlines.",
        "One selection color that is not also the brand wallpaper.",
        "A properties pattern: aligned labels, one control height, groups separated by a gap or a hairline.",
        "Monochrome toolbar icons.",
        "Compact UI type (12–14px) only where the user is operating, not where they are reading prose. Keep `a11y.contrast` and do not put a paragraph at 11px.",
        "A hard line between the marketing register and the tool register."
      ],
      "avoid": [
        "This panel layout on a blog, a shop, or a landing page. A properties sidebar next to an essay is a costume.",
        "Tiny type for reading. Compact is for controls.",
        "A second and third blue. Selection, links, and primary actions can share one hue; illustrations on the canvas do not count against the budget.",
        "The marketing site's illustrations, gradients, or campaign type, imported into a tool \"for consistency.\"",
        "Figma's specific blue as your brand accent. The lesson is the role, not the paint."
      ]
    },
    {
      "id": "stripe-docs",
      "title": "Stripe Docs",
      "url": "https://docs.stripe.com",
      "direction": "precise-technical",
      "job": "read and copy a technical document",
      "tags": [
        "docs",
        "measure",
        "toc",
        "code-as-material",
        "three-zones"
      ],
      "summary": "Three zones. A navigation column of the documentation, a reading column with a title and a short dek, and a rail of the headings on this page. Prose has a measure. Code sits in a quiet well, visually a different material from the paragraph, and it is something you are meant to copy. Language choice is a control for the sample, not a visual motif. The page is a document: title, introduction, then sections. There is no hero, no logo cloud, and no feature grid.",
      "steal": [
        "Title, one-sentence dek, then the document. No hero.",
        "A measured column. A contents rail only if the page is long enough to need one.",
        "Code or data samples on a separate surface, in mono, with the surrounding prose in the text family.",
        "Navigation that is a catalog of the docs, not a brand bar of product links.",
        "The separation between a graphic marketing page and a reading page."
      ],
      "avoid": [
        "The indigo or blurple, unless you are Stripe. On a new product it trips `color.indigo-default`.",
        "Three columns on a short page. A rail of two links is clutter. Use the rail when the document has real sections.",
        "This layout for a film, a bowl, or a task list. A table of contents beside a still is a mismatch (`product.direction-serves-job`).",
        "Gradient bands, glowing buttons, or the stripe.com homepage illustration style, \"to make the docs feel like the brand.\"",
        "Tabs, callouts, and cards on every paragraph. One callout style, used when the reader will be hurt if they miss it."
      ]
    },
    {
      "id": "ia-writer",
      "title": "iA Writer",
      "url": "https://ia.net/writer",
      "direction": "precise-technical",
      "job": "write the next sentence",
      "tags": [
        "writing",
        "column",
        "focus",
        "one-family",
        "chrome-leaves"
      ],
      "summary": "A text column. The library is a list of files, and it can be hidden. Focus Mode, documented for the current apps, dims every sentence except the one at the cursor, or every paragraph except the current one. A separate typewriter option keeps the cursor vertically centered and does not dim the text. Statistics (words, characters, a reading time) can be turned off. The type in the column is one of their writing faces: iA Writer Mono, Duo, or Quattro. Duo is duospace. Quattro keeps wide word spacing and monospaced punctuation while letting a few letters take different widths. They were built from IBM Plex and published for other people to use. The toolbar does not compete with the paragraph.",
      "steal": [
        "A single readable column, with the file's name and almost nothing else above it.",
        "A library that is a list, shown when you are choosing a file and gone when you are writing.",
        "Focus as type color: the current sentence in ink, the rest in a muted ink that still clears contrast (`color.contrast`). Do not blur the page.",
        "One text face drawn for long reading. Mono if the writing benefits from alignment. A proportional face if it does not.",
        "Preferences for the apparatus (stats, syntax color) so the default can stay quiet."
      ],
      "avoid": [
        "Rebuilding iA Writer. They have said not to. Use the idea in a product that has its own documents.",
        "Their faces on a marketing hero. The faces are for a column of writing (`type.license` still applies if you ship them; read their license).",
        "A hex from memory. This file does not record the app's colors. Light text on a light ground and the reverse are both offered. The identity is the column, not a theme.",
        "Focus Mode that removes the paragraph you need to edit. Dimming is the move. Deleting the context is not.",
        "A fake \"distraction-free\" landing: a giant wordmark, a gradient, and a download button. That is the page their chrome is trying to get away from."
      ]
    },
    {
      "id": "teenage-engineering",
      "title": "Teenage Engineering",
      "url": "https://teenage.engineering",
      "direction": "precise-technical",
      "job": "inspect an instrument",
      "tags": [
        "instruments",
        "labels",
        "inspection",
        "object",
        "diagram"
      ],
      "summary": "Machines with every control labeled. A synthesizer, a recorder, a mixer: keys, encoders, and ports in rows, each with a name or a small pictogram, color on the hardware used as a code rather than as decoration. The website's useful pages put that object where you can study it. A picture of the machine, a name, a short technical fact, a way to move to the next part. One capture of the homepage describes a full-bleed monochrome photograph and a hairline navigation. Another describes a light editorial mode and a dark product mode. The homepage is allowed to change. The inspection is the reference.",
      "steal": [
        "One object, large, with callouts or a spec list that shares the object's alignment.",
        "Labels in the same voice as the hardware: short, literal, sentence case or a consistent case, never a pile of badges.",
        "A second view only when it shows a different fact (a port, a dimension, a screen), not a second mood.",
        "Technical facts in a column or a definition list: name, then value. Tabular figures where the values are numbers (`type.numbers`)."
      ],
      "avoid": [
        "Hairline-weight type at a size used for navigation decoration. If a capture shows very light, very small labels, that fails `a11y.size` and often fails contrast. Keep the diagrammatic idea and set the label so it can be read.",
        "Their pictograms as a general icon library for a SaaS app. A mark that means \"this product section\" is not a universal action icon.",
        "A monochrome store photograph as a theme. One homepage capture is not a token set.",
        "Rounded or square corners from a single write-up. The captures disagree. Decide from the object.",
        "COS's campaign structure with these products swapped in. A model in a building is not an inspection."
      ]
    },
    {
      "id": "cereal",
      "title": "Cereal",
      "url": "https://readcereal.com",
      "direction": "editorial-print",
      "job": "read a photographic essay",
      "tags": [
        "magazine",
        "photography",
        "serif",
        "space-as-hierarchy",
        "archive"
      ],
      "summary": "Photography of places, interiors, and objects, printed or posted with very little chrome. In the Volume 16 print redesign, Studio Faculty kept a serif for most of the text and a sans for captions and credits, and they refused the usual magazine jump from a huge headline to tiny body. Hierarchy comes from space, from a ragged edge, and from a caption that is actually a caption. Dialogue can sit in italic. A rule can mark the end of a piece.",
      "steal": [
        "A text serif for prose and a sans for captions, credits, and navigation.",
        "A measure you can read, ragged right, with captions clearly smaller and not trapped in a colored box.",
        "An image that is allowed to be the first screen, with a factual caption under it or beside it.",
        "Navigation as a few words or a search field when the content is an archive.",
        "The print lesson, translated carefully: if you do not need five type sizes, do not invent them. On screen, still keep body at a readable size (`a11y.size`). Their print body is small because it is print."
      ],
      "avoid": [
        "Emptiness as an aesthetic when you have no photographs. Cereal without pictures is not editorial. It is a blank (`density.not-empty`).",
        "A drop cap, a pull quote in a card, a huge headline, and a background texture, all at once.",
        "Justified text on the web. The rag was a deliberate readability choice.",
        "Their archive randomization as a gimmick on a store. It works because the archive is deep.",
        "A centered serif headline over every article image with a gradient scrim. That is the template version of \"magazine.\""
      ]
    },
    {
      "id": "financial-times",
      "title": "Financial Times",
      "url": "https://www.ft.com",
      "direction": "editorial-print",
      "job": "read the day's report",
      "tags": [
        "newspaper",
        "salmon-paper",
        "rules",
        "numeric",
        "size-as-rank"
      ],
      "summary": "One salmon sheet for the whole page. Ink is a soft near-black. The lead story is larger than the story beside it. Section labels and the wordmark use a claret that does not fill the buttons. Numbers in the markets line up in columns. Rules divide stories. A May 2026 capture of the homepage also shows a navy subscribe control and other UI hues in navigation and tickers. Those are product chrome. The page's idea is the colored paper, the ranked headlines, and the figures.",
      "steal": [
        "One sheet color for the whole view. If the product has a paper, it is the page.",
        "A front that makes importance obvious: one lead, then smaller stories, divided by rules.",
        "Numeric columns with tabular figures, a header, and a unit. Right-align the numbers.",
        "A serif for the story and a sans for labels, navigation, and figures. Two families (`type.two-families`).",
        "An accent used for the masthead and the kicker, then put away."
      ],
      "avoid": [
        "Financier or Metric, unless you have licensed them. Source Serif 4 or Newsreader can hold the serif role. Public Sans can hold the sans. The roles are the lesson (`type.license`).",
        "Salmon as a highlight on one card, or as a \"warm mode\" of a white app. If you take the paper, it is the background.",
        "Claret buttons, claret links, and a claret hero. The capture's point is how little of the page is claret.",
        "The rest of a homepage capture: navy pills, teal navigation, ticker greens and reds. Importing the whole UI palette produces a costume (`color.budget`).",
        "Their hex values as your tokens. The salmon online is widely cited as `#fff1e5`, including by the FT's own Alphaville. A May 2026 capture lists ink near `#33302e` and claret near `#990f3d`. Label them as observations."
      ]
    },
    {
      "id": "new-york-times",
      "title": "The New York Times",
      "url": "https://www.nytimes.com",
      "direction": "editorial-print",
      "job": "see what matters today",
      "tags": [
        "newspaper",
        "front-page",
        "position",
        "rules",
        "photography"
      ],
      "summary": "A white page. A blackletter masthead. Stories assigned to positions: a lead with a photograph, secondary stories in narrower columns, a denser index further down. Hairline rules separate them. A story page is a headline, a dek, a byline, a measured column, and captions under photographs. Photography is the color. The ground is white, not a tinted sheet.",
      "steal": [
        "A lead, then stories that are visibly secondary by width and position, then a plain index.",
        "Hairline rules in the ink or a soft gray. Square pictures. Captions that are captions.",
        "On the story: one headline, a dek, a byline in the secondary face, a column near 65–72 characters, ragged or carefully justified only if you know why.",
        "Two families in the product you are making. Serif for the story, sans for the byline, the nav, and the caption."
      ],
      "avoid": [
        "Four licensed families, or the exact webfont file names. They change, and they are not yours (`type.license`). An open serif (Source Serif 4, Newsreader) and an open sans (Public Sans) can hold the two roles.",
        "Uppercase labels at a size a person cannot read. The capture's tiny eyebrows fail `a11y.size` if you copy the size, and they fail `type.all-caps-everything` if every label becomes one.",
        "A red breaking-news mark used as the link color, the button, and the brand.",
        "A white card with a shadow for each story. The rule is the divider.",
        "The blackletter masthead as a decorative font on an unrelated product. It is their nameplate."
      ]
    },
    {
      "id": "monocle",
      "title": "Monocle",
      "url": "https://monocle.com",
      "direction": "editorial-print",
      "job": "take a briefing",
      "tags": [
        "magazine",
        "briefing",
        "sections",
        "serif",
        "dense"
      ],
      "summary": "A bound briefing. The launch issue, February 2007, ran long and was divided into named sections: Affairs, Business, Culture, Design, and Edits. Later years kept that spine and added to it (Fashion among them). Pages are dense: several short reports, then a longer story, photographs and illustration mixed with columns of text. The founding design notes name Plantin for the text and Helvetica Neue for captions and information, inside a strict grid. The print object is the point. The site is how a subscriber finds the same sections again.",
      "steal": [
        "A small set of named sections that match how the reader already thinks.",
        "A contents or a section opener that is type, a rule, and a list of real headlines.",
        "Serif prose, sans for the apparatus (caption, page label, nav).",
        "Mixed lengths: a few lines for a note, a real column for a story, with the same margins.",
        "Illustration used as information (a map, a portrait, a diagram), with a caption."
      ],
      "avoid": [
        "Plantin or Helvetica Neue unless you have licensed them. The 2007–2008 notes are a description of their pages, not a font assignment for yours (`type.license`).",
        "Their retail and café life as the layout. The briefing is the reference. A product grid is a different job.",
        "A black cover frame, a serif, and a travel photograph on the generic skeleton. That is the costume.",
        "Print density copied as 9px web type. Their page is paper. On screen, body stays readable (`a11y.size`).",
        "An invented palette. This file has no hex."
      ]
    }
  ],
  "antiPatterns": [
    {
      "id": "skeleton.saas-landing",
      "signals": [
        "Logo left, links, filled button on the right.",
        "Centered headline, often gradient or oversized, with a dek and two buttons.",
        "A row of gray customer logos.",
        "Three feature cards with an icon in a tinted square.",
        "A bento, testimonials, a three-column pricing table with the middle plan highlighted, an FAQ, a four-column footer."
      ],
      "also_called": "the generic agent landing",
      "why": "This layout is the median of recent agent output. Visitors have learned to ignore it, so the product's actual offer never gets a form.",
      "instead": "Use the direction's first_screen in taste/directions.yaml. One subject, one action, real nouns."
    },
    {
      "id": "layout.dashboard-costume",
      "signals": [
        "Left sidebar with a product name and a long nav.",
        "Four statistic cards in a row.",
        "A chart beside or above a table.",
        "A greeting such as \"Good morning\"."
      ],
      "why": "The page claims to be an instrument and reports numbers nobody opened the screen to see.",
      "instead": "Start on the repeating object (the revision, the task, the document). Put a number on that row if the number changes a decision."
    },
    {
      "id": "layout.equal-cards",
      "signals": [
        "Unrelated ideas share one bordered container, one radius, and one shadow.",
        "The card is the layout, not the content."
      ],
      "why": "Equal chrome tells the eye that equal things happened. They did not.",
      "instead": "A column with headings, or a grid of real repeated objects (products, films, files)."
    },
    {
      "id": "layout.nested-cards",
      "signals": [
        "A padded border inside a padded border, sometimes inside a modal."
      ],
      "why": "Each box spends the page's only depth budget on a group that space could have made.",
      "instead": "A heading and a 1px hairline."
    },
    {
      "id": "layout.center-stack",
      "signals": [
        "Headline, paragraph, buttons, and cards are all center-aligned."
      ],
      "why": "The eye restarts on every line. Nothing accumulates into a column.",
      "instead": "One start edge. Center a single ceremonial title only."
    },
    {
      "id": "layout.bento-claims",
      "signals": [
        "Uneven tiles containing similar marketing sentences.",
        "The grid could be shuffled without changing the story."
      ],
      "why": "The bento borrows importance the sentences did not earn.",
      "instead": "One strong subject and a plain list, or a single column."
    },
    {
      "id": "color.aurora",
      "signals": [
        "Purple-to-blue mesh or blurred orbs as the page background.",
        "Gradient text on the headline.",
        "A colored glow behind a card or button."
      ],
      "why": "This is the current mark of generated UI. It replaces a subject with atmosphere.",
      "instead": "A flat tinted surface. Color belongs to a photograph, a product, or one state."
    },
    {
      "id": "color.indigo-default",
      "signals": [
        "White or gray-50 background.",
        "Indigo or violet as the primary.",
        "Inter, Geist, or a similar default grotesk.",
        "No structural idea beyond the skeleton."
      ],
      "why": "The combination is what models emit when they are asked for \"clean SaaS\".",
      "instead": "Change the structure first. Then choose temperature and type for the job."
    },
    {
      "id": "color.gold-on-black",
      "signals": [
        "Pure black background.",
        "Gold or brass rules, dividers, or buttons.",
        "Playfair Display, Cormorant, or another high-contrast Didot as the luxury signal."
      ],
      "why": "The costume says luxury without an object, a material, or a room.",
      "instead": "For an object, use warm paper and a quiet grotesk. For a night room, use the work itself as the color."
    },
    {
      "id": "color.rainbow-pills",
      "signals": [
        "Every status is a saturated filled pill in a different hue."
      ],
      "why": "The pills become the visual event. The words they contain stop mattering.",
      "instead": "A quiet hue plus the word, in a consistent column."
    },
    {
      "id": "type.three-voices",
      "signals": [
        "A display face, a serif, a mono, and often a script on one screen."
      ],
      "why": "The page is performing typography instead of speaking in one voice.",
      "instead": "Two families, each with a written role."
    },
    {
      "id": "type.all-caps-everything",
      "signals": [
        "Small tracked capitals on navigation, labels, buttons, and eyebrows alike."
      ],
      "why": "When everything is an eyebrow, nothing is a kicker. Caps also hurt reading speed.",
      "instead": "Sentence case. One tracked line on the page, or none."
    },
    {
      "id": "type.tiny-gray",
      "signals": [
        "Body or meta set in a light gray that fails 4.5:1, defended as elegant."
      ],
      "why": "Illegible text is not quiet. It is unfinished.",
      "instead": "Mute with size or weight one step, and keep the contrast ratio."
    },
    {
      "id": "material.gray-card-shadow",
      "signals": [
        "Page background near gray-50.",
        "White cards with a large radius and a small shadow.",
        "The same pattern repeated down the page."
      ],
      "why": "This is the default visual sentence of utility CSS. It has no material.",
      "instead": "Flat paper, a real margin, hairlines where groups need a boundary."
    },
    {
      "id": "material.glass-on-flat",
      "signals": [
        "A backdrop-blur panel sitting on a gradient or a flat illustration."
      ],
      "why": "Glass is a response to something moving or photographic behind it. Without that, it is a blur effect.",
      "instead": "A solid surface. Save blur for a control over a real image."
    },
    {
      "id": "material.icon-tile",
      "signals": [
        "A feature row or grid of icon-in-tinted-square, short title, one sentence."
      ],
      "why": "The tile is a placeholder for a feature that was never given a form.",
      "instead": "State the fact in a sentence, or show the object."
    },
    {
      "id": "motion.stagger-fade",
      "signals": [
        "Sections start invisible and fade or slide in on load, often one after another."
      ],
      "why": "The page delays the content to look dynamic. It reads as a template behavior.",
      "instead": "Show the content. Animate the next change the user causes."
    },
    {
      "id": "motion.hover-lift",
      "signals": [
        "Cards scale up and gain a shadow on hover."
      ],
      "why": "The hover announces that the card is a card. It does not help the choice.",
      "instead": "Change ink, underline, or hairline."
    },
    {
      "id": "content.fake-proof",
      "signals": [
        "A row of gray logos.",
        "A number such as \"10,000+ teams\" with no source.",
        "Testimonials with stock portraits and vague praise."
      ],
      "why": "Invented proof is less believable than silence, and it looks generated.",
      "instead": "One real fact (a place, a number you can stand behind, a named customer) or nothing."
    },
    {
      "id": "content.abstract-verbs",
      "signals": [
        "Headlines built from Elevate, Unlock, Seamless, Next-gen, Supercharge, Delightful, \"your workflow\"."
      ],
      "why": "These verbs have no subject. They fit every product, so they describe none.",
      "instead": "The noun a customer would repeat. \"Ash glaze, 18 cm.\" \"Retry delay on the preview proxy.\""
    },
    {
      "id": "chrome.two-primaries",
      "signals": [
        "Two filled buttons side by side."
      ],
      "why": "The page refuses to choose, so the visitor has to.",
      "instead": "One filled action and one text action."
    },
    {
      "id": "chrome.badge-pile",
      "signals": [
        "Several of New, AI, Pro, Beta, Hot on a single title."
      ],
      "why": "The badges are doing the advertising the title failed to do.",
      "instead": "One fact, written into the title or the line under it."
    },
    {
      "id": "chrome.sparkle",
      "signals": [
        "A sparkle or wand icon as the symbol of the feature, often next to the word AI."
      ],
      "why": "The icon is a genre marker. It does not depict the product.",
      "instead": "The object's shape, the data's shape, or no icon."
    },
    {
      "id": "a11y.placeholder-label",
      "signals": [
        "An input whose only name is placeholder text."
      ],
      "why": "The name disappears as soon as someone types, and it usually fails contrast.",
      "instead": "A visible label that stays."
    },
    {
      "id": "a11y.focus-removed",
      "signals": [
        "outline: none, or an equivalent, with no focus-visible replacement."
      ],
      "why": "Keyboard users cannot see where they are. The page also looks broken when it is tabbed, which it will be.",
      "instead": "A 2px offset ring in ink or the accent, designed once."
    }
  ],
  "tokens": {
    "quiet-luxury": {
      "name": "Warm Paper",
      "file": "tokens/quiet-luxury.DESIGN.md",
      "colors": {
        "surface": "#f3efe6",
        "surface-raised": "#f7f4ee",
        "ink": "#1c1915",
        "ink-muted": "#5c564c",
        "hairline": "#ddd4c6",
        "accent": "#7a3e2e",
        "on-accent": "#f6f1e8",
        "danger": "#8d2f2f"
      }
    },
    "cinematic-dark": {
      "name": "Night Room",
      "file": "tokens/cinematic-dark.DESIGN.md",
      "colors": {
        "surface": "#141311",
        "surface-raised": "#1e1c19",
        "ink": "#f3f0e8",
        "ink-muted": "#9c978e",
        "hairline": "#2a2825",
        "line": "#746e66",
        "accent": "#c9846a",
        "on-accent": "#141311",
        "danger": "#e7b2aa"
      }
    },
    "precise-technical": {
      "name": "Instrument",
      "file": "tokens/precise-technical.DESIGN.md",
      "colors": {
        "surface": "#f5f5f2",
        "surface-raised": "#ffffff",
        "ink": "#1b1d1c",
        "ink-muted": "#4e5450",
        "hairline": "#e2e3dc",
        "accent": "#1e5c40",
        "on-accent": "#f3f6f4",
        "danger": "#8f2d1f",
        "warning": "#8a5a12"
      }
    },
    "editorial-print": {
      "name": "Column",
      "file": "tokens/editorial-print.DESIGN.md",
      "colors": {
        "surface": "#f6f1e8",
        "surface-raised": "#fbf7f1",
        "ink": "#1c1917",
        "ink-muted": "#4e4944",
        "hairline": "#d8d0c4",
        "line": "#8a8176",
        "accent": "#1c1917",
        "danger": "#8d2f2f"
      }
    }
  }
};
