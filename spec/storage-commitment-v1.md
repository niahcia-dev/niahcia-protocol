# Storage Commitment V1

## Status

Draft proof-of-service object.

A storage commitment records a service node's promise to retain retrievable content for a stated period.

## Canonical fields

```text
StorageCommitmentV1
- schema_version
- commitment_id
- service_node_id
- operator_id
- service_class
- object_id
- manifest_root
- chunk_count
- total_bytes
- retained_from_block
- retained_until_block
- commitment_nonce
- created_block
- signature
```

## Rules

- `manifest_root` MUST commit to the complete ordered chunk manifest.
- `chunk_count` and `total_bytes` MUST match the manifest.
- `service_class` MUST be one of the storage-bearing service classes defined by the service-node specification.
- the retention interval is inclusive of `retained_from_block` and exclusive of `retained_until_block`.
- `commitment_nonce` prevents accidental commitment-ID collisions for otherwise identical commitments.
- the provider signature proves authorship of the commitment, not successful service.

## Commitment ID

```text
commitment_id =
  digest(
    purpose = "ID/STORAGE_COMMITMENT",
    canonical object with commitment_id and signature excluded
  )
```

## Reward meaning

A StorageCommitmentV1 creates eligibility to prove service.

It does not by itself create a reward entitlement.
