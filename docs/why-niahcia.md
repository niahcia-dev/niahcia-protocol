# Why NIAHCIA

Status: **DESCRIPTIVE / pre-alpha project rationale**

This document explains the architectural problem NIAHCIA is trying to solve and why its design differs from simply attaching AI workloads to a blockchain. It is not a claim that every described capability is already implemented or production-ready.

NIAHCIA is currently pre-alpha. Where this document says the network *is designed to*, *should*, or *will*, it describes protocol direction rather than demonstrated production capability.

## The central idea

NIAHCIA is being designed as a decentralized execution and economic protocol for autonomous intelligence.

The goal is not merely to create a cryptocurrency that rewards AI compute, nor merely a marketplace where users rent GPUs. The goal is to provide a decentralized substrate in which chain security, execution, AI compute, storage, verification, agents, capabilities, memory, and settlement can cooperate without collapsing into one trusted service.

The defining architectural choice is **separation of responsibilities**.

```text
                         NIAHCIA
                            |
             +--------------+--------------+
             |              |              |
          CPU PoW        AI COMPUTE      STORAGE /
          CONSENSUS       WORKERS         SERVICE
             |              |              |
        chain security    inference,      models,
        and ordering      execution       memory,
             |            and jobs        archival
             |              |              |
             +--------------+--------------+
                            |
                       EVM / CONTRACTS
                            |
                          AGENTS
```

These roles can interact economically, but they do not inherit one another's authority.

## 1. AI compute is not consensus

NIAHCIA deliberately does not pretend that securing a blockchain and executing useful AI workloads are the same problem.

CPU proof-of-work has one responsibility: make canonical chain history expensive to attack or reorganize and give independent nodes an objective cumulative-work fork-choice rule.

GPU/accelerator compute has another responsibility: execute useful AI workloads under declared models, execution profiles, job rules, and verification policies.

A miner does not need a GPU or AI runtime to secure the chain.

A GPU operator does not acquire chain-consensus authority merely by owning substantial compute.

This separation allows both systems to evolve independently. A new model architecture, inference runtime, accelerator, or verification method should not require redesigning proof-of-work consensus.

## 2. Useful service does not equal consensus authority

The same rule applies to storage and service nodes.

NIAHCIA service/storage nodes are intended to preserve and distribute useful network resources: models, manifests, memory objects, snapshots, archival material, relay data, availability evidence, and other content-addressed protocol resources.

They may earn compensation for measurable useful service.

They do not vote on the canonical chain.

Proof-of-service is evidence for service accounting and rewards; it is not a second consensus mechanism. A storage operator cannot gain additional fork-choice authority by storing more data or winning more service challenges.

This boundary is deliberate because useful-service incentives and chain-security incentives solve different problems.

## 3. Agents are protocol objects, not accounts on one website

NIAHCIA's longer-term agent architecture treats an Agent as a durable, versioned network identity rather than merely a prompt, API session, or process running on a particular company's server.

The protocol reserves explicit concepts for:

- `Agent`
- `AgentVersion`
- `AgentManifestV1`
- `Model`
- `ExecutionProfile`
- `ComputeWorker`
- `Operator`
- `ServiceNode`
- `Job`
- `VerificationPolicy`
- `Capability`
- `MemoryDescriptor`
- `PaymentPlan`
- `ResultCommitment`
- `ExecutionReceiptV1`

This makes it possible to reason about agent ownership, upgrades, permissions, tools, memory, model selection, compute execution, verification, payments, delegation, portability, and execution history as versioned protocol relationships rather than hidden application behavior.

The intended end state is that an agent can survive the disappearance of the original frontend or execution host because its identity and authorized relationships are not owned by that frontend.

## 4. Agent sovereignty means portable authority and state

A decentralized agent should not become property of whichever server currently runs its inference process.

NIAHCIA is therefore developing `AgentManifestV1` as a portable integrity-verifiable description of an agent's authorized environment. It binds an exact AgentVersion to model/execution policy, capabilities, memory descriptors, payment policy, privacy policy, succession policy, storage manifests, and lineage commitments.

The intended portability invariant is that an independent compatible host can resolve the same authorized execution environment from the same manifest and referenced canonical content without inheriting ownership of the agent.

That means the physical GPU becomes a replaceable execution resource rather than the agent's identity.

Portable memory does not mean making private memory public. Memory can remain encrypted, access-controlled, content-addressed, or distributed while the manifest commits to the authorized descriptors and integrity roots.

## 5. Agent lineage and succession should be verifiable

`AgentVersion` already forms an immutable append-only execution history. `AgentManifestV1` extends the portability model with an explicit lineage commitment so a host or requester can verify which authorized version and policies it is executing.

NIAHCIA also reserves a succession-policy commitment. The purpose is to make creator/controller disappearance a protocol-defined event rather than an emergency handled by whichever server happens to possess a copy.

