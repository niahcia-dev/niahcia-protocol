# NIAHCIA Difficulty Adjustment V1

## Status

Draft algorithm for simulation. **Not frozen consensus.**

The target is approximately one block every 30 seconds.

## Initial parameters

```text
TARGET_BLOCK_INTERVAL = 30 seconds
WINDOW_BLOCKS         = 60
EXPECTED_WINDOW_TIME  = 1800 seconds
MAX_STEP_UP           = 12.5 percent
MAX_STEP_DOWN         = 12.5 percent
```

A 60-block window represents approximately 30 minutes at target rate.

## Observed time

Difficulty uses timestamps from the selected ancestor window and MUST use the timestamp validity rules from `timestamp-rules-v1.md`.

The implementation should derive a robust observed time from the window rather than using one block interval.

Before this specification is frozen, simulation MUST compare at least:

- first/last median subsets,
- trimmed interval samples,
- median interval aggregation.

## Candidate formula

The unclamped target adjustment is conceptually:

```text
candidate_target =
  previous_target
  * observed_window_time
  / expected_window_time
```

Larger target means easier work.

## Per-block clamp

The new target MUST be clamped so it cannot become more than 12.5% harder or 12.5% easier in one block.

The exact integer rounding rule and overflow-safe 256-bit arithmetic MUST be test-vectored before public testnet.

## Absolute bounds

Each network defines:

```text
pow_limit
minimum_target
```

The development network may set an intentionally easy `pow_limit`.

A calculated target MUST remain inside network bounds.

## Network restart / long outage

NIAHCIA SHOULD NOT include an implicit emergency difficulty reset.

If devnet or testnet needs a special minimum-difficulty rule, that rule must be explicit in that network's parameters and MUST NOT silently become mainnet behavior.

## Fork choice

Difficulty does not directly select the chain.

Every valid block contributes exact block work derived from target, and fork choice uses cumulative work.

## Before freezing

This draft MUST be simulated against:

- steady hash rate
- 2x/4x/10x hash-rate increases
- equivalent decreases
- miner timestamp manipulation
- long outages
- burst mining
- oscillating hash rate
- low-hashrate startup

The chosen formula, rounding, clamps, and vectors become consensus only after those simulations.
