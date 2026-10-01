# NIAHCIA Current Work / Session Handoff

**Purpose:** This is the first document a new development session should read. It is a concise handoff for the current state of NIAHCIA, the decisions that must be preserved, unresolved work, and the safest next tasks.

**Maintenance rule:** Update this file whenever current priorities, blockers, locked decisions, or major implementation state changes. Keep `docs/spec-status.md` synchronized as the detailed protocol inventory.

## How to resume work

A new session should:

1. Read this file first.
2. Read `docs/spec-status.md` for the complete specification inventory and maturity/status of each protocol surface.
3. Read `docs/why-niahcia.md` for the architectural rationale and differentiation NIAHCIA is trying to preserve.
4. Read the relevant specification before changing implementation behavior.
5. Inspect the current `niahcia/niahcia` implementation and open/failed GitHub work before making code changes.
6. Keep both implementation documentation and `niahcia-protocol` documentation synchronized with code changes.
7. Do not silently replace locked interoperability behavior. If a locked rule must change, version it explicitly and update its vectors/specification.

## Project objective

NIAHCIA is a decentralized AI + blockchain network designed to separate several responsibilities cleanly:

- CPU proof-of-work secures canonical chain consensus.
- RandomX is the current PoW candidate.
- GPU/accelerator workers perform AI inference and other compute jobs and are rewarded separately from mining.
- Service/storage nodes provide storage, archival, relay, snapshot, observation, and measurable proof-of-service functions without becoming a second consensus authority.
- Agents, models, execution profiles, jobs, capabilities, memory, verification policies, and payment plans are explicit protocol objects rather than assumptions hidden inside one application.
- Smart-contract/EVM execution is integrated through Reth while NIAHCIA retains its own chain identity and consensus boundary.

The rationale behind this composition is documented in `docs/why-niahcia.md`. The intended differentiation is the protocol-native relationship between independently replaceable consensus, compute, storage, verification, agents, and settlement—not dependence on one particular AI model or provider.

A newly explicit differentiation objective is **portable agent sovereignty**: an agent's identity, authorized state, capabilities, economic relationships, lineage, and execution history should remain protocol-resolvable independently of whichever physical host currently executes it.

A corresponding storage objective is **economically maintained, self-healing persistence**: agents and publishers should eventually be able to fund explicit durability obligations while independent providers repair lost replicas from surviving canonical content without a permanent storage coordinator.

## Fundamental architecture rules

These decisions should be treated as architectural invariants unless deliberately revisited:

### Consensus

CPU PoW is the chain-security authority. Fork choice is based on cumulative valid PoW work.

Service/storage nodes do **not** vote on, finalize, veto, or otherwise choose the canonical chain. Their role is to observe, preserve, relay, prove availability/service, and provide independently verifiable evidence.

### Compute

AI compute is not required of miners. GPU/accelerator compute and CPU mining are separate economic/service roles.

The compute protocol must remain capable of supporting different models, runtimes, hardware, verification mechanisms, and workload types without requiring PoW consensus redesign.

Execution hosts are replaceable resources. Hosting an agent MUST NOT automatically grant ownership/control of the agent, its treasury, or its full capabilities.

### Verification

Do not assume a universal fixed 2-of-3 execution scheme. The earlier Prototype-0 fixed redundant 2-of-3 assumption is superseded.

Verification is policy-driven through `VerificationPolicy`; individual workloads may eventually use redundant execution, optimistic verification, auditing, TEEs, proof systems, or other explicitly defined mechanisms.

### Service nodes

Proof-of-service is payment/reward evidence, not chain work. Service-node status must never create fork-choice authority.

Storage providers may store ciphertext and prove possession/availability without receiving decryption, agent governance, treasury, capability, or succession authority.

Distinct provider keys are not proof of independent durability. Unknown provider independence must remain unknown rather than being promoted to independent merely to satisfy a replica target.

### Canonical protocol data

NCE/1 deterministic CBOR is the protocol serialization foundation for canonical protocol objects. JSON is suitable for APIs/debugging but is not the canonical hashed representation.

Persistent identifiers, signing digests, and commitments require explicit domain separation and deterministic serialization.

## Locked / substantially defined work

The protocol repository currently contains specifications and/or interoperability fixtures for core consensus, canonical serialization, identities, addresses, agent/compute/service objects, storage commitments/challenges/responses/Merkle structures, proof-of-service, service epoch reports, service-node security, snapshots, and relay/availability evidence.

See `docs/spec-status.md` for the authoritative detailed inventory and status rather than assuming every listed item is frozen.

## New portable-agent candidates

