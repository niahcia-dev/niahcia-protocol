# NIAHCIA Current Work / Session Handoff

**Purpose:** First document a new development session should read. It summarizes current NIAHCIA state, decisions to preserve, unresolved work, and safest next tasks.

**Maintenance rule:** Update this file whenever priorities, blockers, locked decisions, or major implementation state change. Keep `docs/spec-status.md` synchronized as the detailed inventory.

## Resume sequence

1. Read this file.
2. Read `docs/spec-status.md`.
3. Read `docs/why-niahcia.md`.
4. Read relevant specifications before changing behavior.
5. Inspect current `niahcia/niahcia` implementation and GitHub failures/issues.
6. Keep implementation docs and `niahcia-protocol` synchronized.
7. Never silently replace locked interoperability behavior; version changes and vectors together.

## Core architecture

- CPU PoW is canonical chain authority; RandomX is current candidate.
- GPU/accelerator AI compute is separate from mining.
- Storage/service nodes provide measurable service but never fork-choice/finality authority.
- Agents/models/jobs/capabilities/memory/verification/payment are explicit protocol objects.
- Reth supplies EVM execution while NIAHCIA retains chain identity/consensus boundary.
- Key differentiation objectives: **portable agent sovereignty** and **economically maintained, self-healing persistence**.

## Non-negotiable boundaries

- CPU PoW alone determines canonical chain by cumulative valid work.
- Service/storage nodes do not vote on canonical chain.
- Execution hosts are replaceable and do not automatically own/control Agents.
- Fixed universal Prototype-0 2-of-3 verification is superseded by policy-driven verification.
- Storage may preserve ciphertext without decryption/governance/treasury/succession authority.
- Distinct storage provider keys do not prove independent durability.
- NCE/1 deterministic CBOR is the canonical serialization foundation.

## Cryptographic authority candidates

`KeyAuthorityV1`: durable NIAHCIA identity/address is distinct from one eternal key; separates signing/control, encryption, delegated/session authority, and recovery. Bulk private state uses random DEKs rather than direct wallet-key encryption. Long-term signing keys should be isolated from AI runtimes.

`KeyRotationV1`: same durable subject moves between authority epochs; stale/competing rotations require deterministic rejection.

`RecoveryPolicyV1`: opt-in recovery; candidate NONE/DESIGNATED/THRESHOLD/CONTRACT/DELAYED classes. No NIAHCIA master recovery key. Control recovery and historical memory decryption are separate.

## Secure portable execution

### AgentHostMigrationV1

`spec/agent-host-migration-v1.md`: **execution is portable; authority is not handed to the execution host.** Destination receives bounded session capability and authorized memory scope, never automatic master signing/treasury/recovery/succession authority.

Migration should work without cooperation from a dead old host when durable committed state survives. Ordinary hosts may see plaintext intentionally delivered to them; migration/encryption-at-rest is not private inference.

### AgentCheckpointV1

`spec/agent-checkpoint-v1.md` now defines the candidate durable resume boundary.

Central rule:

> Agent state can be checkpointed; external reality cannot be rolled back with it.

Checkpoints bind exact Agent, AgentVersion/Manifest, KeyAuthority epoch, parent checkpoint, monotonic sequence, memory/private-state roots, pending/completed effects, and active-job state. Checkpoints form a lineage and must not permit silent rollback.

A checkpoint is a state commitment, **not** proof that every external side effect occurred exactly once. Local uncommitted process state is not durable Agent truth.

Concurrent hosts can produce competing checkpoint children. Until branch/merge/current-state semantics are locked, those are conflicts requiring reconciliation rather than silent state merging.

### SideEffectIntentV1

`spec/side-effect-intent-v1.md` defines stable identity for payments, transactions, messages, storage mutations, tool/API calls, purchases, and agent-to-agent economic effects.

Central rule:

> Retry the intent, not a newly invented action.

The same logical retry retains the same `effect_id`. A genuinely new action gets a new effect identity. `UNKNOWN` is a first-class operational state: timeout/lost acknowledgement does not prove failure.

Where a target supports idempotency keys, `effect_id` should be used/mapped to them. Where it does not, NIAHCIA must not claim universal exactly-once execution; adapters reconcile target state before retrying.

A crash after submission but before checkpoint is a critical ambiguity case. Resume logic reconciles the existing effect before issuing another action. Checkpoint rollback never authorizes replay of a finalized external effect.

## Portable-agent objects

`AgentManifestV1`: exact AgentVersion + lineage + execution/model policy + capabilities + memory + payment/privacy/succession/storage references.

