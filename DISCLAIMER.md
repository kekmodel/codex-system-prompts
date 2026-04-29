# Disclaimer

`codex-system-prompts` is an **unofficial mirror** of the prompt strings shipped by OpenAI's [Codex CLI](https://github.com/openai/codex).

## What this is

A version-tracked, fragment-level archive of every prompt string the Codex CLI ships and uses at runtime. Modeled on Piebald AI's [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) philosophy, faithfully adapted to Codex's hybrid prompt architecture (per-model `base_instructions` monoliths + `ContextualUserFragment` wrappers + programmatic `format!`-built tool descriptions).

See [SPEC.md](./SPEC.md) for the full specification.

## What this is NOT

- **Not endorsed by OpenAI.** This project is not authored, maintained, or reviewed by OpenAI.
- **Not a replacement for upstream.** The source-of-truth for actual Codex behavior is the upstream repository at the recorded git tag.
- **Not a customizable runtime.** Editing files here does not change Codex's behavior. To customize Codex's prompts locally, fork the upstream repo or use a tool that patches the binary.

## Trademarks

"Codex" and "OpenAI" are trademarks of OpenAI. Their use here is [nominative](https://en.wikipedia.org/wiki/Nominative_use) — we describe what the upstream project is — and does not imply endorsement.

## License

The mirrored prompt content is licensed under Apache License 2.0 (matching upstream). See [LICENSE](./LICENSE) and [NOTICE](./NOTICE). The extractor tooling under `extractor/` is also Apache-2.0.

## Reporting issues / takedown

If you are an OpenAI representative and have concerns about this mirror, please open an issue or contact the maintainer. Public-facing contact details will be added when the repo is published (see SPEC §10.1, M8).
