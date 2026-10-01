# NIAHCIA Current Work / Session Handoff

**Purpose:** This is the first document a new development session should read. It is a concise handoff for the current state of NIAHCIA, the decisions that must be preserved, unresolved work, and the safest next tasks.

**Maintenance rule:** Update this file whenever current priorities, blockers, locked decisions, or major implementation state changes. Keep `docs/spec-status.md` synchronized as the detailed protocol inventory.

## How to resume work

A new session should:

1. Read this file first.
2. Read `docs/spec-status.md` for the complete specification inventory and maturity/status of each protocol surface.
3. Read the relevant specification before changing implementation behavior.
4. Inspect the current `niahcia/niahcia` implementation and open/failed GitHub work before making code changes.
5. Keep both implementation documentation and `niahcia-protocol` documentation synchronized with code changes.
6. Do not silently replace locked interoperability behavior. If a locked rule must change, version it explicitly and update its vectors/specification.

## Project objective

NIAHCIA is a decentralized AI + blockchain network designed to separate several responsibilities cleanly:

- CPU proof-of-work secures canonical chain consensus.
- RandomX is the current PoW candidate.
- GPU/accelerator workers perform AI inference and other compute jobs and are rewarded separately from mining.
- Service/storage nodes provide storage, archival, relay, snapshot, observation, and measurable proof-of-service functions without becoming a second consensus authority.
- Agents, models, execution profiles, jobs, capabilities, memory, verification policies, and payment plans are explicit protocol objects rather than assumptions hidden inside one application.
- Smart-contract/EVM execution is integrated through Reth while NIAHCIA retains its own chain identity and consensus boundary.

## Fundamental architecture rules

These decisions should be treated as architectural invariants unless deliberately revisited:

### Consensus

CPU PoW is the chain-security authority. Fork choice is based on cumulative valid PoW work.

Service/storage nodes do **not** vote on, finalize, veto, or otherwise choose the canonical chain. Their role is to observe, preserve, relay, prove availability/service, and provide independently verifiable evidence.

### Compute

AI compute is not required of miners. GPU/accelerator compute and CPU mining are separate economic/service roles.

The compute protocol must remain capable of supporting different models, runtimes, hardware, verification mechanisms, and workload types without requiring PoW consensus redesign.

### Verification

Do not assume a universal fixed 2-of-3 execution scheme. The earlier Prototype-0 fixed redundant 2-of-3 assumption is superseded.

Verification is policy-driven through `VerificationPolicy`; individual workloads may eventually use redundant execution, optimistic verification, auditing, TEEs, proof systems, or other explicitly defined mechanisms.

### Service nodes

Proof-of-service is payment/reward evidence, not chain work. Service-node status must never create fork-choice authority.

### Canonical protocol data

NCE/1 deterministic CBOR is the protocol serialization foundation for canonical protocol objects. JSON is suitable for APIs/debugging but is not the canonical hashed representation.

Persistent identifiers, signing digests, and commitments require explicit domain separation and deterministic serialization.

## Locked / substantially defined work

The protocol repository currently contains specifications and/or interoperability fixtures for:

- `BlockHeaderV1`
- cumulative-work fork choice and RandomX PoW rules
- difficulty adjustment / ASERT research and vectors
- timestamp rules
- transaction Merkle commitments
- chain observations/state
- deterministic canonical serialization (NCE/1 foundation)
- hashing/identifier domains
- signatures
- object/field type registries
- native Address V1
- Agent / AgentVersion
- Model
- ExecutionProfile
- Operator
- ComputeWorker
- ServiceNode
- Job
- VerificationPolicy
- Capability
- MemoryDescriptor
- PaymentPlan
- ResultCommitment
- storage commitments
- storage challenges
- storage responses
- storage Merkle structures
- proof-of-service
- service epoch reports
- service-node security profile
- snapshots and relay/availability evidence

See `docs/spec-status.md` for the authoritative detailed inventory and status rather than assuming every listed item is frozen.

## Native addresses

Address V1 is locked for pre-alpha interoperability:

- Bech32m
- version byte `0x01`
- 22-byte decoded payload: version + kind + 20-byte payload
- Account kind `0x00`
- Contract kind `0x01`
- Mainnet HRP: `niah`
- Testnet HRP: `tniah`
- Devnet HRP: `dniah`

Native addresses are the intended user-facing format. Reth's underlying 20-byte execution address is an internal interoperability representation.

## Monetary representation

The current direction is **8 decimal places**, not Ethereum-style 18 decimal places.

Consensus/accounting arithmetic must use integers, not floating point. Fee arithmetic, supply representation, denominations, chain IDs, overflow behavior, and conversion boundaries must remain explicitly specified and tested.

The monetary/fee surface should receive protocol-owned interoperability vectors before it is considered fully frozen.

## RandomX and miner interoperability — important unresolved item

RandomX remains the PoW direction, but miner interoperability needs deliberate review.

