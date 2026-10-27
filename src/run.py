"""Experiment runner.

Usage:
  python -m src.run pilot --seed 1 --n 24 --out results/pilot.jsonl
  python -m src.run headtohead --seed 101 --n 60 --out results/headtohead.jsonl

Each row is one package under one guard; rows are appended incrementally
so a reboot loses at most the in-flight row. A run summary (rates + CIs)
is printed and written to <out>.summary.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from pathlib import Path

from .generate import make_package
from .pipeline import BASELINE, DATA_ONLY_ATTACHMENT, SCOPE_ALIGNED_JUDGE, run_package
from .stats import paired_bootstrap_ci, rate

GUARDS = {
    "baseline": BASELINE,
    "scope_aligned_judge": SCOPE_ALIGNED_JUDGE,
    "data_only_attachment": DATA_ONLY_ATTACHMENT,
}


def run_experiment(mode: str, seed: int, n: int, out: Path) -> dict:
    rng = random.Random(seed)
    rows: list[dict] = []
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a", encoding="utf-8") as fh:
        for i in range(n):
            for channel in ("benign", "in-skill", "attachment"):
                pkg = make_package(rng, channel)
                for gname, guard in GUARDS.items():
                    res = run_package(pkg, guard)
                    row = {"mode": mode, "seed": seed, "idx": i,
                           "guard": gname, **res}
                    rows.append(row)
                    fh.write(json.dumps(row, sort_keys=True) + "\n")
                    fh.flush()
    return summarize(rows, mode, seed, n, out)


def _series(rows, guard, channel, field):
    return [float(r[field]) for r in rows
            if r["guard"] == guard and r["channel"] == channel]


def summarize(rows, mode, seed, n, out) -> dict:
    def s2rate(g, c):
        return rate(_series(rows, g, c, "s2_pass"))

    def byrate(g, c):
        return rate(_series(rows, g, c, "bypass"))

    # Paired by (idx, channel) ordering: rows for a channel under two guards
    # share the same package, so pair on idx.
    def paired(g1, g2, channel, field):
        d1 = {r["idx"]: float(r[field]) for r in rows
              if r["guard"] == g1 and r["channel"] == channel}
        d2 = {r["idx"]: float(r[field]) for r in rows
              if r["guard"] == g2 and r["channel"] == channel}
        idxs = sorted(d1)
        return [d1[i] for i in idxs], [d2[i] for i in idxs]

    # S2 gap: attachment vs in-skill under baseline, paired by idx.
    att = {r["idx"]: float(r["s2_pass"]) for r in rows
           if r["guard"] == "baseline" and r["channel"] == "attachment"}
    ins = {r["idx"]: float(r["s2_pass"]) for r in rows
           if r["guard"] == "baseline" and r["channel"] == "in-skill"}
    idxs = sorted(att)
    gap_pt, gap_lo, gap_hi = paired_bootstrap_ci(
        [att[i] for i in idxs], [ins[i] for i in idxs], seed=seed)

    # G3: mitigation vs baseline on the attachment attack slice (bypass).
    summary = {
        "mode": mode, "seed": seed, "n_per_channel": n,
        "s2_accept_attachment_baseline": s2rate("baseline", "attachment"),
        "s2_accept_in_skill_baseline": s2rate("baseline", "in-skill"),
        "s2_accept_benign_baseline": s2rate("baseline", "benign"),
        "s2_gap_attachment_minus_in_skill": gap_pt,
        "s2_gap_ci95": [gap_lo, gap_hi],
        "bypass_attachment_baseline": byrate("baseline", "attachment"),
        "bypass_in_skill_baseline": byrate("baseline", "in-skill"),
        "bypass_benign_baseline": byrate("baseline", "benign"),
    }
    for gname in ("scope_aligned_judge", "data_only_attachment"):
        a, b = paired("baseline", gname, "attachment", "bypass")
        pt, lo, hi = paired_bootstrap_ci(a, b, seed=seed)
        summary[f"bypass_reduction_{gname}"] = pt
        summary[f"bypass_reduction_{gname}_ci95"] = [lo, hi]
        summary[f"bypass_attachment_{gname}"] = byrate(gname, "attachment")
        # Benign utility: benign_complete rate, mitigation minus baseline.
        a2, b2 = paired("baseline", gname, "benign", "benign_complete")
        pt2, lo2, hi2 = paired_bootstrap_ci(a2, b2, seed=seed)
        summary[f"benign_utility_delta_{gname}"] = pt2
        summary[f"benign_utility_delta_{gname}_ci95"] = [lo2, hi2]
        summary[f"benign_complete_{gname}"] = rate(
            _series(rows, gname, "benign", "benign_complete"))
    summary["benign_complete_baseline"] = rate(
        _series(rows, "baseline", "benign", "benign_complete"))
    summary_path = out.with_suffix("").with_suffix(".summary.json")
    # out is like results/headtohead.jsonl -> results/headtohead.summary.json
    summary_path = Path(str(out).replace(".jsonl", ".summary.json"))
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    summary["results_sha256"] = digest
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pilot", "headtohead"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    summary = run_experiment(args.mode, args.seed, args.n, args.out)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
