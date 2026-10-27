# scope-gap-injection

A controlled, CPU-scale, scripted replication of the *mechanism* behind
"Scope-Gap Injection" (arXiv 2610.34777, Niu, Ren, Qu): an evaluator that
inspects the task and skill definition but not attachment contents is blind
to privileged instructions placed in an attachment, while the agent that
reads attachments during execution follows them.

**What this is not:** a re-run of the paper's competition campaign. The
paper's figures (78% vs 23% S2 acceptance; 5 of 19 targets bypassing all
stages) are campaign observations, not controlled measurements, and are
quoted here as context only. Every number reported by this repo was
measured by the scripted harness in this repo on synthetic targets.

## Pipeline (scripted, zero LLM, deterministic)

- **S1** static skill scan: flags code-execution tokens in the skill definition.
- **S2** scripted judge: inspects task + skill definition only (baseline).
  This is the evaluator channel blind spot under test.
- **S3** scripted agent: reads task + skill + attachment and follows
  instruction lines, executing simulated privileged actions.

## Channels

- `benign` — control: no privileged instruction anywhere.
- `in-skill` — privileged instruction inside the skill definition (visible).
- `attachment` — benign task + skill, privileged instruction inside the
  attachment worklist (the scope-gap placement).

## Mitigations (load-bearing candidates)

- `scope_aligned_judge` — S2 also scans attachment contents.
- `data_only_attachment` — the agent follows instructions from task/skill
  only and treats attachments as data (reading still allowed).

## Measured results (head-to-head, seed 101, n=60/channel)

| Metric | Value |
|---|---|
| S2 acceptance, attachment channel | 1.000 |
| S2 acceptance, in-skill channel | 0.000 |
| S2 acceptance gap (paired bootstrap 95% CI) | 1.000 [1.000, 1.000] |
| All-stage bypass, attachment, baseline | 1.000 |
| All-stage bypass, in-skill, baseline | 0.000 |
| All-stage bypass, benign control | 0.000 |
| Bypass after scope-aligned judge | 0.000 (reduction 1.000, CI [1.000, 1.000]) |
| Bypass after data-only attachment | 0.000 (reduction 1.000, CI [1.000, 1.000]) |
| Benign task completion, all guards | 1.000 |

## Limits (read before citing)

- Scripted lexical judge and agent: deterministic, so CIs are degenerate.
  The effect is measured conditional on judge-detectable phrasing — a
  pilot obfuscation sweep showed phrasings that avoid the judge's verb list
  evade it in both channels (a judge-coverage limit, not a scope-gap effect).
- Synthetic targets only; no real agent, no real LLM judge, no real
  OpenClaw pipeline. Do not cite these numbers as the paper's results.

## Reproduce

```bash
python3 -m pytest tests/ -q
python3 -m src.run pilot --seed 1 --n 24 --out results/pilot.jsonl
python3 -m src.run headtohead --seed 101 --n 60 --out results/headtohead.jsonl
```

Requires Python 3.10+ and only the standard library. Results append one row
per finished run so an interrupted run loses at most the in-flight row.
Re-running seed 101 reproduces results SHA-256
`60d2b309a78184c492df0bf84bbf62dcdc37d9f7fb4d4650c7ee0fab861958cb`.
