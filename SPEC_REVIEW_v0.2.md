# SPEC v0.2 — Objective Critique (pre-M1)

> Authoring date: 2026-04-29
> Reviewer: Claude (self-review of own draft, ultrathink mode)
> Verdict: **Tier 1 weaknesses must be addressed before M5; Tier 2 should be addressed before M1.**

This document critiques `SPEC.md` v0.2 for structural weaknesses that could undermine the project. Findings are ordered by severity. Each item includes (a) the claim in the spec, (b) why it's weak, (c) a concrete fix or escalation.

---

## Tier 1 — Structural blockers (must fix before relevant milestone)

### T1.1 — `codex-core` linking is hand-waved (impacts M5)

**Spec claim** (§2.3, §10.7): the extractor will link against `codex-core` as a Rust dependency to invoke programmatic prompt builders (`format!` chains in `tools/src/*.rs`, `core/src/agent/role.rs::spawn_tool_spec::build`, ContextualUserFragment `body()` methods, etc.) and capture their **default rendering** — the canonical "what the model actually sees" output the user explicitly required (§10.2).

**Why it's weak**:
1. `codex-core` is a workspace-internal crate. We do not know whether its `Cargo.toml` has `publish = false` (likely) or whether its public API is stable across patch releases.
2. Adding it as a git dependency requires a stable, semver-discipline'd public surface. Codex is shipping alphas weekly; that surface almost certainly churns.
3. Adding it as a path dependency hardcodes a local checkout location and breaks for anyone else who clones the mirror repo.
4. Building the extractor *inside* the codex workspace (as an added workspace member) is most reliable but invasive — every extraction would patch the codex tree.
5. Even if linking works, the prompt builders are async, take `&mut Session` references, depend on tokio runtime, and call into network/filesystem code paths we'd have to stub. Constructing a synthetic `Session` from outside is non-trivial.

**Fix proposal — pick one**:
- **Option A (in-workspace extractor crate)**: extractor lives as a `codex-rs/extract-prompts/` crate added at extract-time via a small workspace patch. Build with `cargo run -p extract-prompts`. Pro: full API access, full async runtime. Con: invasive, requires patching upstream tree on each tag; needs a stable patch script.
- **Option B (snapshot-only)**: drop the live-render plan entirely. Use `core/tests/suite/snapshots/model_visible_layout__*.snap` as the canonical rendered-prompt source. Programmatic prompts that don't appear in snapshots are captured as **template-only**. Pro: no codex linkage. Con: parametric coverage gap (T1.3 below); template-only ≠ "what the model actually sees" requirement.
- **Option C (hybrid)**: Option B for everything that snapshots cover; Option A for the gap. Pro: minimal invasive surface. Con: most complex to implement; gap detection itself needs a scheme.
- **Option D (CLI dump mode)**: petition upstream codex to add a `codex --dump-prompts` flag that emits canonical prompt corpus. Pro: durable, official. Con: not in our control; takes time.

**Recommendation**: lock **Option C (hybrid)** but require the in-workspace crate (Option A) be a thin shim (≤200 lines) that imports a single function per programmatic prompt and serializes its output to JSON. Spec must explicitly state which functions get the shim treatment, listed by file:line.

**Spec amendment needed in v0.3**: rewrite §2.3 with the Option C plan, including the explicit shim function list.

---

### T1.2 — "Reachability" is operationally undefined (impacts M2, M3)

**Spec claim** (§2.1): a prompt is in scope iff it is "reachable from one of these entry points: `core::session::turn::build_prompt`, realtime entry points, review entry points, …". The spec implies static call-graph analysis.

**Why it's weak**:
1. Rust's combination of macros, traits with dynamic dispatch, async, and conditional compilation makes whole-program static call-graph extraction a research-grade problem. There is no off-the-shelf tool that handles modern async Rust correctly. `cargo-call-stack` exists but explicitly does not handle async or trait objects reliably.
2. Without real reachability analysis, "reachable" degrades to "the file is referenced somewhere from within a crate that ships in the binary". This **over-includes** test-only paths if the test module isn't `cfg(test)`-gated, and **under-includes** code reached via dynamic dispatch (which is how the entire MCP tool registry works).
3. So the spec's "reachability rule" cannot actually be mechanized as written.

