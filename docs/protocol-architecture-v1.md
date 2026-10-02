# NIAHCIA Protocol Architecture V1

Status: **DESCRIPTIVE pre-alpha architecture map; individual incorporated specifications control normative behavior**

This document is the top-level map of the NIAHCIA protocol. It records the separation of responsibilities established across the project and points implementers toward specifications that lock individual wire formats, consensus objects, economic primitives, and state machines.

It is intentionally architecture-first. This document must not silently invent consensus rules while implementation and interoperability work remain in progress.

## 1. Core objective

NIAHCIA is a decentralized protocol for owning, requesting, executing, verifying, and paying for machine intelligence.

Its minimum operating stack is deliberately small:

- CPU proof-of-work establishes chain consensus and canonical ordering.
- the native NIAHCIA execution/state layer validates transactions, balances, commitments, authorization, payments, and settlement.
- wallets/clients create requests, hold user authority, retain private local state, and communicate with compute workers.
- GPU/accelerator compute workers execute AI inference jobs and earn compute compensation independently of block mining.
- verification mechanisms determine whether off-chain compute results satisfy the job's declared verification policy.

Optional service networks, including decentralized storage, may provide durability, replication, retrieval, relay, or specialized verification. They are not prerequisites for ordinary AI inference or for base-chain correctness.

No compute worker, service/storage node, model provider, agent, website, scheduler, or bootstrap host is a second chain-consensus authority.

## 2. Separate authority from service

CPU PoW answers the consensus question: which valid chain has the greatest accepted cumulative work?

Native execution answers: given an ordered native transaction set, what deterministic NIAHCIA state transition results?

AI compute answers: which worker can execute a declared model/runtime/profile job and produce a verifiable result commitment?

Optional storage/service answers: when a user or application requests remote durability or another service, where can committed content be retrieved and did a provider perform the service it claimed?

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

## 4. Native execution

NIAHCIA uses its own native execution and state transition layer.

```text
NIAHCIA CPU-PoW consensus
       |
       v
native transaction ordering
       |
       v
deterministic native execution
       |
       +-- account state
       +-- authorization
       +-- transaction commitments
       +-- execution commitments
       +-- payments and settlement
```

Every full node independently validates the native transition. External execution engines are not required for the base protocol to remain valid or usable.

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

## 10. Optional service/storage networks

Decentralized storage is an optional service, not part of the minimum NIAHCIA AI execution path.

Ordinary V1 chat/inference may operate as:

```text
wallet/client
  -> encrypted job delivery
  -> compute worker
  -> encrypted result return
  -> wallet-local encrypted history/memory
```

No storage node is required for that flow. Compute workers may also keep supported model weights locally; the protocol need not provide model storage merely to schedule inference.

Users and applications may later request decentralized storage for cross-device persistence, replicated encrypted memory, large artifacts, model distribution, backups, or long-lived autonomous agents. When used, service/storage nodes may provide content-addressed storage, chunk discovery/transfer, integrity verification, availability/service challenges, retrieval accounting, and signed proof-of-service evidence.

Proof-of-service demonstrates useful service under its own challenge rules. It does **not** choose the canonical chain and storage availability must never become a prerequisite for base-chain validity.

## 11. P2P protocol families

NIAHCIA distinguishes three logical families:

- **Chain P2P** — headers, blocks, synchronization, consensus state, and transaction propagation where applicable.
- **AI P2P** — worker discovery, jobs, assignments, input retrieval, output streaming, result commitments, and verification traffic.
- **Optional Storage P2P** — when requested, manifest/chunk discovery, content transfer, availability challenges, and service evidence.

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

## 13.1 Compute micropayments

Ordinary chat prompts should not require one base-chain transaction each.

The preferred V1 payment path is:

```text
wallet funding account
  -> simple ComputeChannelV1
      -> bounded PaymentAuthorizationV1
          -> many Jobs
              -> signed usage receipts
                  -> eventual native settlement
```

The first channel design is deliberately narrow: direct worker payment, no routing, no credit, no generalized state-channel scripting, a hard value ceiling, monotonic cumulative receipts, fixed expiry, and simple cooperative/expiry settlement.

This mechanism reduces chain load and prompt-level economic linkage while preserving hard spending limits. It does not claim complete anonymity.

## 14. Security boundaries

Participants may fail, disconnect, lie, withhold service, submit stale data, or attempt to game rewards. Therefore:

- full nodes independently validate PoW and consensus;
- full nodes independently validate native execution and state transitions;
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

The smallest meaningful AI network should demonstrate independent CPU-PoW full/mining nodes with cumulative-work fork choice and native execution; at least two independently operated compute participants with decentralized eligibility/assignment, execution profiles, result commitments and verification; wallet/client-local encrypted chat memory; and the end-to-end flow `submit job -> execute -> verify -> return result -> settle`.

Decentralized storage is not required for this first milestone.

The base blockchain must remain secure, valid, and usable even if every AI worker and every optional service/storage provider disappears. AI execution naturally pauses when no eligible compute worker exists, but chain consensus and ordinary native value transfer must continue independently.

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
