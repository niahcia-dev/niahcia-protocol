# Canonical Field ID Registry

## Status

Draft — Protocol v1 foundation.

This document assigns permanent numeric field identifiers used by NCE/1 canonical maps.

## Rules

- field IDs are unsigned integers
- field IDs are permanent once assigned
- removed/deprecated IDs remain reserved
- IDs are never reused for another semantic meaning within the same object type
- new fields append new IDs unless a specification explicitly reserves a range
- payload key `1` is `schema_version` for all core protocol objects
- the payload `schema_version` MUST equal the top-level NCE/1 envelope schema version

---

## Agent — object type 0x0001

```text
1   schema_version
2   agent_id
3   creator
4   controller
5   governance_mode
6   current_version
7   treasury_address
8   status
9   created_block
10  metadata_uri
```

## AgentVersion — object type 0x0002

```text
1   schema_version
2   agent_id
3   version
4   definition_hash
5   primary_models
6   fallback_models
7   execution_profiles
8   verification_policy_id
9   system_definition_hash
10  tool_manifest_hash
11  permission_manifest_hash
12  memory_policy_hash
13  economic_policy_hash
14  trigger_policy_hash
15  child_agent_policy_hash
16  previous_version
17  created_block
```

## Model — object type 0x0003

```text
1   schema_version
2   model_id
3   creator
4   name
5   architecture
6   weights_manifest_hash
7   tokenizer_hash
8   config_hash
9   license_id
10  license_hash
11  manifest_uri
12  supported_workloads
13  supported_execution_profiles
14  status
15  created_block
```

## ExecutionProfile — object type 0x0004

```text
1   schema_version
2   profile_id
3   runtime
4   runtime_version
5   runtime_build_hash
6   hardware_requirements
7   precision
8   quantization
9   context_limit
10  determinism_mode
11  batch_policy
12  seed_policy
13  generation_policy
14  supported_workloads
15  input_format_version
16  output_format_version
17  profile_hash
```

## Operator — object type 0x0005

```text
1   schema_version
2   operator_id
3   controller
4   payment_address
5   bond
6   status
7   workers
8   service_nodes
9   reputation_ref
10  created_block
```

## ComputeWorker — object type 0x0006

```text
1   schema_version
2   worker_id
3   operator_id
4   controller
5   payment_address
6   execution_profiles
7   hardware_capabilities
8   workload_types
9   capacity
10  queue_state
11  models_hot
12  models_warm
13  pricing_policy
14  bond
15  reputation_ref
16  availability_expiry
17  endpoint_descriptor
18  advertisement_signature
19  status
```

## ServiceNode — object type 0x0007

```text
1   schema_version
2   service_node_id
3   operator_id
4   controller
5   payment_address
6   services
7   storage_capacity
8   bandwidth_class
9   stored_manifests
10  availability_state
11  endpoint_descriptor
12  pricing_policy
13  bond
14  reputation_ref
15  status
```

## Job — object type 0x0008

```text
1   schema_version
2   job_id
3   requester
4   agent_id
5   agent_version
6   model_id
7   execution_profile_id
8   workload_type
9   input_manifest_hash
10  output_requirements_hash
11  verification_policy_id
12  payment_plan_id
13  resource_requirements
14  privacy_requirements
15  scheduling_policy
16  parent_job_id
17  root_job_id
18  created_block
19  deadline_block
20  status
21  accepted_result_id
```

## VerificationPolicy — object type 0x0009

```text
1   schema_version
2   policy_id
3   type
4   executor_count
5   agreement_threshold
6   challenge_window
7   audit_probability
8   audit_count
9   bond_requirements
10  dispute_policy
11  hardware_diversity_rules
12  operator_diversity_rules
13  settlement_delay
14  policy_hash
```

## Capability — object type 0x000A

```text
1   schema_version
2   capability_id
3   subject
4   resource_type
5   resource_identifier
6   actions
7   limits
8   max_spend
9   rate_limit
10  valid_from
11  expiry
12  approval_mode
13  delegate_allowed
14  revocation_ref
15  capability_hash
```

## MemoryDescriptor — object type 0x000B

```text
1   schema_version
2   memory_id
3   scope
4   owner
5   agent_id
6   session_id
7   root_hash
8   storage_manifest_hash
9   encryption_policy
10  read_policy
11  write_policy
12  replication_policy
13  version
14  previous_root
15  updated_block
```

## PaymentPlan — object type 0x000C

```text
1   schema_version
2   payment_plan_id
3   currency
4   max_total
5   escrow_amount
6   executor_budget
7   verifier_budget
8   storage_budget
9   routing_budget
10  child_agent_budget
11  creator_fee
12  protocol_fee
13  refund_policy
14  settlement_policy
15  expiry_policy
16  plan_hash
```

## ResultCommitment — object type 0x000D

```text
1   schema_version
2   commitment_id
3   job_id
4   worker_id
5   operator_id
6   model_id
7   execution_profile_id
8   input_hash
9   output_hash
10  token_or_artifact_hash
11  runtime_receipt_hash
12  output_manifest_hash
13  output_location
14  started_at
15  completed_at
16  submitted_block
17  nonce_or_salt_commitment
18  signature
```

## Derived-field rule

The assigned field ID exists even when the field is excluded from a particular hash/signing preimage.

Examples:

- `profile_id` and `profile_hash` retain their field IDs but are omitted while deriving those values
- `commitment_id` and `signature` retain their IDs but are omitted while deriving/signing a ResultCommitment
- a stable `agent_id` is included in normal Agent serialization, but its creation derivation uses the separate `ID/AGENT` formula

Exclusion is a preimage rule, not a renumbering rule.