**Fix proposal**:
- Replace the call-graph claim with an **enumerated allow-list** of source files/symbols that contain prompt content, plus a fallback rule: "anything `include_str!`'d under a shipping crate is in by default". Maintain the allow-list manually with extractor-tooling support.
- Add a **denylist** for known test-only paths.
- Document that the allow-list is the source of truth, not call-graph analysis.

**Spec amendment needed in v0.3**: rewrite §2.1 around enumerated allow/deny lists. Explicitly state we are **not** doing static analysis; we are doing curated enumeration with mechanical filters.

---

### T1.3 — Snapshot verification has a parametric coverage gap (impacts M4)

**Spec claim** (§2.4): "every line of every `model_visible_layout__*.snap` must trace back to a captured fragment. Lines that cannot be attributed are spec bugs."

**Why it's weak**:
- Snapshots are recorded outputs of *specific test scenarios* with specific config values, sandbox modes, model selections, MCP configs, etc. They cover the prompt-assembly paths that the test suite happens to exercise.
- A prompt that never appears in any snapshot test (e.g., a prompt that only fires under `realtime + danger_full_access + specific MCP server present`) is **invisible** to the snapshot trace-back check.
- The spec implies "snapshot coverage = capture coverage". This is **not true**.
- Worse: 100% snapshot trace-back gives a false sense of completeness, which the README plans to advertise.

**Fix proposal**:
- Reframe the snapshot check as a **negative test**: "no captured prompt may contain content that *contradicts* a snapshot". I.e., snapshots prove a lower bound on capture correctness, not an upper bound on completeness.
- Add a **second** completeness check based on the allow-list (T1.2): "every entry on the allow-list must produce at least one captured file". This catches missing extractions even for never-tested prompts.
- README's "Coverage" section should report two numbers: (i) snapshot trace-back %, (ii) allow-list completeness %.

**Spec amendment needed in v0.3**: rewrite §2.4 + §3.4 coverage section.

---

## Tier 2 — Significant risks (should fix before M1 to avoid rework)

### T2.1 — Inline-string `MIN_SIZE = 80 chars` threshold is arbitrary

**Spec claim** (§2.2 Pass 1): inline `r#"..."#` blocks ≥ 80 chars are extracted; smaller are ignored.

**Why it's weak**: 80 is arbitrary. Excludes legitimate ~40-char prompt fragments. Includes 80-char error messages or comments that aren't prompts.

**Fix**: replace size threshold with **intent attributes**. Inline strings are extracted iff (a) annotated with a marker (e.g., `// PROMPT-EXTRACT`) or (b) reside in an explicit allow-list of constants/functions. We're already maintaining an allow-list per T1.2; reuse it.

---

### T2.2 — Feature-flag handling is undefined

**Spec claim**: silent on `#[cfg(feature = "...")]`-gated prompts. Recon flagged the `child_agents_md` feature flag specifically.

**Why it's weak**: the same `codex` binary built with different `--features` flags has different reachable prompts. Without a baseline declaration, "what's in scope" is ambiguous.

**Fix**: declare in spec: **mirror is built against `--features default`** (i.e., what `cargo build` produces unmodified at the upstream tag). Feature-gated content not in default is in `prompts/feature-flag/<flag-name>/...` clearly labeled. Re-run extraction with `--all-features` as a separate audit.

---

### T2.3 — Token counts mislead for variable-bearing prompts

**Spec claim** (§7): count template body verbatim; placeholders intact; runtime tokens differ.

**Why it's weak**:
- Piebald says "actual counts will differ slightly — likely not beyond ±20 tokens". For Codex this is dramatically wrong: the personality slot alone is 100+ tokens; AGENTS.md content can be thousands. The README's per-file counts can mislead by an order of magnitude.
- For programmatic prompts with `*-template.md` and `*-default.md` siblings, we count both. The default is closer to runtime but still parametric (chosen synthetic context).

**Fix**:
- Rename frontmatter `tokens.o200k_base` → `tokens.template_o200k_base` (template token count, placeholders intact) for templates. For renderings, use `tokens.rendered_o200k_base` with an explicit `render_context` echo.
- README index displays both with a clear "template vs. rendered" header.
- Add to README a prominent disclaimer: "Token counts for variable-bearing prompts are *template token counts*, NOT runtime token counts. Real session tokens can be 2–5× higher."

---

### T2.4 — Tag-skip vs. 1:1 tag mapping contradiction

**Spec claim** (§3.5, §6.1, §13.3): no-prompt-diff tags are silently skipped (no commit, no CHANGELOG entry). But §13.3 says "Every mirror commit is tagged with the same tag string as upstream".

