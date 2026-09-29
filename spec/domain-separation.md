# Domain Separation Registry

## Status

Draft.

NIAHCIA uses explicit domain separation for hashes and signatures so that a valid digest in one protocol context cannot be reused in another.

## Rule

Every protocol hash/signature purpose is a permanent ASCII string.

Purpose strings:

- are uppercase
- use `/` separators
- are case-sensitive
- are never localized
- are never reused for a different semantic meaning
- are changed only by defining a new domain string

## Object domains

```text
OBJECT/AGENT
OBJECT/AGENT_VERSION
OBJECT/MODEL
OBJECT/EXECUTION_PROFILE
OBJECT/OPERATOR
OBJECT/COMPUTE_WORKER
OBJECT/SERVICE_NODE
OBJECT/JOB
OBJECT/VERIFICATION_POLICY
OBJECT/CAPABILITY
OBJECT/MEMORY_DESCRIPTOR
OBJECT/PAYMENT_PLAN
OBJECT/RESULT_COMMITMENT
```

## Stable identifier domains

```text
ID/AGENT
ID/OPERATOR
ID/COMPUTE_WORKER
ID/SERVICE_NODE
ID/JOB
ID/MEMORY
```

## Signing domains

```text
SIGN/AGENT_CONTROL
SIGN/OPERATOR_CONTROL
SIGN/WORKER_REGISTRATION
SIGN/WORKER_ADVERTISEMENT
SIGN/SERVICE_REGISTRATION
SIGN/SERVICE_ADVERTISEMENT
SIGN/JOB_REQUEST
SIGN/JOB_ACCEPT
SIGN/JOB_CANCEL
SIGN/RESULT_COMMITMENT
SIGN/RESULT_REVEAL
SIGN/VERIFICATION
SIGN/CAPABILITY
SIGN/MEMORY_UPDATE
SIGN/PAYMENT_AUTHORIZATION
SIGN/P2P_MESSAGE
```

## Storage/manifest domains

```text
MANIFEST/MODEL
MANIFEST/MEMORY
MANIFEST/ARTIFACT
MANIFEST/DATASET
CHUNK/STORAGE
```

## Future domains

New domains require a protocol specification or NIP.

Implementations MUST reject an unknown domain where verification depends on understanding its semantics.

## Consensus domains

The fixed-width consensus formats use the following full ASCII domain strings directly in their hash preimages:

```text
NIAHCIA/BLOCK-HEADER/V1
NIAHCIA/MINING-TEMPLATE/V1
NIAHCIA/EXECUTION-COMMITMENT/V1
NIAHCIA/TX/V1
NIAHCIA/MERKLE-EMPTY/V1
NIAHCIA/MERKLE-LEAF/V1
NIAHCIA/MERKLE-NODE/V1
```

These are consensus constants and are distinct from the generic NCE/1 object-purpose domains above.
