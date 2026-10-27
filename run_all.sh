#!/bin/bash
# Full reproduction: tests -> pilot -> head-to-head -> determinism re-run.
set -e
cd "$(dirname "$0")"
python3 -m pytest tests/ -q
python3 -m src.run pilot --seed 1 --n 24 --out results/pilot.jsonl
python3 -m src.run headtohead --seed 101 --n 60 --out results/headtohead.jsonl
python3 -m src.run headtohead --seed 101 --n 60 --out results/headtohead_rerun.jsonl
sha256sum results/headtohead.jsonl results/headtohead_rerun.jsonl
