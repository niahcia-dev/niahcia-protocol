# NIAHCIA Protocol Mirror

NIAHCIA is a permissionless CPU-PoW blockchain with first-class native smart contracts, decentralized AI compute, wallet-controlled Agents, and optional service/storage networks.

During pre-alpha development, `niahcia/niahcia` is the canonical working repository for the reference node plus consolidated protocol/spec/test-vector material. This repository is retained as a synchronized protocol mirror and must not contradict the canonical working repository.

## Core architecture

- CPU Proof-of-Work is the sole chain-consensus authority.
- Native value transfer and smart-contract execution are base-chain capabilities.
- `ContractCall` and `ContractCreate` are already reserved native transaction actions; their deterministic native runtime remains inactive until separately specified, vectored, tested, and explicitly activated.
- AI inference is off-chain service execution and never part of consensus execution.
- Compute workers, service/storage nodes, Agents, websites, and schedulers receive no fork-choice or finality authority.
- Wallet/client-local encrypted chat history and Agent memory are the first ordinary AI persistence default.
- Decentralized storage is optional and may be added when needed for remote durability, replication, retrieval, or long-lived autonomous state.

## Smart contracts

Smart contracts are a core NIAHCIA requirement, not an optional future feature.

NIAHCIA's current direction is a deterministic native contract runtime owned by the protocol/reference node rather than reintroducing Reth/EVM as the base execution engine. The exact VM/instruction technology, storage model, gas schedule, call/create/revert behavior, receipts, persistence rules, and activation boundary remain review work.

See `spec/native-contract-runtime-v1.md`.

## Repository synchronization rule

A protocol-visible change is not complete until, where applicable:

1. the canonical specification/status is updated in `niahcia/niahcia`;
2. interoperability vectors are updated for consensus/wire changes;
3. implementation-facing documentation is synchronized;
4. this retained mirror is synchronized where it carries the same material;
5. superseded behavior is removed or clearly marked historical.

This repository is not permitted to preserve an older Reth/EVM, fixed-2-of-3, storage-required, or other superseded architecture as though it were current.