**Why it's weak**: contradiction. If we skip an upstream tag, mirror tags ≠ upstream tags 1:1.

**Fix**: pick one and enforce:
- Either **always tag** (even no-prompt-diff): mirror commit just records "no prompt change" and the CHANGELOG entry says so. Pro: 1:1 mapping preserved. Con: more tags.
- Or **selective tag** with clear rule: mirror tag a→b directly with no intermediate. CHANGELOG header says "Spans upstream tags X..Y, no prompt change in intermediate".

**Recommendation**: selective (less noise), documented explicitly. Update §13.3 accordingly.

---

### T2.5 — Manual mode via Claude has context-window limits

**Spec claim** (§8.2): Claude executes extractor + dry-run review + commit on user prompt.

**Why it's weak**: a full extraction touches ~100 prompt files with frontmatter, snapshots, diffs. Concatenated into a single dry-run review, this can blow past Claude's context window. Particularly bad for first extraction (no diff baseline; everything is "new").

**Fix**: extractor's dry-run output must be **paginated/summarized**:
- Default: summary only (`N files added, M modified, K removed; total token Δ ±X`).
- Optional flags for `--show-diff <category>` to see specific category diffs.
- Full diff written to `dry-run-report.md` regardless; Claude reads on request.

---

## Tier 3 — Process / governance issues

### T3.1 — Effort estimate (5–6 days) is optimistic by ~2–3×

**Spec claim** (§11): "Total: ~5–6 days of focused work, risk concentrated in M5."

**Why it's weak**: M5 alone is likely 5–7 days given codex-core linking unknowns (T1.1), the ContextualUserFragment runtime-state extraction problem (cwd, env vars, AGENTS.md content all need stubs), and the 1101-line `code-mode/src/description.rs` constants. Realistic estimate: 12–18 days for v1.0 at production quality.

**Fix**: rewrite §11 with milestone-level estimates that account for unknown-unknowns. Add an explicit "research spike" before M5 to validate the codex-core linkage strategy.

---

### T3.2 — Frozen category list is too rigid

**Spec claim** (§3.2): "no further additions [to the prefix list] without spec amendment".

**Why it's weak**: codex evolves; new categories (e.g., a new mode) will arise. A spec amendment process for every new prefix creates governance friction. Also creates ambiguity for novel prompts that don't fit any prefix.

**Fix**: replace with an open process: "new prefixes may be added to the working tree; the SPEC.md prefix table is regenerated from observed prefixes at each release. Adding a prefix requires a 1-paragraph rationale in the README index."

---

### T3.3 — GH Action automation has no auth/rate-limit plan

**Spec claim** (§8.3): hourly poll of upstream tags via GH Action.

**Why it's weak**:
- Hourly = 24 calls/day per workflow. GitHub API unauthenticated rate limit is 60/hour per IP. Authenticated is 5000/hour per token. So we need auth.
- Spec doesn't say which token (PAT? GITHUB_TOKEN? bot account?), where it's stored, who owns it.
- If the action fails to detect a tag for any reason, we silently drift behind.

**Fix**: §8.3 must specify:
- Auth: `GITHUB_TOKEN` for cross-repo read of `openai/codex` tags is sufficient (public repo).
- Rate limit: ample headroom even hourly.
- Drift detection: a daily reconcile job that diffs `openai/codex` tag list against our mirror tag list and flags missing tags.

---

### T3.4 — Backfill correctness undefined

**Spec claim** (§13.6): "Initial release covers only the latest tag at extraction time. Historical backfill ... is deferred."

**Why it's weak**: backfilling old tags with the *current* extractor produces results that may differ from what the *historical* extractor would have produced. A reader looking at `git checkout rust-v0.123.0` of our mirror sees an extraction that uses the current spec, not the spec that was current when v0.123.0 shipped. This is fine if disclosed but should be disclosed.

**Fix**: §13.6 add: "Historical backfilled commits will state in their commit message: `Extracted under spec vN.M which post-dates this codex tag`. Original snapshots from older spec versions are not re-derived."

---

### T3.5 — Extractor versioning isn't part of the snapshot identity

**Spec claim** (§13.5): "Mirror snapshot is a function of (codex tag, spec version)".

**Why it's weak**: it's actually a function of (codex tag, spec version, **extractor version**). If we fix a bug in the extractor without a spec change, re-extracting same codex tag yields different output. This non-deterministic-feeling behavior should be made explicit.

