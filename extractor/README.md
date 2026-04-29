# extractor/

Extraction tooling for `codex-system-prompts`. See [/SPEC.md §2](../SPEC.md#2-extraction-strategy) for the design.

## Layout

| Path | Purpose |
|---|---|
| `pyproject.toml` | Python orchestrator project (uv-managed) |
| `src/extractor/` | Python source — CLI, passes 1/1.5/2/3/4/5 |
| `codex-shim/` | Rust crate patched into `codex-rs/` workspace at extract time (SPEC §2.3.1) |
| `allow_list.toml` | Curated allow-list (SPEC §2.1 (B)) |
| `denylist.toml` | Denylist (SPEC §2.1 (C)) |

## Setup

```sh
cd extractor
uv sync
```

## Usage (M2+)

```sh
# Dry-run extraction at the latest upstream rust-v* tag
uv run extractor extract \
  --codex-root /path/to/codex \
  --out .. \
  --mode dry-run

# Inspect a category-specific diff after dry-run
uv run extractor diff --category tool
```

M1 ships only the skeleton; commands raise `NotImplementedError`.

## Two-language design (SPEC §10.7)

- **Python orchestrator** drives the pipeline (Passes 1, 1.5, 2, 3, 4, 5), tokenizes (`tiktoken`), generates frontmatter, writes the corpus, and renders README + CHANGELOG.
- **Rust shim** (`codex-shim/`) is the **only** path to accurate `format!`/`writeln!` rendering for programmatic prompts. It's patched into the codex-rs Cargo workspace at extract time, builds against the actual codex-core / codex-tools / codex-code-mode crates at the target tag, invokes the prompt builders with a synthetic default context (SPEC §2.3.3), and emits JSON. Python consumes the JSON.
- The patch is reverted after extraction; codex tree returns clean.
