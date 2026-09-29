# ServiceNode

## Purpose

`ServiceNode` represents a bonded provider of persistent network services.

Storage is the initial service, not the permanent limit.

## Canonical fields

```text
ServiceNode
- schema_version
- service_node_id
- operator_id
- controller
- payment_address
- services[]
- storage_capacity
- bandwidth_class
- stored_manifests[]
- availability_state
- endpoint_descriptor
- pricing_policy
- bond
- reputation_ref
- status
```

## Service classes

Initial/future vocabulary:

```text
MODEL_STORAGE
MEMORY_STORAGE
ARTIFACT_STORAGE
DATASET_STORAGE
ROUTING
INDEXING
ARCHIVE
VERIFICATION
```

A node may advertise several services.

## Storage integrity

Storage services MUST be content-addressed. Retrieval clients verify received content against registered manifests/hashes.

## Availability

Service rewards SHOULD depend on measurable activity such as:

- successful retrievals
- storage availability challenges
- replication commitments
- routing/serving work

Collateral ownership alone MUST NOT entitle a node to service rewards.

## Status

```text
ACTIVE
DRAINING
SUSPENDED
EXITED
```

## Invariants

1. Service nodes do not participate in PoW fork choice by virtue of service-node status.
2. Stored content MUST be independently integrity-verifiable.
3. Service claims MUST be explicit and auditable.
4. Payment for one service class MUST NOT imply entitlement to another.

## Prototype 0

Prototype 0 enables MODEL_STORAGE, model manifest/chunk serving, basic availability tracking, and test retrieval accounting.