**Fix**: every mirror commit message records `Extractor: <git-sha-of-extractor-source>` in addition to `Spec: vN.M`. Frontmatter on each prompt file records `extractor_version` too.

---

## Tier 4 — Documentation / clarity issues

### T4.1 — `source.kind` enum is incomplete

**Spec claim** (§3.3): `source.kind: include_str | inline_raw_string | json_field | toml_field | format_template`.

**Why it's weak**: missing kinds we already know about:
- `text_resource` (e.g., `agent_names.txt`)
- `lark_grammar` (e.g., `apply_patch.lark`)
- `concat_macro` (multi-piece `concat!()`)
- `writeln_chain` (sequential writeln! into a buffer)

**Fix**: extend the enum.

---

### T4.2 — GPT-5 tokenizer assumption unverified

**Spec claim** (§7): `tiktoken o200k_base` covers gpt-5.x.

**Why it's weak**: tokenizer choice for gpt-5.x is asserted, not verified. If gpt-5 uses a different BPE, our token counts are wrong for those models.

**Fix**: pre-extraction verification: check `tiktoken.encoding_for_model("gpt-5")` and `"gpt-5.2-codex"` to confirm. If unknown, fall back to `o200k_base` and document.

---

### T4.3 — Repo naming has trademark exposure

**Spec claim** (§9, §12): defer trademark review to lawyer.

**Why it's weak**: starting M1 with the name `codex-system-prompts` and pushing to GitHub publicly creates exposure that's hard to undo (search indexing, references). Cheaper to pick a defensible name now.

**Fix**: pre-M1 decision: pick one of:
- (a) `codex-system-prompts` (current) — risk of nominative-use challenge.
- (b) `openai-codex-prompts-mirror` — clearer mirror status, still uses "Codex"+"OpenAI" nominatively.
- (c) `codex-prompt-archive` — neutral, less search-discoverable.
- (d) Keep mirror private until name is settled.

**Recommendation**: (a) for working name with `DISCLAIMER.md` upgraded to explicitly cite nominative-use safe harbor; revisit only if challenged. Public repo OK.

---

## Summary table

| ID | Tier | Title | Blocks | Required spec work |
|---|---|---|---|---|
| T1.1 | 1 | codex-core linking | M5 | §2.3 rewrite |
| T1.2 | 1 | Reachability operational gap | M2, M3 | §2.1 rewrite |
| T1.3 | 1 | Snapshot coverage gap | M4 | §2.4, §3.4 rewrite |
| T2.1 | 2 | MIN_SIZE arbitrary | M2 | §2.2 fix |
| T2.2 | 2 | Feature-flag scope | M2 | §1, §2.1 add |
| T2.3 | 2 | Token-count framing | M6 | §7, §3.4 fix |
| T2.4 | 2 | Tag-skip contradiction | M5 | §13.3 fix |
| T2.5 | 2 | Claude context limit | M5 | §8.2 fix |
| T3.1 | 3 | Effort estimate | M0 | §11 rewrite |
| T3.2 | 3 | Frozen prefix list | governance | §3.2 fix |
| T3.3 | 3 | GH Action auth | M7 | §8.3 fix |
| T3.4 | 3 | Backfill disclosure | (post-M8) | §13.6 add |
| T3.5 | 3 | Extractor version identity | (cross-cut) | §13.5 fix |
| T4.1 | 4 | source.kind enum | M2 | §3.3 fix |
| T4.2 | 4 | GPT-5 tokenizer | M6 | §7 verify |
| T4.3 | 4 | Repo naming exposure | M1 | §9 decide |

---

## Recommended action

**Path A (rigorous spec-driven)**: produce SPEC v0.3 addressing Tier 1 + Tier 2 before M1. Estimated 0.5–1 day of spec work. Then proceed to M1 with confidence.

**Path B (pragmatic spec-driven)**: address Tier 1 + Tier 2.1 + T2.2 + T2.4 in v0.3 (the items that truly block design). Defer Tier 3, 4, and remaining Tier 2 to be resolved during the milestones they touch (with TODO markers in the spec). Estimated 2–3 hours of spec work. Then proceed to M1.

**Path C (skip-it)**: proceed to M1 with v0.2 as-is, treating this critique as a known-issues log. Higher risk of M5 rework.

I recommend **Path B** — it preserves the spec-driven discipline for the design-impacting issues without paying for hyper-completeness up front.
