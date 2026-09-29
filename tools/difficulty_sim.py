#!/usr/bin/env python3
"""Deterministic NIAHCIA difficulty-candidate simulator.

This tool intentionally uses Python integers so the arithmetic model is exact
and unbounded. It is a protocol-development aid, not consensus code.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

TARGET_SECONDS = 30
WINDOW = 60
MIN_SOLVE = 1
MAX_SOLVE = 300
LOW_NUM, LOW_DEN = 7, 8
HIGH_NUM, HIGH_DEN = 9, 8


@dataclass
class Sample:
    solve_time: float
    target: float


def clamp(value: float, low: float, high: float) -> float:
    return min(high, max(low, value))


def normalized_next_target(previous: float, samples: list[Sample]) -> float:
    window = samples[-WINDOW:]
    work_time = sum(clamp(s.solve_time, MIN_SOLVE, MAX_SOLVE) * s.target for s in window)
    raw = work_time / (TARGET_SECONDS * len(window))
    return clamp(raw, previous * LOW_NUM / LOW_DEN, previous * HIGH_NUM / HIGH_DEN)


def rejected_raw_window_target(previous: float, samples: list[Sample]) -> float:
    values = sorted(clamp(s.solve_time, MIN_SOLVE, MAX_SOLVE) for s in samples[-WINDOW:])
    if len(values) == WINDOW:
        values = values[6:-6]
    observed = sum(values) / len(values)
    raw = previous * observed / TARGET_SECONDS
    return clamp(raw, previous * LOW_NUM / LOW_DEN, previous * HIGH_NUM / HIGH_DEN)


def hash_rate_for(name: str, height: int) -> float:
    if name == "steady":
        return 1.0
    if name == "2x":
        return 1.0 if height < 100 else 2.0
    if name == "10x":
        return 1.0 if height < 100 else 10.0
    if name == "90pct_drop":
        return 1.0 if height < 100 else 0.1
    if name == "oscillating":
        return 4.0 if (height // 50) % 2 else 0.25
    raise ValueError(name)


def run(name: str, algorithm, blocks: int = 400, stochastic: bool = False, seed: int = 1):
    rng = random.Random(seed)
    target = 1.0
    samples: list[Sample] = []
    rows = []

    for height in range(1, blocks + 1):
        hashrate = hash_rate_for(name, height)
        expected = TARGET_SECONDS / (hashrate * target)
        solve = rng.expovariate(1.0 / expected) if stochastic else expected
        samples.append(Sample(solve, target))
        target = algorithm(target, samples)
        rows.append((height, hashrate, solve, target))

    return rows


def summarize_step(name: str, algorithm):
    rows = run(name, algorithm)
    checkpoints = (100, 110, 130, 160, 200, 300, 400)
    print(f"\n{name}")
    print("height  solve_s   target_ratio  difficulty_ratio")
    for height in checkpoints:
        _, _, solve, target = rows[height - 1]
        print(f"{height:>6}  {solve:>7.2f}   {target:>12.6f}  {1/target:>16.6f}")


def stochastic_summary(name: str, algorithm, seeds: int = 20):
    mean_solve = []
    mean_target = []
    for seed in range(1, seeds + 1):
        rows = run(name, algorithm, blocks=1500, stochastic=True, seed=seed)
        tail = rows[500:]
        mean_solve.append(sum(row[2] for row in tail) / len(tail))
        mean_target.append(sum(row[3] for row in tail) / len(tail))

    print(
        f"{name:>12}: mean solve={sum(mean_solve)/len(mean_solve):.3f}s "
        f"mean target ratio={sum(mean_target)/len(mean_target):.6f}"
    )


def main():
    print("NIAHCIA difficulty candidate — deterministic step response")
    for scenario in ("steady", "2x", "10x", "90pct_drop"):
        summarize_step(scenario, normalized_next_target)

    print("\nRejected raw-window algorithm — 2x step demonstrates feedback oscillation")
    summarize_step("2x", rejected_raw_window_target)

    print("\nNormalized candidate — seeded stochastic steady-state")
    for scenario in ("steady", "2x", "10x", "90pct_drop"):
        stochastic_summary(scenario, normalized_next_target)


if __name__ == "__main__":
    main()
