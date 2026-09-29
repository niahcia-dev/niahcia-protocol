# Storage Response V1

## Status

Draft proof-of-service object.

A storage response proves that a service node answered a StorageChallengeV1.

## Canonical fields

```text
StorageResponseV1
- schema_version
- response_id
- challenge_id
- commitment_id
- service_node_id
- answered_at
- range_proofs
- response_bytes_hash
- signature
```

Each range proof contains:

```text
chunk_index
offset
length
returned_bytes
chunk_hash
manifest_proof
```

## Verification

A verifier MUST check:

1. the response matches the referenced challenge,
2. every requested range is present exactly once,
3. returned bytes hash to the claimed chunk/range commitment,
4. each chunk is included in the committed manifest root,
5. the response arrived before the challenge deadline,
6. the provider signature is valid.

## Proof level

A successful response proves availability for the sampled ranges at the challenge time.

It does not prove that every byte of the committed object was retained locally at every instant.
