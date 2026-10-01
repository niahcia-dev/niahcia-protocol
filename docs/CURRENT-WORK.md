# NIAHCIA Current Work / Session Handoff

**Purpose:** This is the first document a new development session should read. It is a concise handoff for current NIAHCIA state, decisions that must be preserved, unresolved work, and the safest next tasks.

**Maintenance rule:** Update this file whenever priorities, blockers, locked decisions, or major implementation state changes. Keep `docs/spec-status.md` synchronized as the detailed protocol inventory.

## How to resume work

1. Read this file first.
2. Read `docs/spec-status.md` for the complete specification inventory/maturity.
3. Read `docs/why-niahcia.md` for architectural rationale.
4. Read the relevant specification before changing implementation behavior.
5. Inspect current `niahcia/niahcia` implementation and open/failed GitHub work.
6. Keep implementation documentation and `niahcia-protocol` synchronized with code changes.
7. Never silently replace locked interoperability behavior; version changes and update vectors/specification together.

## Project objective

NIAHCIA is a decentralized AI + blockchain network with deliberately separated responsibilities:

- CPU proof-of-work secures canonical chain consensus; RandomX is the current candidate.
- GPU/accelerator workers execute AI/compute jobs and are rewarded separately from mining.
- Service/storage nodes provide storage, archival, relay, snapshots, observations, and measurable proof-of-service without becoming consensus authorities.
- Agents, models, execution profiles, jobs, capabilities, memory, verification policies, and payment plans are explicit protocol objects.
- Smart-contract/EVM execution integrates through Reth while NIAHCIA retains its chain identity/consensus boundary.

Key differentiation objectives are **portable agent sovereignty** and **economically maintained, self-healing persistence**.

## Fundamental architecture rules

### Consensus

CPU PoW is the chain-security authority. Fork choice is cumulative valid PoW work. Service/storage nodes do not vote on, finalize, veto, or choose the canonical chain.

### Compute

AI compute is not required of miners. Execution hosts are replaceable resources and MUST NOT automatically gain agent ownership, treasury control, or full capabilities.

### Verification

The old Prototype-0 universal fixed 2-of-3 assumption is superseded. Verification is policy-driven through `VerificationPolicy`.

### Service/storage

Proof-of-service is payment/reward evidence, not chain work. Storage may preserve ciphertext without decryption/governance/treasury/succession authority. Distinct provider keys are not proof of independent durability; unknown independence remains unknown.

### Canonical data

NCE/1 deterministic CBOR is the canonical serialization foundation. Persistent identifiers, signing digests, and commitments require explicit domain separation and deterministic serialization.

## Cryptographic authority direction

The current candidate direction is now explicit:

> Every protocol actor and economically controlled resource ultimately resolves to NIAHCIA cryptographic authority, but one private key must not perform every cryptographic role.

A durable NIAHCIA address/entity is distinct from one eternal private key. Versioned authority epochs allow keys to rotate while identity remains stable.

### KeyAuthorityV1

`spec/key-authority-v1.md` defines the candidate separation between:

- durable NIAHCIA identity/address;
- signing/control authority;
- encryption authority;
- bounded delegated/session authority;
- explicit recovery policy.

Bulk agent memory/private objects should use random symmetric data-encryption keys (DEKs), with access controlled/wrapped under versioned encryption authority. Do **not** directly encrypt all agent state with the wallet/signing private key.

Long-term private signing keys should not normally be exposed to AI runtimes. A signer/key service should validate canonical operations against capabilities/policy/budgets before signing. Natural-language model output is untrusted input, never sufficient privileged authorization.

An autonomous Agent should be capable of possessing its own durable NIAHCIA cryptographic identity distinct from its creator/controller.

### KeyRotationV1

`spec/key-rotation-v1.md` defines candidate auditable authority transitions:

```text
same durable subject/address
  authority epoch N
       -> authorized rotation
  authority epoch N+1
```

Historical signatures remain attributable to the epoch valid when created. Competing/stale rotations require deterministic rejection. Rotation limits future compromise but cannot make already exposed plaintext secret again.

### RecoveryPolicyV1

`spec/recovery-policy-v1.md` defines opt-in recovery. Candidate policy classes include NONE, DESIGNATED, THRESHOLD, CONTRACT, and DELAYED, but exact semantics are not locked.

There is **no NIAHCIA master recovery key**. Miners, storage nodes, compute hosts, developers, websites, and service nodes gain no implicit recovery authority.

A successful recovery should normally authorize replacement/rotation into a new KeyAuthority epoch rather than reconstruct the old lost/compromised signing key.

Control recovery and historical memory decryption are separate. A policy may deliberately make old encrypted memory unrecoverable, provide threshold recovery of selected key material, or permit only future encryption-key rotation. Storage nodes must never become silent key escrow.

## Portable-agent candidates

`AgentManifestV1` binds an exact AgentVersion to lineage, model/execution policy, capabilities, memory descriptors, payment/privacy/succession policy, and storage manifests.

`ExecutionReceiptV1` binds a Job to exact agent/version/manifest, model/profile, worker, result commitment, verification evidence, resource accounting, and settlement while permitting private inputs/results to remain committed rather than disclosed.

Do not prematurely lock succession mechanics, privacy classes, scheduling, reputation, receipt inclusion, one TEE vendor, or universal deterministic-output requirements.

## Storage durability candidates