`AgentManifestV1` (`spec/agent-manifest-v1.md`) defines the candidate portability contract binding an exact AgentVersion to lineage, model/execution policy, capabilities, memory descriptors, payment policy, privacy policy, succession policy, and storage manifests.

`ExecutionReceiptV1` (`spec/execution-receipt-v1.md`) defines a candidate privacy-aware execution receipt binding a Job to the exact agent/version/manifest, model/profile, worker, result commitment, verification policy/evidence, resource-accounting commitment, and settlement commitment.

Do not prematurely lock succession state-machine semantics, concrete privacy classes, host scheduling/selection, reputation/ranking, receipt inclusion/on-chain commitment, one TEE/privacy vendor, or deterministic-output requirements for all AI jobs.

## New storage durability candidates

### StorageAgreementV1

`spec/storage-agreement-v1.md` expresses that an exact content-addressed object should remain available for a defined duration with a target/minimum provider level, storage profile, challenge/retrieval policy, payment plan/budget, privacy policy, renewal policy, and recovery policy.

Initial implementation direction is straightforward chunked replication. Erasure coding is a future versioned storage profile rather than a pre-alpha requirement.

### StorageHealthV1

`spec/storage-health-v1.md` defines the candidate observational lifecycle:

```text
HEALTHY -> DEGRADED -> AT_RISK -> RECOVERING -> HEALTHY
                              -> UNAVAILABLE
EXPIRED
```

Health is derived service state, **not chain finality**. Recovery should be permissionless: an eligible provider can discover an under-replicated exact object, retrieve surviving canonical chunks, verify/reconstruct it, begin serving it, and restore durability without permission from a failed provider or original publisher.

Implementation follow-up is tracked in `niahcia/niahcia#27` and is intentionally limited to non-consensus telemetry after current CI is green.

### StorageProviderIndependenceV1

`spec/storage-provider-independence-v1.md` defines a candidate conservative model for distinguishing provider identity count from actual durability evidence.

Key rule:

> five provider keys are not necessarily five independent copies.

Candidate evidence categories are `SAME_OPERATOR`, `SHARED_DOMAIN`, `UNKNOWN`, and `EVIDENCE_OF_SEPARATION`. `UNKNOWN` remains unknown; it is not promoted to independent merely to satisfy a target.

The model may eventually consider operator linkage, network/ASN domains, facility/infrastructure domains, long-term correlated failures, independent observations, bonds/service history, and concurrent unpredictable challenges. No one signal proves independence and no production independence score is locked.

NIAHCIA must not require one central KYC, cloud, geolocation, or infrastructure authority to decide provider eligibility. Exact physical addresses and other unnecessary sensitive provider information should not be required publicly.

A future StorageAgreement revision should be able to bind a versioned `independence_policy_id`, but the current candidate hash/schema is not being casually modified while CI is red. That change should be made with NCE/1 field allocation and vectors.

### Storage threat model status

`docs/threat-model.md` now explicitly covers Sybil replicas, correlated failure domains, just-in-time storage, challenge replay, fake retrieval/bandwidth farming, deliberate degradation/repair farming, withholding/extortion, corrupt reconstruction, encrypted-memory authority separation, key loss, object poisoning, resource-exhaustion agreements, and StorageHealth manipulation.

Important safety conclusions:

- raw self-reported bandwidth is not sufficient for production rewards;
- storage durability and encryption-key custody are separate problems;
- storage providers must not become silent key escrow;
- repair economics must not make destruction more profitable than continuous storage;
- recovery preserves exact committed content, not semantically similar substitutes.

### Storage work deliberately left open

Do not yet lock exact storage pricing/rewards, provider independence scoring, automatic renewal semantics, encryption/key distribution, erasure-coding parameters, repair-provider selection, geographic placement, health observation windows/hysteresis, compensable bandwidth accounting, infrastructure-attestation requirements, or consensus inclusion/commitment of agreements.

These need threat modeling, canonical vectors, and devnet evidence.

## Native addresses

Address V1 is locked for pre-alpha interoperability: Bech32m, version byte `0x01`, 22-byte decoded payload (version + kind + 20-byte payload), Account kind `0x00`, Contract kind `0x01`, and HRPs `niah` / `tniah` / `dniah`.

Native addresses are the intended user-facing format. Reth's underlying 20-byte execution address is an internal interoperability representation.

## Monetary representation

The current direction is **8 decimal places**, not Ethereum-style 18 decimal places.

Consensus/accounting arithmetic must use integers, not floating point. Fee arithmetic, supply representation, denominations, chain IDs, overflow behavior, and conversion boundaries must remain explicitly specified and tested.

