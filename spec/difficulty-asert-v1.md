# NIAHCIA ASERT Difficulty Adjustment V1

## Status

Draft consensus candidate. **Not frozen.**

NIAHCIA uses an anchor-based ASERT-style difficulty controller as the leading candidate for Protocol v1.

The moving-window candidates were rejected in simulation because they produced undesirable periodic feedback behavior under hash-rate switching.

## Constants

```text
IDEAL_BLOCK_TIME = 30 seconds
HALF_LIFE        = 4320 seconds
RADIX            = 65536
```

The 4320-second half-life equals 72 minutes, or 144 target blocks.

## Inputs

The exact target computation consumes:

```text
anchor_target
anchor_height
anchor_parent_time
evaluation_height
evaluation_time
pow_limit
```

All target values are exact unsigned 256-bit integers.

The evaluation height MUST be greater than or equal to the anchor height.

## Conceptual formula

```text
next_target =
  anchor_target
  * 2^(
      (
        time_delta
        - IDEAL_BLOCK_TIME * (height_delta + 1)
      )
      / HALF_LIFE
    )
```

where:

```text
time_delta   = evaluation_time - anchor_parent_time
height_delta = evaluation_height - anchor_height
```

## Deterministic fixed-point algorithm

Consensus implementations MUST NOT use floating point.

Define:

```text
radix = 65536

exponent =
  trunc_div(
    (
      time_delta
      - 30 * (height_delta + 1)
    )
    * radix,
    4320
  )

num_shifts =
  arithmetic_shift_right(exponent, 16)

fractional =
  exponent - num_shifts * radix

factor =
  (
    195766423245049 * fractional
    + 971821376 * fractional^2
    + 5127 * fractional^3
    + 2^47
  ) >> 48
  + 65536

next_target =
  anchor_target * factor

if num_shifts < 0:
  next_target >>= -num_shifts
else:
  next_target <<= num_shifts

next_target >>= 16
```

Then:

```text
if next_target == 0:
    next_target = 1

if next_target > pow_limit:
    next_target = pow_limit
```

Signed division in the exponent step MUST truncate toward zero.

The right shift used to obtain `num_shifts` MUST be arithmetic for negative values.

## Origin of the polynomial

The integer polynomial is adapted from the published Bitcoin Cash ASERT `aserti3-2d` specification, while NIAHCIA changes the target interval and half-life for its own 30-second PoW chain.

NIAHCIA stores full 256-bit targets directly in `BlockHeaderV1`, so no Bitcoin compact-`nBits` conversion is part of the NIAHCIA algorithm.

## Anchor

Every network MUST define an immutable ASERT anchor context:

```text
anchor_height
anchor_parent_time
anchor_target
```

For a network launched with ASERT from genesis, the network-parameter specification must define an equivalent deterministic genesis-relative anchor.

The final devnet/testnet/mainnet anchor rules remain to be frozen.

## Timestamp dependency

ASERT consumes consensus block timestamps.

Therefore the NIAHCIA median-time-past and future-drift validation rules are part of the security boundary.

The difficulty algorithm does not use local wall-clock time directly.

## PoW limit

The output target is capped at the network's `pow_limit`.

There is no implicit mainnet emergency-difficulty reset.

Any special devnet/testnet recovery rule must be explicit in that network's parameters.

## Implementation

The reference node now contains a development fixed-point implementation matching this draft.

Machine-readable vectors live in:

```text
test-vectors/difficulty-asert-v1.json
```

## Before consensus freeze

Still required:

- adversarial timestamp simulation,
- long-outage simulation,
- low-hashrate launch simulation,
- pow-limit saturation tests,
- larger fixed-point vector set,
- anchor/genesis decision,
- final network `pow_limit`,
- independent implementation reproduction.

Until these are complete, ASERT remains the leading candidate rather than frozen mainnet law.