`ExecutionReceiptV1`: Job -> exact agent/version/manifest, model/profile, worker, result commitment, verification evidence, resource accounting, settlement.

Still open: succession mechanics, privacy classes, scheduling, reputation, receipt inclusion, private compute, universal deterministic-output assumptions.

## Storage candidates

`StorageAgreementV1`: exact content object, duration, provider targets, storage profile, challenge/retrieval policy, budget, privacy, renewal, recovery.

`StorageHealthV1`: `HEALTHY -> DEGRADED -> AT_RISK -> RECOVERING -> HEALTHY`, plus `UNAVAILABLE`/`EXPIRED`. Health is service state, not finality. Implementation issue `niahcia/niahcia#27` remains non-consensus telemetry after CI is green.

`StorageProviderIndependenceV1`: `SAME_OPERATOR`, `SHARED_DOMAIN`, `UNKNOWN`, `EVIDENCE_OF_SEPARATION`; no central KYC/geolocation/cloud authority.

`docs/threat-model.md` covers storage, authority/recovery, migration, signer and duplicate-execution threats.

## Native addresses

Address V1 remains locked pre-alpha: Bech32m; version `0x01`; 22-byte decoded payload; Account `0x00`; Contract `0x01`; HRPs `niah`, `tniah`, `dniah`. KeyAuthority does not alter locked address encoding.

## Monetary representation

Current direction: **8 decimals**; integer consensus/accounting arithmetic only. Fee/supply/denomination/chain-ID/overflow/conversion boundaries require explicit specs/vectors.

## RandomX interoperability

RandomX remains PoW direction. Ordinary/common RandomX miner/pool compatibility is preferred where protocol-safe. Do not change locked RandomX inputs/vectors merely for miner convenience. Dedicated NIAHCIA miner remains lower priority.

## Current blocker

At this handoff, GitHub work associated with **#266** was red/failing. Avoid risky consensus changes until rechecked/resolved. GitHub state is authoritative.

## Safe work while CI is blocked

1. Address V1 interoperability vectors.
2. Denomination/value/fee vectors.
3. Remove stale Prototype-0 fixed 2-of-3 language.
4. Cross-check NCE/1 IDs/domains/signature preimages/storage vectors.
5. Review current candidate protocol objects without activating them in implementation.
6. Allocate canonical IDs/fields/domains and vectors before implementation activation.
7. Continue adversarial review of authority, recovery, migration, checkpoint rollback, duplicate execution, and side-effect replay.
8. Design the next missing layer: multi-step workflow/compensation semantics and deterministic effect reconciliation, without claiming universal distributed transactions across external systems.
9. Keep both repositories' docs synchronized.

Deliberate consensus review still needed for RandomX stock miner/pool interoperability, public-testnet RandomX epoch/seed parameters, remaining monetary constants, genesis/network parameters, and chain-ID finalization.

## Documentation model

- `niahcia/niahcia` — implementation behavior/tests/docs.
- `niahcia/niahcia-protocol` — implementation-independent architecture, formats, interoperability rules, security boundaries, research, vectors.

Protocol-visible implementation changes update both.

## Development doctrine

Prefer small, testable milestones. Before public devnet/testnet prioritize deterministic consensus, reproducible vectors, stable network identity, reliable startup/sync, miner/pool interoperability, clear execution-engine boundary, observable failures, and green CI.

## New-session behavior

If asked simply to continue: check GitHub status/#266, read spec status, compare implementation to relevant specs, choose highest-priority safe unresolved work, test if appropriate, update both doc sources, and refresh this handoff. If CI remains blocked, continue safe specification/vector/threat-model work rather than unrelated consensus changes.

## Quick references

- `docs/CURRENT-WORK.md`
- `docs/spec-status.md`
- `docs/why-niahcia.md`
- `docs/threat-model.md`
- `spec/key-authority-v1.md`
- `spec/key-rotation-v1.md`
- `spec/recovery-policy-v1.md`
- `spec/agent-host-migration-v1.md`
- `spec/agent-checkpoint-v1.md`
- `spec/side-effect-intent-v1.md`
- `spec/agent-manifest-v1.md`
- `spec/execution-receipt-v1.md`
- `spec/storage-agreement-v1.md`
- `spec/storage-health-v1.md`
- `spec/storage-provider-independence-v1.md`
- `spec/address-v1.md`
- `spec/network-parameters-v1.md`
- `spec/block-header-v1.md`
- `spec/randomx-pow-v1.md`
- `spec/canonical-serialization.md`
- `spec/domain-separation.md`
- `test-vectors/`

---

**Handoff principle:** A new session should be able to read this document, inspect current GitHub state, and continue without relying on chat history.