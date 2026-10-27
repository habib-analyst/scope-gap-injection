# Kill-gate record — project #87 scope-gap-injection

All gates evaluated in order. No gate was skipped, no bar moved after locking.

## G0 — harness (PASS)
Scripted judge + agent audit harness built first; 7/7 tests green
(`python3 -m pytest tests/ -q`) before any head-to-head measurement.
Deterministic, zero LLM, synthetic scope stated in README and PAPER.

## G1 — author-code recheck (PASS — no author code found)
- arXiv abs page for 2610.34777 (read live 2026-10-27) carries no code link.
- Exact-title search and author-name searches (Weihang Niu, Mengxing Ren,
  Che Qu) returned no author repository: only unrelated OpenClaw
  scope-squatting coverage, an unrelated "Scope" federated-learning defense
  repo, and patents. Watch-time shelf (empty) confirmed, not assumed.
- Proceeded with a clean-room harness; no author code reused.

## G2 — disease, pilot-calibrated and PREREG-locked (PASS)
Pilot (seed 1, n=24/channel, calibration-only):
S2 accept attachment 1.000 vs in-skill 0.000; gap 1.000, 95% CI [1.000, 1.000].
Obfuscation sweep: standard phrasings show the placement gap; obfuscated
phrasings evade the lexical judge in BOTH channels (judge-coverage limit,
recorded in PREREG and PAPER, and the reason the locked template set is the
6 standard business-worklist templates).
Locked bars (PREREG.md): gap >= 0.30 with CI lower bound > 0; attachment
bypass >= 0.50; benign control bypass = 0.00.
Head-to-head (seed 101, n=60/channel, 540 rows):
- S2 acceptance: attachment 1.000, in-skill 0.000, benign 1.000.
- S2 gap: 1.000, paired bootstrap 95% CI [1.000, 1.000] — bar 1 met.
- All-stage bypass (baseline): attachment 1.000, in-skill 0.000 — bar 2 met.
- Benign control bypass: 0.000 — bar 3 met.
G2 VERDICT: PASS.

## G3 — load-bearing (PASS)
Locked bars: bypass reduction >= 0.50 with CI lower bound > 0 AND benign
utility drop >= -0.10.
- Scope-aligned judge (S2 also scans attachments): bypass 1.000 -> 0.000,
  reduction 1.000, 95% CI [1.000, 1.000]; benign utility delta 0.000.
- Data-only attachment (agent follows task/skill only, reads attachments
  as data): bypass 1.000 -> 0.000, reduction 1.000, 95% CI [1.000, 1.000];
  benign utility delta 0.000 (benign completion 1.000 under all guards).
G3 VERDICT: PASS (both mitigations independently satisfy both bars).

## Determinism
Re-running seed 101 reproduced an identical results SHA-256:
60d2b309a78184c492df0bf84bbf62dcdc37d9f7fb4d4650c7ee0fab861958cb
(headtohead.jsonl == headtohead_rerun.jsonl).

## Honest caveat (carried into PAPER.md)
The scripted judge and agent are deterministic, so headline CIs are
degenerate ([1.000, 1.000]). The measured effect is the placement
mechanism conditional on judge-detectable phrasing — it is NOT a
reproduction of the paper's campaign figures (78%/23%, 5/19), which remain
context only and are never presented as reproduced.
