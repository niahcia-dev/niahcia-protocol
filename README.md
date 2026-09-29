# NIAHCIA Protocol

**AI CHAIN — reversed.**

NIAHCIA is a permissionless decentralized blockchain and AI-agent network combining CPU-secured consensus, EVM smart contracts, decentralized compute, distributed storage, and persistent AI agents.

The protocol is designed so that no central AI provider, scheduler, model host, storage server, or website is required for the network to continue functioning.

## Core doctrine

- **The blockchain is sovereign.** AI, storage, websites, and workers may fail independently without stopping the chain.
- **Consensus and AI remain separate.** CPU miners secure the network; compute workers execute AI. Neither role is mandatory for the other.
- **Agents belong to the network, not servers.** An agent is a versioned network identity that can be executed by many independent hosts.
- **No mandatory central service.** No scheduler, API server, model repository, database, or frontend may become a protocol dependency.
- **Every participant is paid for the service they provide.** CPU miners earn for security, compute workers for AI execution, and service nodes for storage and network services.
- **Smart contracts are first-class.** NIAHCIA targets EVM compatibility and Solidity tooling.
- **Fast AI UX matters.** Inference and token streaming happen over the AI P2P network; blockchain settlement happens asynchronously.
- **Protocol v1 defines the future-facing architecture.** Prototype 0 implements only the minimum end-to-end slice required to prove the design.

## Repository purpose

This repository is the source of truth for the NIAHCIA architecture and protocol specifications.

- `docs/` — architecture, goals, doctrine, economics, threat model, Prototype 0
- `spec/` — canonical protocol object definitions
- `nips/` — NIAHCIA Improvement Proposals

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

## Prototype 0 working profile

- CPU-friendly PoW: RandomX
- Target block interval: ~30 seconds
- EVM execution: Reth
- AI runtime: vLLM
- Canonical workload: pinned Qwen3-class ~8B text model
- Initial hardware profile: NVIDIA Ampere
- Initial verification: deterministic redundant 2-of-3, designed to be replaceable by optimistic verification
- Service nodes: model replication and retrieval
- Large payloads: off-chain, content-addressed
- On-chain: identities, registries, commitments, escrow, verification state, and settlement

## Status

Early architecture and protocol design. Interfaces and parameters are expected to evolve before any production network launch.
