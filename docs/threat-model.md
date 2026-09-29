# Threat Model

This document begins the NIAHCIA threat model. It is intentionally conservative.

## Consensus threats

- majority PoW attacks
- selfish mining
- timestamp manipulation
- difficulty manipulation bugs
- invalid-state block propagation
- chain reorganization attacks

Mitigation work belongs in the consensus specification and must remain independent from AI-layer security.

## Compute threats

- worker returns fabricated output without running the requested model
- worker substitutes a different model or tokenizer
- worker lies about runtime or execution profile
- worker copies another worker's revealed result
- worker accepts jobs and intentionally times out
- Sybil operators register many worker identities
- colluding executor and verifier identities approve invalid work
- hardware/runtime numerical differences cause honest disagreement

Protocol hooks include:

- content-addressed model identity
- execution profiles
- commit/reveal for redundant verification
- operator identities
- worker bonds
- random audits
- optimistic challenges
- reproducible execution work
- future cryptographic proof systems

## Service-node threats

- claims to store data but discards it
- serves corrupted model chunks
- disappears after accepting storage payment
- withholds popular models
- attempts eclipse/routing attacks

Required defenses include:

- content hashes
- chunk-level verification
- replication
- periodic availability challenges
- independent peer discovery
- service reputation evidence

### Service-node capture and false observations

A service-node cartel may attempt to publish false reorg warnings, suppress archival data, bias relay paths, or present a coordinated false view of the chain.

Defenses include:

- no service-node vote in fork choice,
- independent PoW/header verification by clients,
- operator-diverse observation sources,
- signed observation records for accountability,
- competing-provider retrieval,
- retention of stale branches and reorg evidence,
- treating service-node disagreement as telemetry rather than consensus.

## Agent threats

- malicious system instructions
- excessive permissions
- unauthorized spending
- recursive agent-call loops
- malicious tool execution
- silent model or prompt substitution
- creator changes behavior after users establish trust

Required architectural safeguards include:

- immutable agent versions
- capability-based permissions
- explicit spending limits
- call-depth and child-budget limits
- model/config hashes
- sandboxed tool execution
- isolated signing components
- transparent governance/controller policy

## Frontend threats

The official website is not trusted as protocol authority.

A compromised frontend may misrepresent data or construct malicious transactions, but it must not be able to:

- rewrite chain state
- substitute an agent version without the user being able to detect the on-chain identity
- become the only path to workers or service nodes
- custody protocol-required user funds

## Privacy

Prototype 0 must assume selected compute workers can read job payloads. Private inference is a future capability and must not be implied before an appropriate cryptographic or trusted-execution design exists.


## Botnet and stolen-compute threat

CPU-accessible proof of work has a specific operational threat: an attacker may aggregate large amounts of unauthorized CPU capacity from compromised machines and direct it at NIAHCIA.

Consensus cannot reliably distinguish an authorized miner from a compromised host. NIAHCIA therefore MUST NOT depend on IP allowlists, device identity, hardware attestation, developer-operated admission servers, or miner registration to decide whether PoW is valid.

Botnet-related risks include:

- sudden temporary hashrate spikes,
- abrupt hashrate disappearance,
- majority-hash censorship,
- private-chain/reorganization attacks,
- selfish mining,
- timestamp manipulation when the attacker wins many blocks,
- concentration through one pool or command-and-control operator.

Protocol defenses are limited but important:

- cumulative-work fork choice,
- a DAA that remains stable under abrupt entry/exit of hashrate,
- timestamp rules resistant to DAA manipulation,
- no implicit mainnet emergency minimum-difficulty reset,
- independent peer discovery and anti-eclipse work,
- miner/pool decentralization,
- clear chain-reorg and hashrate telemetry,
- no consensus privilege for known miners or pools.

RandomX raises the memory footprint of each mining process and favors general-purpose CPUs, but it is not a botnet-prevention mechanism. A sufficiently large botnet is still real PoW hashrate.

If an attacker obtains sustained majority hashpower, no ordinary Nakamoto-style PoW rule can guarantee protection from censorship or reorganization. NIAHCIA should make such attacks expensive, observable, and difficult to amplify, not pretend they are impossible.
