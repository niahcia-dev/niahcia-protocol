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

CPU PoW alone determines canonical chain by cumulative valid work. Service/storage nodes do not vote on canonical chain. Execution hosts are replaceable and do not automatically own/control Agents. Fixed Prototype-0 universal 2-of-3 verification is superseded by policy-driven verification. Storage may preserve ciphertext without decryption/governance/treasury/succession authority. Distinct provider keys do not prove independent durability. NCE/1 deterministic CBOR is canonical serialization foundation.

## Cryptographic authority candidates

`KeyAuthorityV1`: durable NIAHCIA identity/address differs from one eternal key; separates signing/control, encryption, delegated/session authority, and recovery. Bulk private state uses random DEKs. Long-term signing keys should be isolated from AI runtimes.

`KeyRotationV1`: same durable subject moves between authority epochs; stale/competing rotations require deterministic rejection.

`RecoveryPolicyV1`: opt-in recovery; candidate NONE/DESIGNATED/THRESHOLD/CONTRACT/DELAYED classes. No NIAHCIA master recovery key. Control recovery and historical memory decryption are separate.

## Portable execution and continuity

`AgentHostMigrationV1`: **execution is portable; authority is not handed to the execution host.** Destination receives bounded session capability and authorized memory scope, not master signing/treasury/recovery/succession authority. Migration can continue without a dead old host when durable state survives.

`AgentCheckpointV1`: **Agent state can be checkpointed; external reality cannot be rolled back with it.** Checkpoints bind Agent/version/manifest/authority epoch, lineage, memory/private-state roots, pending/completed effects, and active jobs. Local uncommitted process state is not durable Agent truth.

`SideEffectIntentV1`: **retry the intent, not a newly invented action.** Same logical retry retains the same effect ID. `UNKNOWN` is first-class; timeout/lost acknowledgement does not prove failure. Target-native idempotency is used where available. NIAHCIA does not claim universal exactly-once behavior for external systems that cannot provide it.

## Multi-step autonomous work

### AgentWorkflowV1

`spec/agent-workflow-v1.md` now defines the candidate durable multi-step orchestration model.

Central rule:

> A workflow is a durable state machine, not a distributed database transaction.

A workflow may coordinate compute, payments, contracts, storage, messages, APIs/tools, purchases, and agent-to-agent actions. Arbitrary external systems are never assumed to share one atomic commit/rollback boundary.

Each externally visible step uses `SideEffectIntentV1` where applicable. A step that times out enters `UNKNOWN`; reconciliation happens before retry. If safety cannot be established, the workflow may remain unknown or enter `MANUAL_REVIEW` rather than guessing.

### Compensation is not rollback

If a completed step must be undone economically/operationally, compensation is a **new forward action** with its own effect identity, authority, budget, receipt, and failure state. Examples include refunding a payment, cancelling a reservation where possible, revoking a capability, or issuing a corrective action.

Some actions are irreversible. Workflow policy should identify them explicitly and, where appropriate, defer them until reversible prerequisites complete or require explicit controller approval.

### Migration and workflow continuity

Workflow, step, effect, and budget identities survive host migration. Moving to another GPU host never resets spend limits or permits a fresh payment merely because execution restarted.

Duplicate hosts are expected. Canonical workflow state, signer policy, stable effect IDs, budgets, capabilities, and target idempotency/reconciliation contain the race.

Agent-to-agent workflows preserve each Agent's independent authority. One Agent cannot roll back another Agent's finalized state because its own workflow later fails.

## Portable-agent objects

`AgentManifestV1`: exact AgentVersion + lineage + execution/model policy + capabilities + memory + payment/privacy/succession/storage references.

`ExecutionReceiptV1`: Job -> exact agent/version/manifest, model/profile, worker, result commitment, verification evidence, resource accounting, settlement.

Still open: succession mechanics, privacy classes, scheduling, reputation, receipt inclusion, private compute, universal deterministic-output assumptions.

## Storage candidates

`StorageAgreementV1`: exact content, duration, provider targets, profile, challenge/retrieval policy, budget, privacy, renewal, recovery.

`StorageHealthV1`: `HEALTHY -> DEGRADED -> AT_RISK -> RECOVERING -> HEALTHY`, plus `UNAVAILABLE`/`EXPIRED`. Health is service state, not finality. `niahcia/niahcia#27` remains non-consensus telemetry after CI is green.

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
5. Review candidate protocol objects without activating them in implementation.
6. Allocate canonical IDs/fields/domains and vectors before implementation activation.
7. Continue adversarial review of authority, recovery, migration, checkpoint rollback, duplicate execution, side-effect replay, workflow compensation, and budget abuse.
8. Next portable-agent gap: define deterministic effect receipts/reconciliation evidence and how workflow state learns that an external action is OBSERVED/FINALIZED without trusting the execution host's assertion.
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
- `spec/agent-workflow-v1.md`
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