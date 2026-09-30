# NIAHCIA Protocol Architecture V1

Status: **DESCRIPTIVE pre-alpha architecture map; individual incorporated specifications control normative behavior**

This document is the top-level map of the NIAHCIA protocol. It records the separation of responsibilities established across the project and points implementers toward specifications that lock individual wire formats, consensus objects, economic primitives, and state machines.

It is intentionally architecture-first. This document must not silently invent consensus rules while implementation and interoperability work remain in progress.

## 1. Core objective

NIAHCIA is a decentralized protocol in which independent resource classes perform distinct jobs:

- CPU proof-of-work establishes chain consensus and canonical ordering.
- Reth provides EVM execution and execution-state validation.
- GPU compute workers execute AI inference jobs and earn compute compensation independently of block mining.
- service/storage nodes distribute and preserve canonical model and protocol data and prove useful service.
- verification mechanisms determine whether off-chain compute results satisfy the job's declared verification policy.
- agents are protocol identities that can discover services, request work, hold permissions, use memory descriptors, and participate in protocol payments as those capabilities are enabled.

No compute worker, service/storage node, model provider, agent, website, scheduler, or bootstrap host is a second chain-consensus authority.

## 2. Separate authority from service

CPU PoW answers the consensus question: which valid chain has the greatest accepted cumulative work?

Execution answers: given an ordered execution payload, what state transition does the EVM produce?

AI compute answers: which worker can execute a declared model/runtime/profile job and produce a verifiable result commitment?

Storage/service answers: where can canonical content be retrieved, and did a registered node provide the service it claimed?

These roles may coexist on one physical machine, but their protocol authority does not merge. More GPU/storage capacity does not grant additional PoW consensus authority. Mining a block does not make an AI result correct merely because a miner included it.

## 3. Chain consensus

The NIAHCIA consensus daemon owns chain consensus. Current direction:

- standard RandomX PoW;
- approximately 30-second target block interval;
- highest valid cumulative-work fork choice;
- independent validation by every full node;
- chain P2P for blocks, headers, synchronization, and consensus data;
- authenticated local integration with the execution engine.

External miners and pools produce work; they are not trusted validators.

### Mining interoperability

Compatibility with stock common RandomX mining software is an explicit objective. In particular, a pool-facing interface should permit stock XMRig participation without maintaining a NIAHCIA-specific XMRig fork.

The exact XMRig-compatible PoW preimage/blob layout is **CANDIDATE / NOT LOCKED**. It requires a separately reviewed interoperability specification plus canonical node/pool/XMRig vectors before production use.

## 4. Execution

Reth owns EVM execution and execution state. NIAHCIA owns chain ordering and consensus.

```text
NIAHCIA consensus
       |
       | authenticated Engine API
       v
Reth execution engine
       |
       +-- EVM transaction execution
       +-- execution payload validation
       +-- execution state
       +-- Ethereum-compatible execution RPC
```

Consensus commits to the execution relationship defined by the applicable block protocol; nodes independently validate it. Reth conventions do not silently redefine NIAHCIA-native signed objects.

## 5. Identity and addresses

NIAHCIA uses native, network-aware human-facing addresses while retaining execution compatibility. Current V1 work establishes Bech32m network forms and typed/versioned address containers with a 20-byte execution-compatible payload.

Agent, worker, operator, service-node, model, capability, and other protocol-object identifiers remain distinct typed identities where their specifications require them. An operator's payment account is not automatically the identity of every resource the operator controls.

## 6. Native value and chain identity

Current V1 monetary representation uses:

- symbol `NIAH`;
- exactly 8 decimal places;
- `1 NIAH = 100,000,000 aniah`;
- integer-only native consensus arithmetic;
- checked arithmetic;
- explicit network and native chain identifiers;
- deterministic fee arithmetic.

Representation is separate from monetary policy. Decimal scale alone does not choose maximum supply, subsidy, emission curve, genesis allocation, tail emission, or reward split.

## 7. AI compute

AI execution is economically and operationally separate from PoW mining.

A compute worker is expected to possess an identity, advertise supported execution capabilities/profiles, become eligible without a permanent central scheduler, retrieve canonical inputs, verify declared hashes/profile requirements, execute work, stream permitted output, construct result commitments/evidence, and receive settlement only according to the applicable Job and VerificationPolicy rules.

The initial runtime direction uses vLLM, but runtime choice belongs in versioned execution profiles rather than permanent chain consensus. GPU ownership does not imply chain authority, and miners need not operate GPUs.

## 8. Job lifecycle

Architectural lifecycle:

```text
request
  -> canonicalize
  -> fund/escrow
  -> make eligible
  -> assign/select worker(s)
  -> execute
  -> commit result/evidence
  -> verify or challenge
  -> finalize
  -> settle
```

Detailed state names, timeouts, selection rules, retry behavior, verification thresholds, and payment transitions belong in versioned Job and VerificationPolicy specifications.

A scheduler must not become a permanent trusted coordinator. Selection inputs and eligibility rules should be reproducible from protocol-visible state or otherwise verifiable under the applicable protocol.

## 9. Verification