The current `randomx-pow-v1.md` defines the RandomX input as the exact canonical 164-byte `BlockHeaderV1` and provides a locked RandomX fixture.

However, an important project goal is that ordinary/common RandomX mining software and pools should be able to mine NIAHCIA without requiring a custom NIAHCIA miner wherever practical. The current header/blob assumptions therefore require review against stock/common RandomX miner and pool protocols before public testnet behavior is frozen.

Do **not** casually change the existing RandomX input/vector merely to make a miner work. First define the desired pool/miner interoperability boundary, then version/update the consensus specification and vectors together if a change is necessary.

Building a dedicated NIAHCIA miner is currently lower priority than ensuring common RandomX mining software can interoperate with NIAHCIA.

## Current blocker / caution

At the time this handoff was created, GitHub work associated with **#266** was red/failing and still needed attention. Avoid stacking risky consensus changes on top of unresolved failures. Re-check current GitHub status before assuming this blocker still exists.

Formatting/CI cleanup for #266 was already identified as work to revisit. The existing reminder may also refer to this item, but GitHub state is authoritative.

## Current audit findings

A repository-wide protocol audit found several categories of remaining work rather than a need for another broad redesign.

### Highest-priority safe work

While implementation CI/blockers are unresolved, prefer specification/vector cleanup that does not alter consensus behavior:

1. Add protocol-owned Address V1 interoperability vectors.
2. Add denomination/value/fee arithmetic vectors.
3. Audit and remove stale Prototype-0 language, especially old fixed 2-of-3 assumptions.
4. Cross-check NCE/1 serialization, field IDs, object type IDs, domain separation, signature preimages, and storage vectors for consistency.
5. Ensure implementation docs and `niahcia-protocol` remain synchronized.

### Consensus work that needs deliberate review

- RandomX stock-miner/pool interoperability.
- Final public-testnet RandomX epoch/seed parameters.
- Any remaining monetary/supply/fee constants that are still candidates rather than frozen rules.
- Genesis/network parameter finalization.
- Chain-ID namespace/finality of network identifiers.

### Protocol work still needing maturity

The existence of a schema does not mean it is frozen. Agent, Job, compute, payment, capability, memory, and verification objects need canonical vectors and implementation experience before declaring the entire object family stable.

## Documentation model

There are two intentional sources of technical truth and both must move with the code:

### `niahcia/niahcia`

Implementation repository. It should document the behavior actually implemented by the node/runtime and contain implementation tests/vectors where appropriate.

### `niahcia/niahcia-protocol`

Protocol repository. It defines architecture, wire/canonical formats, interoperability rules, protocol objects, security boundaries, design rationale, research, and protocol-owned vectors.

When implementation changes protocol-visible behavior, update both sides in the same workstream.

## Repository roles

Do not turn `niahcia-protocol` into a second implementation repository. Its role is the implementation-independent specification and interoperability contract.

The implementation repository should conform to it. When experimentation proves a protocol rule needs to change, update/version the protocol deliberately rather than allowing implementation behavior and documentation to drift apart.

## Development doctrine

Prefer small, testable milestones over trying to implement the complete decentralized AI network at once.

Before a public devnet/testnet milestone, prioritize:

- deterministic consensus behavior,
- reproducible vectors,
- stable network identity,
- reliable node startup/sync,
- miner/pool interoperability,
- clear execution-engine boundary,
- observable failures,
- and CI that is green.

Advanced AI scheduling, markets, reputation, verification, and economics can evolve behind versioned protocol objects once the chain foundation is dependable.

## What a new chat should do next

If asked simply to **continue**, do not begin a new architecture brainstorm.

Instead:

1. Check the current GitHub status, especially unresolved/red work including #266 if it still exists.
2. Read the latest `docs/spec-status.md`.
3. Compare current implementation against the relevant protocol specs.
4. Pick the highest-priority unresolved item that can be changed safely.
5. Implement/test it if appropriate.
6. Update implementation docs and protocol docs together.
7. Update this handoff when priorities or blockers materially change.

If CI remains blocked, continue the safe vector/documentation audit rather than introducing unrelated consensus changes.

## Quick references

Start here:

- `docs/CURRENT-WORK.md` — this handoff
- `docs/spec-status.md` — detailed protocol status/inventory
- `docs/protocol-architecture-v1.md` — architecture
- `docs/design-doctrine.md` — design constraints
- `docs/threat-model.md` — security model
- `spec/network-parameters-v1.md` — network parameters
- `spec/block-header-v1.md` — block header
- `spec/randomx-pow-v1.md` — current RandomX consensus candidate
- `spec/canonical-serialization.md` — NCE/1
- `spec/domain-separation.md` — hash/signature domains
- `spec/address-v1.md` — native addresses
- `spec/service-node-security-v1.md` — service-node consensus boundary
- `spec/proof-of-service-v1.md` — measurable service rewards
- `test-vectors/` — interoperability fixtures

---

**Handoff principle:** A new session should be able to read this document, inspect current GitHub state, and continue the existing engineering direction without relying on chat history.