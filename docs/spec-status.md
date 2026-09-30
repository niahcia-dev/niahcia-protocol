# NIAHCIA Specification Status Audit

Last reviewed: 2026-09-30

This is a living audit of protocol documents against current design decisions, reference implementation evidence, and interoperability requirements. It does not itself promote a candidate to normative consensus.

Status vocabulary:

- **LOCKED** — normative behavior for the stated protocol version.
- **CANDIDATE** — intended/proposed behavior still awaiting review, vectors, testing, activation, or another explicit freeze criterion.
- **DESCRIPTIVE** — architecture or rationale; not independent consensus law.
- **IMPLEMENTED (DEV)** — present in the reference implementation, but implementation alone does not make it normative.
- **VECTORED** — canonical machine-readable interoperability vectors exist.
- **REVIEW REQUIRED** — a known open question, conflict, or new interoperability requirement prevents freezing.
- **SUPERSEDED** — retained only for historical/rationale purposes and not the current protocol direction.

## Consensus/mining audit

| Area | Protocol document | Protocol status | Implementation/vector evidence | Audit finding |
| --- | --- | --- | --- | --- |
| Block header | `spec/block-header-v1.md` | CANDIDATE | Development reference node uses the 164-byte V1 shape | Header structure is still a candidate. Do not call it frozen consensus. |
| PoW preimage | `spec/block-header-v1.md` | CANDIDATE | Development node currently hashes the canonical 164-byte header | **REVIEW REQUIRED:** stock-XMRig interoperability is now an explicit objective. The current rule `PoW preimage = canonical header` plus 64-bit nonce/64-bit extra nonce must not be frozen until a stock-XMRig-compatible design is proven with vectors. |
| RandomX | architecture + implementation | CANDIDATE direction | Reference node uses standard `randomx-rs` behavior; standalone reference miner work reproduced the node vector | Preserve standard RandomX. Do not create a NIAHCIA-specific RandomX VM/hash variant merely for transport compatibility. |
| Difficulty, normalized window | `spec/difficulty-adjustment-v1.md` | SUPERSEDED candidate | Simulation document records its earlier role | The document itself predates the later ASERT direction. Keep for rationale/history, but it is not the leading Protocol V1 controller. |
| Difficulty, ASERT | `spec/difficulty-asert-v1.md` | CANDIDATE | Spec states development implementation and `test-vectors/difficulty-asert-v1.json` exist | Leading candidate, **not frozen**. Timestamp-adversary finding explicitly blocks freeze pending hardening/analysis. |
| Target interval | ASERT/network docs | CANDIDATE parameter | Current candidate uses 30 seconds | Treat 30 seconds as current V1 direction until concrete network parameters are frozen. |
| Fork choice | difficulty/architecture docs | CANDIDATE architecture | Greatest valid cumulative work is consistently specified | Direction is stable, but exact work arithmetic remains consensus-critical and should remain tied to vectors/implementation tests. |
| Network parameters | `spec/network-parameters-v1.md` | CANDIDATE framework | Devnet values exist in development implementation | Framework is sound; production genesis, pow limit, seed/epoch parameters, activation heights and concrete network definitions remain to be frozen. |

## Immediate consensus blockers before freeze

1. Resolve the stock-XMRig mining-preimage/nonce-layout question without modifying RandomX itself.
2. Produce a node + pool adapter + stock XMRig canonical RandomX interoperability vector for the chosen PoW preimage.
3. Resolve the ASERT/timestamp-adversary issue and reproduce the final arithmetic independently.
4. Freeze concrete per-network PoW limits, genesis/anchor behavior, RandomX seed/epoch rules and activation parameters.
5. Ensure the reference node documentation mirrors each frozen decision.

## Documentation synchronization

For every protocol-affecting code change:

1. update this repository's affected specification/status;
2. update canonical vectors where consensus/wire behavior changes;
3. update the reference implementation;
4. update the corresponding implementation-facing documentation in `niahcia/niahcia`;
5. explicitly identify superseded behavior.

The audit will be expanded through value/fees, addresses/chain identity, transactions/serialization, service/storage, compute/jobs/verification, and agents/capabilities.
