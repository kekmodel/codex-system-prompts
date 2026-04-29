//! codex-prompt-extract-shim
//!
//! See /SPEC.md §2.3 for the design. This crate is patched into the
//! codex-rs workspace at extract time. It imports prompt-builder symbols
//! from codex-core / codex-tools / codex-code-mode, invokes them with a
//! synthetic default context (§2.3.3), and serializes outputs to JSON.
//!
//! M1: stub. M5 will populate.

fn main() {
    eprintln!("codex-prompt-extract-shim: M5 will implement.");
    std::process::exit(2);
}
