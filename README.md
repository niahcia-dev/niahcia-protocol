# NIAHCIA Protocol

NIAHCIA is a permissionless decentralized blockchain and AI-agent network combining CPU-secured consensus, EVM smart contracts, decentralized compute, distributed storage, and persistent AI agents.

The protocol is designed so that no central AI provider, scheduler, model host, storage server, or website is required for the network to continue functioning.

## Repository authority

This repository is the **normative source of truth for the NIAHCIA protocol**.

The implementation repository, `niahcia/niahcia`, contains the Rust reference node, implementation notes, build/run instructions, devnet operations, RPC documentation, tests, and development milestones. Implementation code does not silently override a normative protocol specification.

When protocol behavior changes, the corresponding specification and interoperability vectors in this repository must be updated alongside the implementation.

- `docs/` — architecture, goals, doctrine, economics, threat model, Prototype 0 and supporting design analysis
- `spec/` — normative/candidate protocol definitions and canonical encodings
- `nips/` — NIAHCIA Improvement Proposals for proposed protocol evolution
- `test-vectors/` — byte-for-byte and state-transition interoperability vectors shared by independent implementations
- `tools/` — protocol-oriented validation/generation tools where appropriate

Specifications should clearly identify their status. The project uses these meanings:

- **LOCKED / normative** — interoperability behavior implementations must follow for that protocol version.
- **CANDIDATE** — proposed behavior still subject to review, vectors, testing, or activation decisions.
- **DESCRIPTIVE** — architecture/explanation that does not independently create consensus rules.
- **IMPLEMENTATION DETAIL** — replaceable behavior of a particular implementation.

## Core doctrine

- **The blockchain is sovereign.** AI, storage, websites, and workers may fail independently without stopping the chain.
- **Consensus and AI remain separate.** CPU miners secure the network; compute workers execute AI. Neither role is mandatory for the other.
- **Agents belong to the network, not servers.** An agent is a versioned network identity that can be executed by many independent hosts.
- **No mandatory central service.** No scheduler, API server, model repository, database, or frontend may become a protocol dependency.
- **Every participant is paid for the service they provide.** CPU miners earn for security, compute workers for AI execution, and service nodes for storage and network services.
- **Smart contracts are first-class.** NIAHCIA targets EVM compatibility and Solidity tooling.
- **Fast AI UX matters.** Inference and token streaming happen over the AI P2P network; blockchain settlement happens asynchronously.
- **Protocol v1 defines the future-facing architecture.** Prototype 0 implements only the minimum end-to-end slice required to prove the design.

## Initial architecture

```text
                         NIAHCIA

                    CPU PoW blockchain
                           |
                          EVM
                           |
        +------------------+------------------+
        |                  |                  |
   Compute network     Service network     AI agents
        |                  |                  |
   vLLM / future       model storage       identity
   runtimes            memory/storage      tools
   GPU/accelerators    routing/services    permissions
        |                  |                  |
        +------------------+------------------+
                           |
                      native economy
```

## Current architecture direction

- CPU-friendly PoW: standard RandomX
- Target block interval: approximately 30 seconds
- Fork choice: highest valid cumulative work
- EVM execution: Reth
- AI runtime direction: vLLM through versioned execution profiles
- Compute workers are economically and operationally separate from miners
- Service/storage nodes provide useful service but are not a second consensus authority
- Large AI/model payloads are content-addressed/off-chain; identities, commitments, verification state and settlement are protocol/on-chain concerns where specified
- Stock RandomX miner compatibility, especially stock XMRig through pool-facing interoperability, is an explicit design objective; the exact compatible PoW preimage is not yet locked

## Status

Pre-alpha protocol and devnet development. Some V1 primitives are already locked, while other interfaces and parameters remain candidates. A document's own status and the normative specifications in `spec/` control; this README is descriptive.

## Consensus foundation

Concrete chain-consensus specifications are tracked under `spec/`, including the NIAHCIA-owned PoW header and transaction commitments.

The reference implementation may temporarily contain development behavior ahead of a formal spec, but such behavior is not automatically promoted to protocol law. Before production interoperability, consensus-critical encodings and state transitions require canonical vectors and explicit specification status.

## Service-node security boundary

Service/storage nodes may provide archive, snapshot, relay, reorg-watch, model-storage, agent-storage, and related services.

They strengthen network survivability and observability but **never vote on the canonical chain**. Canonical chain selection remains RandomX PoW plus cumulative work.

See `spec/service-node-security-v1.md` and the architecture documentation in this repository.

## Documentation synchronization rule

A protocol change is not complete until its documentation is synchronized.

For consensus-critical or interoperability-critical changes, completion means, as applicable:

1. update the normative/candidate specification here;
2. update or add canonical test vectors;
3. update the reference implementation;
4. update implementation-facing documentation in `niahcia/niahcia`;
5. identify superseded behavior rather than leaving contradictory rules in place.

This separation is intentional: **`niahcia-protocol` defines what NIAHCIA means; `niahcia` implements it.**
