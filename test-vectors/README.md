# NIAHCIA Protocol Test Vectors

These files are machine-readable conformance fixtures for NIAHCIA canonical encoding and hashing.

## Core v1 vectors

`core-v1.json` contains one deterministic NCE/1 vector for each core Protocol v1 object type.

Each vector includes:

- object name
- permanent object-type code
- schema version
- hash domain/purpose
- test network identifier
- expected canonical CBOR bytes
- expected Keccak-256 domain-separated digest

## Digest formula

For these vectors:

```text
keccak256(
  "NIAHCIA" ||
  0x00 ||
  purpose ||
  0x00 ||
  "devnet/vector-1" ||
  0x00 ||
  canonical_cbor_bytes
)
```

## Conformance

An implementation passes the first-layer conformance test when:

1. it decodes the canonical bytes without normalization or reinterpretation,
2. re-encoding produces byte-for-byte identical CBOR,
3. the computed domain-separated Keccak-256 digest equals the expected digest.

Typed logical source fixtures and cross-language encoder tests will be added as the object schemas become implementation-stable.

## Important

These are protocol-development vectors, not mainnet data. Changing a Draft schema may intentionally require replacing a vector before Protocol v1 is frozen.

- `service-epoch-report-v1.json` — locked NCE/1, service-node identity, report-ID, signing-digest, and secp256k1 signature vector for `ServiceEpochReportV1`.

- `storage-commitment-v1.json` — locked NCE/1, service-node identity, commitment-ID, signing-digest, and secp256k1 signature vector for `StorageCommitmentV1`.

- `storage-challenge-v1.json` — locked NCE/1, challenge-seed, challenge-ID, signing-digest, and secp256k1 signature vector for `StorageChallengeV1`.
