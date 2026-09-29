# NIAHCIA ASERT Difficulty Candidate

## Status

Research candidate. **Not frozen consensus.**

The first rolling-window difficulty candidates exposed two undesirable behaviors in simulation:

1. raw moving-window target adjustment oscillated badly after large hashrate changes,
2. even the target-normalized rolling estimator performed poorly under deliberate periodic hashrate switching.

NIAHCIA is therefore evaluating an anchor-based ASERT-style difficulty algorithm instead of trying to tune a moving average indefinitely.

## Why ASERT is being evaluated

Bitcoin Cash adopted ASERT specifically to address periodic difficulty/hashrate oscillation in its prior moving-average DAA.

The useful architectural property is that the next target is derived from an absolute schedule relative to an anchor block rather than feeding a moving window back into itself.

For NIAHCIA:

```text
ideal_block_time = 30 seconds
```

Conceptually:

```text
next_target =
  anchor_target
  * 2^(
      (
        elapsed_time
        - ideal_block_time * elapsed_blocks
      )
      / half_life
    )
```

Consensus implementation MUST use deterministic integer/fixed-point arithmetic. Floating point is simulation-only.

## Candidate half-lives

Because NIAHCIA targets 30-second blocks, directly copying Bitcoin Cash's two-day half-life would be far too sluggish in block-count terms.

The current simulation compares:

```text
2160 seconds  = 72 target blocks
4320 seconds  = 144 target blocks
8640 seconds  = 288 target blocks
```

The **4320-second (72-minute) half-life is the current leading candidate**.

It is not frozen.

## Initial simulation

Seeded stochastic simulations were run against:

- steady hashrate,
- 2x step,
- 10x step,
- 90% hashrate loss,
- 16x periodic switching (0.25x / 4x),
- recurring 10x burst mining.

The anchor-based candidate with a 4320-second half-life held long-run averages close to the 30-second target in all of these initial scenarios.

This was materially better than the target-normalized 60-block moving-window candidate under periodic switching.

## Anchor

The eventual specification must define an immutable anchor tuple:

```text
anchor_height
anchor_parent_time
anchor_target
```

For a network launched with ASERT from genesis, the network-parameter specification may define an equivalent genesis-relative anchor representation.

## Timestamp source

ASERT still depends on block timestamps, so NIAHCIA's median-time-past and future-drift validity rules remain required.

The adversarial timestamp simulation must be completed before consensus is frozen.

## Required before adoption

- exact fixed-point integer algorithm selected,
- half-life simulation expanded,
- timestamp-game analysis,
- launch/startup analysis,
- pow-limit behavior,
- exact arithmetic vectors,
- Rust implementation,
- independent implementation reproduction.

Until then, both the earlier moving-window code and this ASERT document are development experiments rather than mainnet consensus.