### StorageAgreementV1

Defines exact content-addressed object, duration, target/minimum provider level, storage profile, challenge/retrieval policy, payment/budget, privacy, renewal, and recovery. Initial direction is chunked replication; erasure coding remains a future versioned profile.

### StorageHealthV1

Candidate lifecycle:

```text
HEALTHY -> DEGRADED -> AT_RISK -> RECOVERING -> HEALTHY
                              -> UNAVAILABLE
EXPIRED
```

Health is service state, not finality. Recovery should be permissionless from surviving canonical content. Implementation follow-up `niahcia/niahcia#27` is intentionally non-consensus telemetry only after CI is green.

### StorageProviderIndependenceV1

Separates provider identity count from actual durability evidence. Categories: `SAME_OPERATOR`, `SHARED_DOMAIN`, `UNKNOWN`, `EVIDENCE_OF_SEPARATION`. No centralized KYC/geolocation/cloud authority should decide network-wide storage eligibility.

### Storage threat conclusions

`docs/threat-model.md` covers Sybil replicas, correlated failure domains, just-in-time storage, replay, fake retrieval/bandwidth farming, repair farming, withholding/extortion, corrupt reconstruction, encrypted-memory authority separation, key loss, object poisoning, resource exhaustion, and health manipulation.

Do not yet lock storage pricing/rewards, provider-independence scoring, automatic renewal, encryption/key distribution, erasure coding, repair selection, geography, health windows/hysteresis, bandwidth accounting, infrastructure attestation, or agreement consensus inclusion.

## Native addresses

Address V1 is locked for pre-alpha interoperability: Bech32m; version `0x01`; 22-byte decoded payload (version + kind + 20-byte payload); Account `0x00`; Contract `0x01`; HRPs `niah`, `tniah`, `dniah`.

Native addresses are user-facing identity. Reth's 20-byte execution address is an internal interoperability representation.

The new KeyAuthority candidate does **not** change locked Address V1 encoding. It defines how durable identities can resolve versioned authority without changing address presentation.

## Monetary representation

Current direction is **8 decimal places**. Consensus/accounting arithmetic uses integers, never floating point. Fee/supply/denomination/chain-ID/overflow/conversion boundaries require explicit specification and vectors.

## RandomX interoperability

RandomX remains the PoW direction. A key project goal is ordinary/common RandomX miner and pool compatibility wherever protocol-safe. Do not casually change locked RandomX input/vectors merely to make a miner work; define the interoperability boundary and version consensus/vector changes together if necessary. A dedicated NIAHCIA miner is lower priority.

## Current blocker / caution

At this handoff, GitHub work associated with **#266** was red/failing. Avoid stacking risky consensus changes until rechecked/resolved. Formatting/CI cleanup was already identified. GitHub state is authoritative.

## Safe work while CI is blocked

1. Protocol-owned Address V1 interoperability vectors.
2. Denomination/value/fee arithmetic vectors.
3. Remove stale Prototype-0 fixed 2-of-3 language.
4. Cross-check NCE/1 serialization, IDs, domains, signature preimages, and storage vectors.
5. Review candidate AgentManifest, ExecutionReceipt, StorageAgreement, StorageHealth, StorageProviderIndependence, KeyAuthority, KeyRotation, and RecoveryPolicy at protocol level only.
6. Allocate canonical IDs/fields/domains and create vectors before activating candidates in implementation.
7. Threat-model signer isolation, recovery abuse, guardian compromise, key-epoch rollback, capability leakage, and encrypted-memory continuity.
8. Keep both repositories' documentation synchronized.

Consensus work needing deliberate review includes RandomX stock-miner/pool interoperability, public-testnet RandomX epoch/seed parameters, remaining monetary/supply/fee constants, genesis/network parameters, and chain-ID finalization.

## Documentation model

- `niahcia/niahcia` — implementation behavior/tests/docs.
- `niahcia/niahcia-protocol` — implementation-independent architecture, formats, interoperability rules, security boundaries, research, and protocol vectors.

When implementation changes protocol-visible behavior, update both in the same workstream.

## Development doctrine

Prefer small, testable milestones. Before public devnet/testnet prioritize deterministic consensus, reproducible vectors, stable network identity, reliable startup/sync, miner/pool interoperability, clear execution-engine boundary, observable failures, and green CI.

Advanced scheduling, markets, reputation, verification, privacy, succession, storage economics, and autonomous-agent economics can evolve behind versioned protocol objects afterward.

## What a new chat should do next

If asked simply to continue:

1. Check GitHub status, especially #266 if it still exists/red.
2. Read `docs/spec-status.md`.
3. Compare implementation against relevant protocol specs.
4. Pick the highest-priority safe unresolved item.
5. Implement/test only if appropriate.
6. Update both implementation and protocol docs.
7. Update this handoff when priorities/blockers change.

If CI remains blocked, continue safe vector/documentation/threat-model work rather than unrelated consensus changes.

## Quick references

- `docs/CURRENT-WORK.md`
- `docs/spec-status.md`
- `docs/why-niahcia.md`
- `docs/threat-model.md`
- `spec/key-authority-v1.md`
- `spec/key-rotation-v1.md`
- `spec/recovery-policy-v1.md`
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

**Handoff principle:** A new session should be able to read this document, inspect current GitHub state, and continue the existing engineering direction without relying on chat history.