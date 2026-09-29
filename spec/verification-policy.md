# VerificationPolicy

## Purpose

`VerificationPolicy` defines how execution correctness is evaluated without baking one verification mechanism into the protocol.

## Canonical fields

```text
VerificationPolicy
- schema_version
- policy_id
- type
- executor_count
- agreement_threshold
- challenge_window
- audit_probability
- audit_count
- bond_requirements
- dispute_policy
- hardware_diversity_rules
- operator_diversity_rules
- settlement_delay
- policy_hash
```

## Policy types

```text
NONE
REDUNDANT
OPTIMISTIC
AUDITED
TEE
ZK_PROOF
CUSTOM
```

## REDUNDANT

Multiple independent executions are compared using canonical result commitments.

Example Prototype 0:

```text
executor_count = 3
agreement_threshold = 2
operator_diversity = required
```

## OPTIMISTIC

One primary execution is accepted after a challenge window unless challenged.

## AUDITED

Execution is subject to mandatory or probabilistic independent audits.

## TEE / ZK_PROOF

These policy types reserve standardized proof/attestation-driven verification mechanisms. Exact proof systems are defined separately.

## Disagreement

A disagreement does not automatically imply fraud.

Policies MUST distinguish:

- timeout/unavailability
- non-reproducible honest mismatch
- malformed commitment
- cryptographically provable protocol violation
- adjudicated dishonest execution

Penalty policy MUST be explicit.

## Invariants

1. The policy is immutable once used by a Job.
2. Verification mechanism changes do not require PoW consensus changes.
3. Independent verification SHOULD enforce operator diversity where the policy claims independence.
4. Result comparison MUST use canonical serialized commitments.

## Prototype 0

Prototype 0 uses REDUNDANT 2-of-3 agreement with commit-before-reveal and no automatic slashing for ordinary mismatch.
