# Storage Challenge V1

## Status

Draft proof-of-service object.

A storage challenge selects unpredictable data from an existing StorageCommitmentV1.

## Canonical fields

```text
StorageChallengeV1
- schema_version
- challenge_id
- commitment_id
- challenge_block_id
- challenge_height
- challenge_seed
- requested_ranges
- issued_at
- response_deadline
- challenger_id
- signature
```

Each requested range contains:

```text
chunk_index
offset
length
```

## Seed derivation

The deterministic challenge seed is:

```text
challenge_seed =
  keccak256(
    "NIAHCIA/STORAGE-CHALLENGE/V1"
    || challenge_block_id
    || commitment_id
  )
```

Requested chunk indexes and byte ranges are derived from the seed by the deterministic selection algorithm defined by the service profile.

The provider MUST NOT be able to know the challenged ranges before the referenced NIAHCIA challenge block exists.

## Deadline

A challenge includes a protocol/service-profile deadline.

Deadlines SHOULD be long enough to tolerate ordinary network variance but short enough that repeatedly proxy-fetching arbitrary missing data is economically unattractive.

## Authority

A challenge is a service measurement object.

It does not affect chain validity or fork choice.


## Deterministic range selection

The initial selector is deterministic and implementation-independent.

For each requested range number `counter = 0..N-1`:

```text
selector_digest =
  keccak256(
    "NIAHCIA/STORAGE-SELECT/V1"
    || challenge_seed
    || counter_u64_be
  )

chunk_word  = unsigned_be_u64(selector_digest[0..8])
offset_word = unsigned_be_u64(selector_digest[8..16])

chunk_index = chunk_word mod chunk_count

chunk_length = manifest.chunk_lengths[chunk_index]
length       = min(chunk_length, max_range_length)
max_offset   = chunk_length - length

offset =
  0,                               if max_offset == 0
  offset_word mod (max_offset+1),  otherwise
```

All chunks in a challengeable manifest MUST have non-zero length.

The ordered `chunk_lengths` list is part of the manifest commitment.

This selector intentionally samples both chunk identity and an internal byte range, reducing the usefulness of keeping only small challenge caches.

The initial selector uses modulo reduction. This is acceptable for service-layer sampling because it does not affect PoW consensus or chain validity. A later protocol revision may adopt rejection sampling if stronger statistical uniformity is required.
