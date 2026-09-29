# Service Epoch Report V1

## Status

Draft reward-accounting object.

Service rewards are settled from verified service evidence aggregated over epochs rather than from self-reported uptime.

## Candidate epoch length

```text
SERVICE_EPOCH_BLOCKS = 720
```

At a 30-second target interval this is approximately six hours.

This value is a development candidate, not frozen consensus.

## Canonical fields

```text
ServiceEpochReportV1
- schema_version
- report_id
- service_node_id
- operator_id
- epoch_start_height
- epoch_end_height
- commitments_sampled
- challenges_passed
- challenges_failed
- deadlines_missed
- verified_bytes_served
- distinct_requester_count
- distinct_challenge_block_count
- service_classes
- evidence_root
- eligibility_weight
- created_block
- signature
```

## Principles

- reward accounting MUST be based on verifiable evidence,
- repeated challenges from one friendly identity MUST NOT alone create full eligibility,
- evidence diversity matters,
- collateral or bond ownership alone earns no service reward,
- reputation is advisory and MUST NOT alter chain consensus.

## Evidence root

`evidence_root` commits to the ordered set of challenge/response/retrieval evidence used to calculate the report.

## Eligibility weight

The exact weighting formula is not frozen.

It SHOULD consider:

- challenge success,
- missed deadlines,
- bytes verifiably served,
- requester diversity,
- challenge-block diversity,
- service-class-specific quality metrics.

It MUST NOT include any consensus voting power.
