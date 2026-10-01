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

## Service-node and storage threats

Storage is an availability and service system, not a second consensus system. Storage evidence may eventually affect storage/service settlement, but it MUST NOT grant fork-choice, finality, veto, or block-production authority.

Baseline threats include:

- claims to store data but discards it;
- serves corrupted model/data chunks;
- disappears after accepting storage payment;
- withholds popular models or agent state;
- attempts eclipse/routing attacks;
- stores data only immediately before predictable challenges;
- fabricates provider identities to appear replicated;
- places nominal replicas in the same physical/operator failure domain;
- fabricates retrieval traffic to earn service rewards;
- colludes with requesters or other providers to manufacture paid traffic;
- intentionally drops replicas to create profitable repair work;
- withholds surviving chunks during recovery to extort users or raise repair prices;
- races honest repair providers and claims duplicate rewards;
- replays old challenges/responses or service evidence;
- injects corrupt chunks during reconstruction;
- claims inflated object sizes or bandwidth usage;
- keeps encryption keys or plaintext beyond authorized scope;
- uses possession of agent memory/model data to claim governance/control rights.

Required defenses include content hashes, chunk-level verification, replication, unpredictable availability challenges, independent peer discovery, explicit service evidence, bounded replay windows/nonces, exact object/profile commitments, and strict separation between storage authority and agent/consensus authority.

### Sybil replicas and correlated failure domains

A target of five providers is meaningless if all five identities are one operator, one machine, one rack, or one hosting account.

NIAHCIA must therefore distinguish **provider identity count** from **independent durability**. Production storage economics MUST NOT assume that unique public keys prove independent failure domains.

Potential evidence may eventually include operator identity, network/ASN diversity, declared failure-domain metadata, challenge behavior, long-term correlated uptime, or other independently checkable signals. None of these is currently sufficient alone and no production independence score is locked.

The safe pre-alpha rule is conservative: provider counts are observational and must not be advertised as guaranteed physical independence.

### Challenge predictability and just-in-time storage

If challenges are predictable far enough in advance, a provider can discard committed data and reacquire it only before challenge time.

Challenge designs should therefore provide enough unpredictability that repeatedly fetching missing data on demand is economically or temporally impractical. Responses should bind the provider, commitment, challenge nonce/context, requested range/proof, and applicable epoch/window.

Challenge randomness must not depend on a storage provider's unilateral choice. Exact challenge derivation belongs in the applicable locked storage-challenge specification and vectors.

### Replay and evidence reuse

A valid response to one challenge must not automatically satisfy another challenge or earn repeated payment.

Compensable evidence needs unique context and replay protection. Settlement/accounting must prevent the same evidence from being paid more than once even across retries, reorg handling, or competing report paths.

### Fake retrieval and bandwidth farming

Raw provider-reported byte counts are not trustworthy. Two colluding identities can repeatedly send the same bytes to each other and claim useful retrieval service.

Therefore NIAHCIA MUST NOT pay production rewards solely from self-reported bandwidth, HTTP counters, or provider/requester signatures without additional anti-collusion design.

Early storage rewards should favor evidence with stronger verification properties such as unpredictable possession challenges and explicitly authorized retrieval obligations. Useful-bandwidth rewards remain a research item until traffic fabrication is economically addressed.

### Repair farming and deliberate degradation

A provider or cartel could intentionally remove replicas, push an agreement into `DEGRADED`/`AT_RISK`, then earn elevated repair compensation.

Recovery economics must avoid making destruction more profitable than continuous honest storage. Candidate defenses include:

- no repair premium for providers responsible for recent loss;
- delayed eligibility for replacement rewards;
- service history/bond consequences for broken obligations;
- bounded total repair compensation;
- evidence linking previous commitments to failures;
- no duplicate payment for reconstruction and ordinary possession of the same interval.

Exact economics are not locked.

### Withholding and extortion

A provider possessing rare surviving chunks may refuse retrieval or demand out-of-protocol payment.

The primary defense is proactive redundancy: recovery should begin while the object is `DEGRADED`, not after only one copy remains. Storage health should make declining redundancy observable early enough for independent providers to repair it.

No provider should possess a protocol veto over reconstruction when other valid committed content is available.

### Corrupt reconstruction

Recovery providers must verify every retrieved chunk/proof against the exact committed object/profile before accepting it. Reconstruction must reproduce the exact `object_root`; semantically equivalent models/files are not substitutes.

A corrupt peer should cause rejection of its bytes, not mutation of the expected commitment.

### Encrypted agent memory

Storage nodes should generally be able to preserve encrypted agent memory without possessing decryption authority.

Storage/recovery of ciphertext MUST NOT imply:

- agent controller authority;
- capability delegation;
- treasury/payment authority;
- succession rights;
- permission to alter AgentVersion/AgentManifest state;
- permission to publish plaintext.

A recovery provider reconstructs committed ciphertext/content. Key recovery and authorization are separate protocol/security problems.

A critical unresolved threat is **key loss**: perfect ciphertext durability is useless if all authorized decryption capability disappears. Future agent privacy/succession design must explicitly address whether keys are non-recoverable, threshold recoverable, succession-controlled, hardware-bound, or governed by another versioned policy. NIAHCIA must not silently escrow user/agent keys in storage nodes.

### Object poisoning and namespace confusion

Attackers may publish objects with familiar filenames, model names, agent labels, or metadata while serving different bytes.

Execution and recovery must bind exact content-addressed roots and versioned manifests. Human-readable names are discovery metadata, not integrity authority.

### Oversized and resource-exhaustion agreements

Attackers may advertise huge objects, excessive replication targets, or pathological chunk/manifests to exhaust provider bandwidth, memory, disk, or verification time.

Providers need local admission/resource limits. Protocol objects need bounded field sizes/counts where consensus/interoperability requires them. Accepting a StorageAgreement must remain explicit; discovery of an agreement is not an obligation for every node to store it.

### Storage-health manipulation

Attackers may try to force false `AT_RISK` or `HEALTHY` states by suppressing evidence, flooding identities, delaying reports, or selectively answering observers.

Until deterministic evidence windows and eligibility rules are locked, `StorageHealthV1` must remain non-authoritative operational telemetry and MUST NOT create consensus/economic state transitions.

If health later affects settlement, the exact evidence set, window boundaries, threshold arithmetic, reorg handling, and state transitions require canonical vectors and adversarial tests.

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

Storage confidentiality is separate: providers may preserve ciphertext without being able to decrypt it. Durable ciphertext does not solve key-management, access-control, or private-compute requirements by itself.

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
