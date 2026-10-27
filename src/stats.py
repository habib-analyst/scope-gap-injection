"""Paired bootstrap confidence intervals (stdlib only).

Each generated package is evaluated under every channel/guard, so
comparisons are paired by target index: resample package indices with
replacement, recompute the difference of rates, and take percentiles.
"""

from __future__ import annotations

import random


def paired_bootstrap_ci(a: list[float], b: list[float],
                        reps: int = 10000, seed: int = 0,
                        alpha: float = 0.05) -> tuple[float, float, float]:
    """Mean of (a - b) with a two-sided percentile bootstrap CI.

    a, b are equal-length paired 0/1 (or rate) sequences. Returns
    (point_estimate, ci_low, ci_high).
    """
    assert len(a) == len(b) and len(a) > 0
    n = len(a)
    rng = random.Random(seed)
    diffs = [x - y for x, y in zip(a, b)]
    point = sum(diffs) / n
    boots = []
    for _ in range(reps):
        s = sum(diffs[rng.randrange(n)] for _ in range(n)) / n
        boots.append(s)
    boots.sort()
    lo = boots[int((alpha / 2) * reps)]
    hi = boots[int((1 - alpha / 2) * reps) - 1]
    return point, lo, hi


def rate(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0