Execution and verification are separate responsibilities. A signed worker result is authenticated, not automatically correct.

VerificationPolicy identifies the evidence/agreement rules required for a class of job. The protocol should support multiple strategies over time instead of embedding one universal redundant-execution rule into every workload.

Disagreement resolves through explicit versioned states such as acceptance, additional verification, challenge, timeout, reassignment, failure, or another specified outcome—not silent coordinator discretion.

## 10. Service/storage

Service/storage nodes provide useful network services but are not a second consensus committee. Initial responsibilities include canonical manifest ingestion, content-addressed storage, chunk discovery/transfer, integrity verification, availability/service challenges, retrieval accounting, and signed proof-of-service evidence where required.

Proof-of-service demonstrates useful service under its own challenge rules. It does **not** choose the canonical chain.

Canonical content should be reconstructable from independently verifiable manifests/chunks rather than depending on one operator's server.

## 11. P2P protocol families

NIAHCIA distinguishes three logical families:

- **Chain P2P** — headers, blocks, synchronization, consensus state, and transaction propagation where applicable.
- **AI P2P** — worker discovery, jobs, assignments, input retrieval, output streaming, result commitments, and verification traffic.
- **Storage P2P** — manifest/chunk discovery, content transfer, availability challenges, and service evidence.

Implementations may reuse secure identity/transport primitives without collapsing the authority or semantics of these protocol families.

## 12. Agents

An Agent is a versioned protocol identity, not merely a prompt or a process running on one server.

The architecture reserves explicit concepts for `Agent`, `AgentVersion`, `Model`, `ExecutionProfile`, `Capability`, `MemoryDescriptor`, `PaymentPlan`, `Job`, `VerificationPolicy`, and `ResultCommitment`.

Creator/operator authority, upgrades, delegation, revocation, tools, agent-to-agent payments, discovery, reputation, and memory semantics require explicit versioned rules and must not depend on one website as gatekeeper.

## 13. Economic separation

Economically useful roles are not interchangeable:

- miners earn for chain security/block production under monetary policy;
- compute workers earn for accepted AI compute;
- service/storage nodes may earn for accepted useful service;
- verifiers may earn where the applicable VerificationPolicy provides it;
- users/agents pay according to transaction/job/service rules.

Reward in one subsystem does not grant authority in another. Native settlement uses canonical NIAH/aniah representation unless a future versioned mechanism explicitly says otherwise.

## 14. Security boundaries

Participants may fail, disconnect, lie, withhold service, submit stale data, or attempt to game rewards. Therefore:

- full nodes independently validate PoW and consensus;
- Reth independently validates execution within the execution boundary;
- AI results require evidence specified by their verification policy;
- service rewards require defined proof of useful service;
- signatures authenticate claims but do not make claims true;
- timeouts/reassignment prevent one worker from permanently blocking a job;
- no bootstrap node, website, model host, scheduler, miner, worker, or service node should be indispensable after network discovery/canonical-state acquisition.

Botnet resistance is not solved merely by choosing CPU-friendly RandomX. Devnet/testnet must measure mining economics, pool concentration, difficulty behavior, work distribution, telemetry, and attacks before production assumptions are made.

## 15. Versioning and interoperability

Consensus-critical encodings and state transitions require canonical byte-for-byte or state-transition vectors before production interoperability is considered locked.

Once a V1 object is declared interoperable, implementations must not silently reinterpret it. Incompatible changes require a new object/profile version or explicitly activated transition.

Project status terminology:

- **LOCKED / normative** — interoperability behavior implementations must follow for that version.
- **CANDIDATE** — proposed behavior awaiting review/vectors/testing/activation.
- **DESCRIPTIVE** — architecture/explanation, not independent consensus law.
- **IMPLEMENTATION DETAIL** — replaceable code behavior.

## 16. Pre-alpha acceptance objective

The smallest complete network should demonstrate independent RandomX full/mining nodes with cumulative-work fork choice and Reth-backed execution; independent GPU workers with decentralized eligibility/assignment, execution profiles, result commitments and verification; independent service nodes with canonical content retrieval and proof of useful service; and the end-to-end flow `submit job -> execute -> verify -> finalize -> settle`.

The network must continue appropriate progress when individual miners, compute workers, service nodes, or the original bootstrap/developer host disappear.

## 17. Source-of-truth rule

This repository (`niahcia/niahcia-protocol`) is authoritative for protocol meaning.

The `niahcia/niahcia` repository is the Rust reference implementation and contains implementation-facing documentation. If implementation and a normative specification disagree, the disagreement must be resolved explicitly; implementation behavior does not silently rewrite the protocol.

Protocol changes are complete only when affected specifications and test vectors are synchronized with implementation changes.

## 18. Not locked by this map

This architecture map does not itself lock:

- final XMRig-compatible PoW preimage layout;
- production genesis parameters;
- final issuance/reward split except where separately specified;
- one universal AI verification algorithm;
- production slashing parameters;
- one mandatory model/runtime forever;
- distributed training semantics;
- private inference or zkML;
- complete autonomous-agent permission/memory/payment state machines.

Those require their own versioned specifications and interoperability tests.