Concrete succession state machines are not yet locked. Candidate future policies may include immutable/no succession, designated successors, contract governance, threshold governance, time-delayed succession, or deliberate dormancy.

An execution host must never gain the right to seize an agent merely because the previous controller or host disappeared.

## 6. Capability-native security should constrain agents and hosts

An agent with a treasury should not need to hand every inference host unrestricted wallet authority.

NIAHCIA's capability model is intended to support least-privilege execution: permitted tools/services, destinations/contracts, budgets, expiration, delegation limits, model/profile access, memory/storage access, rate limits, and revocation can be committed as explicit authority.

The goal is that compromising one worker does not automatically compromise the agent's complete identity or economic authority.

This is especially important for autonomous agents that may purchase compute, storage, verification, or services without a human approving every individual request.

## 7. Compute should be replaceable

NIAHCIA does not intend to enshrine today's AI stack into permanent blockchain consensus.

The initial runtime direction includes vLLM, but model and runtime behavior belongs behind versioned `Model` and `ExecutionProfile` objects.

That distinction matters.

If a better inference runtime appears, the network should be able to support it without changing the meaning of RandomX blocks.

If a new accelerator class appears, compute workers should be able to advertise compatible profiles without changing fork choice.

If one model disappears, an agent should be able to move to an authorized replacement according to its version/policy rather than requiring a chain fork merely because an AI vendor or model changed.

## 8. Verification is a protocol problem

A worker signature proves who claimed to perform work. It does not prove the work was correct.

NIAHCIA therefore separates execution from verification.

`VerificationPolicy` is intended to describe what evidence or agreement is required for a particular class of job. The network should be able to evolve among different verification approaches rather than permanently imposing one universal redundant-execution formula.

The earlier fixed Prototype-0 2-of-3 assumption has been superseded. Redundant execution may still be useful for some workloads, but it is a policy option rather than a universal definition of correctness.

This leaves room for approaches such as deterministic re-execution, sampled auditing, optimistic challenge systems, trusted-execution evidence, specialized proofs, or future techniques where their security properties justify them.

## 9. Execution receipts make machine work auditable

NIAHCIA is developing `ExecutionReceiptV1` as a privacy-aware canonical record that can bind a Job to the exact AgentVersion/manifest, model, execution profile, worker, result commitment, verification policy/evidence, resource accounting, and settlement outcome.

The receipt is evidence rather than correctness by declaration. Verification remains controlled by the referenced VerificationPolicy and canonical protocol state.

Private prompts, results, or memory do not need to be published merely to create an audit trail. The receipt can commit to private material while revealing only the protocol relationships required for independent verification.

This gives agents and users a verifiable history of machine work without requiring one centralized logging or reputation service.

## 10. Privacy should be a job/policy property

Confidential execution should not be treated as a single global network switch.

NIAHCIA's portability design reserves an explicit privacy-policy commitment so different work can eventually declare different requirements: for example public work, encrypted inputs, private results, protected memory, or attested confidential execution.

Concrete privacy modes are not yet locked. The architectural requirement is that a worker unable to satisfy a job's declared privacy requirements must not be considered an equivalent execution host.

This allows privacy mechanisms to evolve without hard-coding one TEE vendor or one cryptographic technique into PoW consensus.

## 11. Storage should be reconstructable, not hosted

A decentralized AI network is not meaningfully decentralized if its models, manifests, agent memory, or execution dependencies disappear when one project's server goes offline.

NIAHCIA's storage direction therefore favors content addressing, canonical manifests, independently verifiable chunks, service discovery, and proof of useful availability.

The objective is not merely to duplicate files. It is to make protocol-relevant resources independently identifiable and verifiable so that another node can retrieve and reconstruct the same object without trusting the original host.

## 12. The blockchain should survive AI failure

One of the simplest tests of the architecture is failure isolation.

If every AI compute worker temporarily disappears, the blockchain should continue producing and validating blocks.

If every service/storage node temporarily disappears, PoW consensus should continue even though higher-level services may become unavailable.

If the primary website disappears, nodes, miners, workers, service nodes, and agents should not lose the protocol itself.

If a model host disappears, canonical identifiers and manifests should allow other eligible providers to restore the service where data remains available.

If the original developers disappear, the protocol should remain understandable from its specifications and independently implementable.

No single subsystem should secretly become the network's control plane.

## 13. Native economics connect independent resource markets

NIAHCIA distinguishes the economic roles performed by different participants:

- CPU miners provide chain security.
- compute workers provide AI execution.
- service/storage nodes provide measurable network services.
- verifiers may provide verification work under policies that compensate it.
- agents and users purchase execution, storage, or other services according to protocol rules.

Payment can connect these systems without equating them.

A GPU worker can earn for useful compute without becoming a miner. A storage node can earn for availability without becoming a validator. A miner can secure the chain without running an LLM.

