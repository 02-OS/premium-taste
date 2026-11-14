# taste/

The judgment layer.

| Path | Role |
| --- | --- |
| `principles.md` | Why a choice looks finished or cheap. Read this when making a new surface. |
| `principles.yaml` | The same rule ids as tests. Grep one id while critiquing. |
| `anti-patterns.yaml` | Named failures, with the visible signals and the move that replaces them. |
| `directions.yaml` | Four directions, how to choose, and a first-screen recipe for each. |
| `index.yaml` | What to load, and what not to load all at once. |
| `references/` | Annotated products. Load one. |

Rule ids are shared between the markdown and the YAML. If you change a rule, change both, then run `python3 scripts/check_catalog.py` from the repo root.

Tokens are not in this folder. Sample identities live in `tokens/` and are optional.