## RandomX and miner interoperability — important unresolved item

RandomX remains the PoW direction, but miner interoperability needs deliberate review. An important project goal is that ordinary/common RandomX mining software and pools should be able to mine NIAHCIA without requiring a custom NIAHCIA miner wherever practical.

Do **not** casually change the existing RandomX input/vector merely to make a miner work. First define the desired pool/miner interoperability boundary, then version/update consensus specification and vectors together if necessary.

Building a dedicated NIAHCIA miner is currently lower priority than ensuring common RandomX mining software can interoperate with NIAHCIA.

## Current blocker / caution

At the time this handoff was updated, GitHub work associated with **#266** was red/failing and still needed attention. Avoid stacking risky consensus changes on top of unresolved failures. Re-check current GitHub status before assuming this blocker still exists.

Formatting/CI cleanup for #266 was already identified as work to revisit. The existing reminder may also refer to this item, but GitHub state is authoritative.

## Current audit findings

While implementation CI/blockers are unresolved, prefer specification/vector cleanup that does not alter consensus behavior:

1. Add protocol-owned Address V1 interoperability vectors.
2. Add denomination/value/fee arithmetic vectors.
3. Audit and remove stale Prototype-0 language, especially old fixed 2-of-3 assumptions.
4. Cross-check NCE/1 serialization, field IDs, object type IDs, domain separation, signature preimages, and storage vectors for consistency.
5. Review AgentManifestV1, ExecutionReceiptV1, StorageAgreementV1, StorageHealthV1, and StorageProviderIndependenceV1 at protocol level only while CI is red.
6. Define canonical IDs/fields/domains and test vectors for candidates before implementation activation.
7. Ensure implementation docs and `niahcia-protocol` remain synchronized.

Consensus work needing deliberate review includes RandomX stock-miner/pool interoperability, final public-testnet RandomX epoch/seed parameters, remaining monetary/supply/fee constants, genesis/network parameters, and chain-ID namespace/finality.

## Documentation model

There are two intentional sources of technical truth and both must move with the code:

- `niahcia/niahcia` — implementation behavior/tests/documentation.
- `niahcia/niahcia-protocol` — implementation-independent architecture, formats, interoperability rules, security boundaries, research, and protocol-owned vectors.

When implementation changes protocol-visible behavior, update both sides in the same workstream.

## Development doctrine

Prefer small, testable milestones over trying to implement the complete decentralized AI network at once.

Before a public devnet/testnet milestone, prioritize deterministic consensus behavior, reproducible vectors, stable network identity, reliable node startup/sync, miner/pool interoperability, a clear execution-engine boundary, observable failures, and green CI.

Advanced AI scheduling, markets, reputation, verification, privacy, succession, storage economics, and economics can evolve behind versioned protocol objects once the chain foundation is dependable.

## What a new chat should do next

If asked simply to **continue**, do not begin a new architecture brainstorm.

Instead:

1. Check current GitHub status, especially unresolved/red work including #266 if it still exists.
2. Read `docs/spec-status.md`.
3. Compare implementation against relevant protocol specs.
4. Pick the highest-priority unresolved item that can be changed safely.
5. Implement/test it if appropriate.
6. Update implementation docs and protocol docs together.
7. Update this handoff when priorities or blockers materially change.

If CI remains blocked, continue safe vector/documentation/threat-model work rather than introducing unrelated consensus changes.

## Quick references

- `docs/CURRENT-WORK.md` — this handoff
- `docs/spec-status.md` — detailed protocol status/inventory
- `docs/why-niahcia.md` — architectural rationale
- `docs/threat-model.md` — security model
- `spec/agent-manifest-v1.md` — portable agent environment candidate
- `spec/execution-receipt-v1.md` — machine-work receipt candidate
- `spec/storage-agreement-v1.md` — durability/economic storage candidate
- `spec/storage-health-v1.md` — storage health/recovery candidate
- `spec/storage-provider-independence-v1.md` — provider/failure-domain candidate
- `spec/network-parameters-v1.md` — network parameters
- `spec/block-header-v1.md` — block header
- `spec/randomx-pow-v1.md` — RandomX consensus candidate
- `spec/canonical-serialization.md` — NCE/1
- `spec/domain-separation.md` — hash/signature domains
- `spec/address-v1.md` — native addresses
- `spec/service-node-security-v1.md` — service-node consensus boundary
- `spec/proof-of-service-v1.md` — measurable service rewards
- `test-vectors/` — interoperability fixtures

---

**Handoff principle:** A new session should be able to read this document, inspect current GitHub state, and continue the existing engineering direction without relying on chat history.