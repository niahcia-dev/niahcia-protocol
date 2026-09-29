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
