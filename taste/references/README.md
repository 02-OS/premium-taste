# Reference gallery

Annotated products an agent can load one at a time. These are not templates and not token sheets. Each file records decisions, what to steal, and what becomes costume if you copy it.

Live sites change. A hex value or a font name is an observation, often from a public capture, not a license to paste. The "What to steal" section is the part you may carry into another product.

## Retrieval

Open `index.yaml`. Filter on `direction`, then on `job`. Load one file.

```yaml
# fields an agent can match
direction: quiet-luxury | cinematic-dark | precise-technical | editorial-print
job: a short phrase for the screen's outcome
tags: [ ... ]
```

## Current set

18 references. The target range is 15–25. Each direction has more than one, so a sample token is not the only example of that direction.

| Id | Direction | Job |
| --- | --- | --- |
| `aesop` | quiet-luxury | buy a physical good |
| `cos` | quiet-luxury | look at a garment |
| `are-na` | quiet-luxury | collect and connect research |
| `hermes` | quiet-luxury | look at an object from the house |
| `muji` | quiet-luxury | choose a plain object |
| `mubi` | cinematic-dark | enter a film journal |
| `resident-advisor` | cinematic-dark | find an event tonight |
| `criterion` | cinematic-dark | choose a film from a library |
| `sonos` | cinematic-dark | see what is playing |
| `things-3` | precise-technical | see what to do today |
| `figma` | precise-technical | edit a design on a canvas |
| `stripe-docs` | precise-technical | read and copy a technical document |
| `ia-writer` | precise-technical | write the next sentence |
| `teenage-engineering` | precise-technical | inspect an instrument |
| `cereal` | editorial-print | read a photographic essay |
| `financial-times` | editorial-print | read the day's report |
| `new-york-times` | editorial-print | see what matters today |
| `monocle` | editorial-print | take a briefing |

## Add a reference

1. Copy `_template.md` to `taste/references/<id>.md`.
2. Use a real, public product or a documented brand system. Write only what you can support. Mark `confidence: medium` when you are describing long-standing character rather than a measured capture.
3. Fill every section in the template. "What not to copy" is required.
4. Add a row to `index.yaml`. The `id` matches the filename.
5. If it is the second reference in a thin direction, say in Uniqueness how it differs from the one already there.
6. Run `python3 scripts/check_catalog.py` from the repo root.

Do not add a reference whose only lesson is "it is minimal." Do not add a generated mock, a Dribbble shot, or a clone of a reference already here.

## What would still be new

The earlier gaps are filled: a financial daily, a maison, a plain-goods label, a writing column, a listening surface with a caution, and an instrument-maker. Stop until a new reference teaches a decision this set does not. Another minimal store does not. A non-Latin reading system, or a dense data terminal, might.