The longer-term objective includes agent-to-agent service relationships: one agent should be able to discover a capability offered by another participant, fund a Job, obtain a committed/verifiable result, and settle according to protocol rules without either agent depending on the identity of the physical GPU that performed the work.

This is intended to produce an economy of specialized decentralized resources rather than one monolithic node role.

## 14. Smart contracts are part of the substrate

NIAHCIA integrates EVM execution through Reth rather than inventing a completely isolated contract environment.

The consensus daemon remains responsible for NIAHCIA chain ordering and PoW consensus; Reth provides EVM execution and execution-state validation across an explicit authenticated boundary.

This allows autonomous agents and decentralized services to interact with programmable settlement while keeping NIAHCIA's native consensus identity separate from execution-engine implementation details.

## 15. Common infrastructure should remain common where practical

NIAHCIA should not fork mature ecosystem software merely to create artificial uniqueness.

Examples of this philosophy include:

- standard RandomX rather than a branded custom RandomX VM;
- an explicit goal of interoperability with ordinary/common RandomX miners and pools where protocol-safe;
- EVM execution through Reth rather than inventing a new smart-contract VM solely for differentiation;
- versioned AI runtimes rather than consensus-locking one inference implementation.

NIAHCIA should innovate where its protocol requires a new abstraction and reuse established infrastructure where established infrastructure already solves the problem safely.

## 16. Decentralized scheduling should not become a hidden coordinator

A network can advertise itself as decentralized while still depending on one scheduler to decide where every AI request goes.

NIAHCIA's compute architecture therefore treats worker discovery, eligibility, assignment, execution, result commitment, verification, timeout, reassignment, and settlement as protocol concerns.

The objective is not that every scheduling decision must be written directly into a block. The objective is that no permanent privileged scheduler becomes necessary for the system to function or impossible for independent participants to replace.

## 17. Protocol-first interoperability

NIAHCIA maintains a separate protocol repository because the Rust node should not become the only definition of the network.

Consensus-critical and interoperability-critical objects require deterministic serialization, explicit domain separation, versioning, and canonical test vectors.

A second implementation should eventually be able to implement NIAHCIA from the protocol specifications without reverse-engineering the Rust source.

This also makes protocol drift visible: implementation behavior cannot silently become consensus law merely because one node happens to do it.

## What NIAHCIA is not

NIAHCIA is not intended to be:

- a blockchain where every miner must run an AI model;
- a GPU-rental marketplace with a token attached;
- a storage network that controls blockchain finality;
- a single hosted AI API paid with cryptocurrency;
- a fixed 2-of-3 inference voting system;
- a blockchain permanently tied to one LLM, one runtime, one accelerator vendor, or one website;
- a system where an inference host automatically owns the agent it executes;
- a reason to fork mature software when interoperable standard software can safely be used.

## What success would look like

A mature NIAHCIA network should make the following flow possible without requiring a permanent central operator:

```text
Agent A
   |
   +-- resolves its portable authorized manifest/state
   +-- discovers Agent B / required capability
   +-- constructs and funds a Job
   v
eligible compute is discovered/selected
   |
   v
independent compute worker
   |
   +-- verifies AgentVersion/manifest/capabilities
   +-- retrieves canonical model/profile/input
   +-- executes work
   +-- streams permitted output
   +-- commits result/evidence
   v
VerificationPolicy
   |
   +-- accept / challenge / audit / reassign as specified
   v
ExecutionReceipt + settlement
   |
   +-- worker/verifier/service compensation
   +-- auditable committed execution history
   +-- result becomes available to authorized participant(s)
```

Meanwhile, CPU miners continue securing the chain independently and service/storage nodes continue preserving network resources independently.

The agent can later execute on a different eligible host without changing its identity merely because the physical machine changed.

That composition—not any single AI model—is the core NIAHCIA idea.

## Current reality

NIAHCIA is pre-alpha.

Several protocol primitives and test vectors exist, and the reference implementation is actively developing consensus, synchronization, Reth integration, storage/service primitives, identities, monetary representation, and related infrastructure. `AgentManifestV1` and `ExecutionReceiptV1` are currently candidate specifications, not implemented production guarantees. Other parts—especially mature autonomous-agent execution, decentralized scheduling, production AI verification/privacy, succession, full economic policy, and public production networking—remain design and implementation work.

Accordingly, NIAHCIA's present differentiation is best described as an **architectural direction being implemented and tested**, not as a claim of production superiority over existing decentralized AI networks.

## Design test

When considering a future feature, ask:

> Does this make NIAHCIA more independently operable, verifiable, replaceable, portable, least-privileged, and permissionless—or does it quietly create a new central dependency?

If a proposed AI provider, scheduler, storage host, website, validator group, model repository, execution host, or developer-controlled service becomes indispensable, the design should be reconsidered.

The objective is not decentralization as branding. The objective is a network whose important roles can actually be replaced by independent participants.