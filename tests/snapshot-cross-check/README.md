# tests/snapshot-cross-check/

Implements [SPEC §2.5](../../SPEC.md#25-verification--two-layers-t13) verification. M4 will populate.

## Layer A — Accuracy (snapshot trace-back)

Every line of every:

- `core/tests/suite/snapshots/model_visible_layout__*.snap`
- `core/src/guardian/snapshots/*.snap`

(downloaded from upstream at the recorded tag) must trace back to a captured prompt fragment in `../../prompts/`, OR be a documented runtime-injected variable (cwd path, current time, git branch, etc.).

Lines that cannot be attributed are spec bugs (CI-blocking).

**Proves**: when a captured prompt is exercised by tests, our extraction matches shipping behavior.

**Does NOT prove**: that all shipping prompts are captured (Layer B handles that).

## Layer B — Completeness (allow-list inventory)

- Every entry in `extractor/allow_list.toml` must produce ≥1 captured file.
- Every `.md`/`.lark`/`.toml`/`.txt` matched by Pass 1 auto-include must produce a captured file (or be deny-listed with rationale).
- Every per-model entry in `models.json` must produce a `base-instructions-<slug>.md` file.

**Proves**: nothing is dropped between source enumeration and corpus emission.

**Does NOT prove**: that the allow-list itself is complete. That's bounded by curation.

Both layers run as required CI checks (SPEC §8.4).
