# Preregistration — Scope-Gap Injection mechanism replication

Locked: 2026-10-27 (after pilot seed 1, n=24 per channel; pilot seeds are
calibration-only and never count toward the head-to-head).

## Target paper
arXiv 2610.34777, Niu, Ren, Qu, "Scope-Gap Injection: Exploiting Evaluator
Channel Blind Spots in the OpenClaw Agent Security Competition" (submitted
26 Oct 2026). Abstract verified live 2026-10-27. The paper's campaign figures
(78% vs 23% S2 acceptance; 5/19 all-stage bypasses) are CONTEXT ONLY and are
not reproduced claims: this replication measures a scripted, synthetic
mechanism, not the paper's competition campaign.

## Author-code recheck (Gate 1)
- arXiv abs page carries no code link (only generic arXivLabs toggles).
- Exact-title and author-name web searches 2026-10-27 returned no author
  repository (only unrelated OpenClaw scope-squatting posts, an unrelated
  "Scope" federated-learning defense repo, and patents).
- Verdict: NO author code found. Clean-room harness proceeds.

## Harness (Gate 0, tests green 7/7 before any measurement)
- S1: static skill scan (code-execution tokens in skill definition).
- S2: scripted judge over task + skill definition ONLY (baseline).
- S3: scripted agent reading task + skill + attachment, following
  instruction lines in followed channels, executing simulated privileged
  actions; benign read task (list worklist items) always allowed.
- All targets/tasks/skills/worklists synthetic, seeded RNG, stdlib only.

## Pilot results (calibration only)
- Pilot seed 1, n=24/channel: S2 accept attachment 1.000 vs in-skill 0.000,
  gap 1.000, 95% CI [1.000, 1.000]; all-stage bypass attachment 1.000,
  in-skill 0.000, benign control 0.000; both mitigations reduce bypass to
  0.000 with benign utility unchanged (1.000).
- Obfuscation sweep: standard phrasings show the placement gap (0 vs 1.0);
  obfuscated phrasings that avoid the judge's verb list evade the lexical
  judge in BOTH channels. Consequence: the locked template set is the 6
  standard business-worklist templates in src/generate.py; the replication
  measures the placement effect CONDITIONAL on judge-detectable phrasing,
  and the writeup must state this judge-coverage limit.

## Locked head-to-head protocol
- Fresh seeds, never pilot seeds: seed 101, n=60 per channel (benign,
  in-skill, attachment), each package evaluated under all three guards
  (baseline, scope_aligned_judge, data_only_attachment).
- Metrics: S2 acceptance rate, all-stage bypass rate, benign task
  completion rate; paired bootstrap CIs (10,000 reps) for all headline
  comparisons, paired by package index.
- Determinism check: re-running seed 101 must reproduce an identical
  results-file SHA-256.

## Locked Gate 2 (disease) bars — ALL must hold
1. S2 acceptance gap (attachment minus in-skill, baseline) >= 0.30 with
   paired bootstrap 95% CI lower bound > 0.
2. All-stage bypass rate, attachment channel, baseline >= 0.50.
3. All-stage bypass rate, benign control channel, baseline = 0.00.
If any bar fails: KILL on scope, no bar-moving, no re-tuning.

## Locked Gate 3 (load-bearing) bars — at least one mitigation must satisfy BOTH
1. Bypass reduction on the attachment attack slice (baseline minus
   mitigation) >= 0.50 with paired bootstrap 95% CI lower bound > 0.
2. Benign utility drop (mitigation minus baseline benign completion) >=
   -0.10, i.e. the 95% CI lower bound must not fall below -0.10.
If no mitigation satisfies both: KILL honestly (reportable only if this
bar had said so — it does not, so a G3 failure is a KILL).

## No-bar-moving rule
Bars above are frozen at lock time. Any post-lock change requires a new
dated amendment stating the change and the reason, and voids the
preregistered claim.
