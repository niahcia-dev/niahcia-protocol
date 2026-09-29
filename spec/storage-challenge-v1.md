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
