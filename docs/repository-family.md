# NIAHCIA Repository and Product Architecture

NIAHCIA uses separate repositories for protocol, chain, mining, AI compute, exploration, and user-facing applications. The separation is intentional: each repository maps to a distinct protocol or product responsibility.

## Canonical repository family

```text
niahcia
niahcia-protocol
niahcia-miner
niahcia-compute
niahcia-explorer
niahcia-web
niahcia.github.io
.github
```

## `niahcia`

Reference blockchain/node implementation.

Primary responsibilities:

- CPU PoW consensus
- RandomX
- Reth/EVM integration
- chain P2P and synchronization
- block production and validation
- smart-contract execution environment
- node orchestration

## `niahcia-protocol`

Protocol source of truth.

Primary responsibilities:

- architecture
- canonical object specifications
- serialization/hashing standards
- threat model
- economics
- NIAHCIA Improvement Proposals
- Prototype profiles

## `niahcia-miner`

Dedicated CPU mining client.

Primary responsibilities:

- RandomX CPU mining
- solo mining
- pool mining
- CPU tuning/autotuning
- failover
- telemetry
- mining console/UI
- reproducible release artifacts

The miner secures the blockchain. It is not an AI compute worker.

## `niahcia-compute`

Decentralized AI compute client.

Primary responsibilities:

- ComputeWorker identity
- hardware/runtime capability discovery
- vLLM and future runtime adapters
- execution-profile support
- P2P job discovery and assignment
- streaming inference
- result commitments
- verification/audit work
- compute telemetry

A host may run both miner and compute software, but they remain distinct services and economic roles.

## `niahcia-explorer`

Unified chain + AI network explorer.

### Chain

- blocks
- transactions
- accounts/addresses
- contracts
- gas
- difficulty
- hashrate
- mining distribution
- reorg indicators

### AI

- jobs
- verification
- models
- execution profiles
- workers
- operators

### Agents

- identities
- immutable versions
- controllers
- permissions
- models
- usage
- jobs

### Service network

- service nodes
- stored replicas
- availability
- retrieval activity

The explorer is observational infrastructure only. Its database must never become protocol authority.

## `niahcia-web`

Official main application.

Primary responsibilities:

- Ask an Agent
- browse/search agents
- wallet connection
- funded AI sessions
- account/job history
- network dashboard
- agent/model publishing
- developer portal
- worker/service-node onboarding

The official website is the primary user experience, but it is not required for protocol operation.

## `niahcia.github.io`

Static GitHub Pages site.

Primary responsibilities:

- project overview
- architecture overview
- links to repositories
- protocol/documentation links
- development status
- downloads/releases
- testnet/mainnet links

The GitHub Pages site should remain lightweight and static.

## `.github`

Shared GitHub presentation/community repository.

Recommended contents:

- organization/profile README
- CONTRIBUTING
- SECURITY
- CODE_OF_CONDUCT
- issue templates
- pull-request template
- shared CI/release policies where appropriate

## Design boundaries

```text
CPU mining != AI compute
Explorer != protocol authority
Official website != protocol
GitHub Pages != main application
Protocol spec != reference implementation
```

These boundaries should remain even if a future installer can launch multiple components together.

## Recommended next repositories

Create in this order:

1. `niahcia-miner`
2. `niahcia-compute`
3. `niahcia-explorer`
4. `niahcia-web`
5. `niahcia.github.io`
6. `.github`

Each should start with a README and architecture scope before substantial implementation.
