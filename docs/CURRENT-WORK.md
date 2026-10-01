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
- GPU/accelerator AI compute is a separate economic role from mining.
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

### KeyAuthorityV1

`spec/key-authority-v1.md`: durable NIAHCIA identity/address is distinct from one eternal private key. Separates signing/control authority, encryption authority, bounded delegated/session authority, and explicit recovery policy.

Bulk private state uses random symmetric data-encryption keys (DEKs), not direct encryption with the wallet/signing key. Long-term signing keys should be isolated from AI runtimes. Structured canonical policy checks precede privileged signing.

An autonomous Agent may have its own durable NIAHCIA identity distinct from its creator/controller.

### KeyRotationV1

`spec/key-rotation-v1.md`: same durable subject can move from authority epoch N to N+1. Historical signatures remain attributable to their valid epoch; stale/competing rotations require deterministic rejection.

### RecoveryPolicyV1

`spec/recovery-policy-v1.md`: opt-in recovery candidate. Candidate classes include NONE, DESIGNATED, THRESHOLD, CONTRACT, DELAYED. No NIAHCIA master recovery key exists. Recovery normally replaces authority rather than reconstructing a lost/compromised signing key.

Control recovery and historical memory decryption are separate. Storage nodes never become silent key escrow.

## Secure portable execution

### AgentHostMigrationV1

`spec/agent-host-migration-v1.md` defines the candidate security boundary for moving Agent execution between hosts.

Central rule:

> execution is portable; authority is not handed to the execution host.

A destination host resolves the exact Agent/AgentVersion/AgentManifest and current KeyAuthority epoch, then receives only a bounded session capability and authorized memory scope. It does **not** receive the Agent's master signing key, unrestricted treasury, recovery/succession authority, or all historical memory keys.

The candidate uses envelope-encryption semantics conceptually: durable memory is ciphertext under DEKs; an authorized execution session obtains only the key material required for its permitted scope. The exact DEK-release mechanism is deliberately open (session-key wrapping, threshold release, optional attestation/private-compute profiles, etc.).

Migration must work without cooperation from a dead/failed old host when durable checkpoint/storage state survives elsewhere. Local host disk is not authoritative persistence.

### Durable checkpoints and duplicate execution

Portable execution requires an explicit committed checkpoint/state boundary. Work after the last durable checkpoint may be retried after host failure.

NIAHCIA must assume old and new hosts can temporarily execute concurrently. Safety cannot depend on “one Agent = one process.” It must come from job/session IDs, current state versions, bounded capabilities, signer policy, spending limits, replay protection, and canonical state transitions.

Exactly-once external side effects cannot be inferred from memory checkpointing. Payments/tool actions need idempotency/receipt/replay semantics of their own.

### Host confidentiality limitation

Ordinary compute hosts may see plaintext intentionally delivered to them. Migration/encryption-at-rest does not equal private inference. Stronger confidentiality requires a separately versioned private-compute mechanism; no single TEE vendor should become universal protocol authority.

## Portable-agent objects

`AgentManifestV1`: exact AgentVersion + lineage + execution/model policy + capabilities + memory + payment/privacy/succession/storage references.

`ExecutionReceiptV1`: binds a Job to exact agent/version/manifest, model/profile, worker, result commitment, verification evidence, resource accounting, and settlement while permitting private payloads to remain committed rather than public.

Still open: succession mechanics, privacy classes, scheduling, reputation, receipt inclusion, one TEE choice, universal deterministic-output assumptions.

## Storage candidates

`StorageAgreementV1`: exact content object, duration, provider targets, storage profile, challenge/retrieval policy, budget, privacy, renewal, recovery. Start with chunked replication; erasure coding later.

`StorageHealthV1`: `HEALTHY -> DEGRADED -> AT_RISK -> RECOVERING -> HEALTHY`, with `UNAVAILABLE` and `EXPIRED`. Health is service state, not finality. Implementation issue `niahcia/niahcia#27` is non-consensus telemetry only after CI is green.

`StorageProviderIndependenceV1`: categories `SAME_OPERATOR`, `SHARED_DOMAIN`, `UNKNOWN`, `EVIDENCE_OF_SEPARATION`; no central KYC/geolocation/cloud authority.

`docs/threat-model.md` covers storage Sybil/correlation, challenge/replay, fake traffic, repair farming, withholding, corrupt reconstruction, key loss, object poisoning, resource exhaustion, health manipulation, plus KeyAuthority/recovery/migration threats.

## Native addresses

Address V1 remains locked pre-alpha: Bech32m; version `0x01`; 22-byte decoded payload; Account `0x00`; Contract `0x01`; HRPs `niah`, `tniah`, `dniah`.

KeyAuthority does not alter locked address encoding; it defines versioned authority behind durable identity.

## Monetary representation

Current direction: **8 decimals**; integer consensus/accounting arithmetic only. Fee/supply/denomination/chain-ID/overflow/conversion boundaries require explicit specs/vectors.

## RandomX interoperability

RandomX remains PoW direction. Ordinary/common RandomX miner/pool compatibility is preferred where protocol-safe. Do not casually change locked RandomX inputs/vectors for miner convenience; define/version the interoperability boundary deliberately. Dedicated NIAHCIA miner remains lower priority.

## Current blocker

At this handoff, GitHub work associated with **#266** was red/failing. Avoid risky consensus changes until rechecked/resolved. GitHub state is authoritative.

## Safe work while CI is blocked

1. Address V1 interoperability vectors.
2. Denomination/value/fee vectors.
3. Remove stale Prototype-0 fixed 2-of-3 language.
4. Cross-check NCE/1 IDs/domains/signature preimages/storage vectors.
5. Review candidate AgentManifest, ExecutionReceipt, StorageAgreement, StorageHealth, StorageProviderIndependence, KeyAuthority, KeyRotation, RecoveryPolicy, and AgentHostMigration only at protocol level.
6. Allocate canonical IDs/fields/domains and vectors before implementation activation.
7. Continue adversarial review of signer isolation, recovery/guardian abuse, authority rollback, capability leakage, memory unlock, migration duplication, and side-effect replay.
8. Keep both repositories' docs synchronized.

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