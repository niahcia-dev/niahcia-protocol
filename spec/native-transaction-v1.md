# NIAHCIA Native Transaction V1

## Status

**CANDIDATE / interoperability design**

This specification defines the canonical NIAHCIA V1 signed transaction
envelope.

NIAHCIA owns transaction identity, native signing-domain separation,
network/chain replay protection, canonical transaction bytes, transaction
ordering, and the consensus commitment to those bytes.

The execution engine owns EVM execution semantics and execution state.

## Design boundary

A `NativeTransactionV1` is not an Ethereum raw transaction and its identifier
is not an Ethereum transaction hash.

A native transaction may request execution whose effects are performed by the
EVM execution engine, but execution-layer conventions MUST NOT silently
redefine the canonical NIAHCIA transaction.

NIAHCIA consensus validates the resulting execution commitment according to
the applicable block/execution protocol.

## Native transaction body

The canonical unsigned body is an NCE/1 object with permanent object type
`0x0010` (`NativeTransactionBody`) and schema version `1`.

The NCE/1 envelope carries `schema_version = 1`.

The NCE/1 payload fields are:

    1   network_id
    2   chain_id
    3   nonce
    4   to_kind
    5   to_payload
    6   value
    7   gas_limit
    8   max_fee_per_gas
    9   data

`network_id`, `chain_id`, `nonce`, `to_kind`, and `gas_limit` use canonical
NCE/1 unsigned-integer encoding.

`to_payload` is a CBOR byte string of exactly 20 bytes.

`value` and `max_fee_per_gas` are integer `aniah` quantities represented as
exactly 16 unsigned big-endian bytes inside NCE/1 CBOR byte strings, consistent
with Monetary and Fee Primitives V1.

`data` is a definite-length CBOR byte string. Its length is encoded by the
canonical CBOR byte-string representation; no separate `data_length` field is
serialized.

The NCE/1 envelope `schema_version` MUST equal `1`.

`network_id` and `chain_id` MUST match the configured NIAHCIA network.

## Recipient

`to_kind` uses the Address V1 kind values:

    0x00 Account
    0x01 Contract

`to_payload` is exactly the 20-byte Address V1 payload.

The human-facing Bech32m HRP is not serialized into the transaction body.
Network identity is committed independently through `network_id` and
`chain_id`.

A node reconstructing a human-facing recipient MUST use the transaction's
validated network and the specified address kind/payload.

Unknown recipient kinds are invalid in V1.

## Sender

The sender is not independently serialized as an address in the unsigned
transaction body.

The sender Account Address V1 payload is derived from the transaction's
authenticated secp256k1 public key according to Address V1:

    public_key = 0x04 || X || Y
    digest = Keccak-256(X || Y)
    sender_payload = digest[12..32]

This prevents a transaction from carrying an independently claimed sender
that disagrees with its cryptographic signer.

## Account transaction nonce

Each Account has a monotonically increasing native transaction nonce.

For ordinary V1 transaction execution:

    tx.nonce == current_sender_transaction_nonce

is required.

A stale nonce is invalid.

A future nonce is not executable until all preceding sender nonces have been
satisfied. Mempool policy for retaining future-nonce transactions is an
implementation concern unless separately specified.

The native account transaction nonce is distinct from:

- registry nonces;
- object-creation nonces;
- Job nonces;
- Agent intent identifiers;
- storage/service protocol nonces;
- EVM contract-creation nonce semantics.

Exact nonce consumption on successful execution, failed execution, and EVM
revert MUST be locked together with the execution-transition rules before V1
is production-final.

## Signed transaction envelope

The canonical signed envelope is:

    SignedNativeTransactionV1
    - body: NativeTransactionBodyV1
    - public_key: bytes65
    - signature: bytes64

`public_key` MUST be canonical uncompressed SEC1:

    0x04 || X || Y

and MUST encode a valid secp256k1 public key.

`body` is a CBOR byte string containing the complete canonical NCE/1 bytes of
NativeTransactionBodyV1, including its top-level NCE/1 envelope.

The embedded body bytes MUST be exactly the same bytes used as
`canonical_unsigned_body` when computing the signing digest. An implementation
MUST NOT substitute a different serialization of the body inside
SignedNativeTransactionV1.

`public_key` is a CBOR byte string of exactly 65 bytes.

`signature` is the canonical fixed-width secp256k1 ECDSA representation:

    r || s

where both `r` and `s` are exactly 32-byte unsigned big-endian integers.

High-S signatures MUST be rejected. V1 accepts only canonical low-S ECDSA
signatures.

DER encoding is not part of the canonical V1 transaction format.

## Signing digest

The signature authenticates the complete canonical unsigned transaction body
using the protocol-wide signing-domain construction.

For Native Transaction V1:

    signing_purpose = "SIGN/NATIVE_TRANSACTION"

and:

    signing_digest =
      Keccak-256(
        "NIAHCIA" ||
        0x00 ||
        "SIGN/NATIVE_TRANSACTION" ||
        0x00 ||
        network_id ||
        0x00 ||
        canonical_unsigned_body
      )

The quoted domain strings are literal ASCII bytes.

`network_id` in the outer signing domain is the same validated network ID
encoded inside `canonical_unsigned_body`. A mismatch is invalid.

The explicit outer network domain is intentional even though the body also
contains `network_id` and `chain_id`: the outer value provides protocol-level
signing-domain separation while the canonical body independently commits to
the transaction's network and chain semantics.

`canonical_unsigned_body` is the complete canonical NCE/1 serialization of
NativeTransactionBody V1, including the top-level NCE/1 envelope with object
type `0x0010`.

The signature MUST verify against `signing_digest` and the serialized public
key.

## Canonical signed bytes

The canonical raw transaction bytes are the canonical serialization of:

    SignedNativeTransactionV1

No JSON, hexadecimal text, Bech32m text, DER signature, execution-engine
transaction encoding, or RPC representation is canonical transaction
serialization.

Canonical serialization MUST be deterministic and uniquely decodable.

## Transaction identifier

The native transaction identifier is:

    tx_id =
      Keccak-256(
        "NIAHCIA/TX-ID/V1" ||
        canonical_signed_transaction_bytes
      )

`tx_id` is a 32-byte native protocol identifier.

Default display form:

    0x<64 lowercase hexadecimal characters>

An execution-engine transaction/block identifier MUST NOT substitute for
`tx_id`.

## Block transaction commitment

The exact same `canonical_signed_transaction_bytes` are supplied as `tx` to
the Transaction Merkle Tree V1 rules.

Therefore:

    tx_digest =
      Keccak-256(
        "NIAHCIA/TX/V1" ||
        canonical_signed_transaction_bytes
      )

and `tx_id` remain deliberately domain-separated commitments.

## Value and maximum fee reserve

Before execution, checked integer arithmetic computes:

    max_fee_reserve =
        gas_limit * max_fee_per_gas

    required_balance =
        value + max_fee_reserve

The sender MUST have at least `required_balance` available according to the
authoritative pre-state.

Overflow is invalid.

## Execution request

The native transaction maps to an execution request containing at least:

- authenticated sender execution address;
- recipient execution address;
- value;
- gas limit;
- execution calldata.

For an Account recipient with empty `data`, the ordinary intended operation is
a value transfer.

For a Contract recipient, `data` may contain EVM calldata.

The exact deterministic native-value/execution-value conversion and
fee/gas mapping MUST be specified before this candidate becomes locked.

NIAHCIA MUST NOT invent competing EVM CREATE or CREATE2 address derivation.

## Execution result

The authoritative execution result provides the execution outcome and
`gas_used`.

It MUST satisfy:

    gas_used <= gas_limit

The applicable fee rules determine:

    effective_fee_per_gas <= max_fee_per_gas

and:

    charged_fee =
        gas_used * effective_fee_per_gas

    unused_fee_reserve =
        max_fee_reserve - charged_fee

    sender_charge =
        value + charged_fee

All arithmetic is checked.

The final disposition of fee components is governed by the applicable
versioned economic policy and is not inferred from the execution engine.

## Failure and revert boundary

The following cases MUST be distinguished by the final V1 transition rules:

1. transaction invalid before execution;
2. transaction accepted for execution and succeeds;
3. transaction accepted for execution but EVM execution reverts;
4. transaction accepted for execution and exhausts its permitted gas;
5. execution result inconsistent with the NIAHCIA transaction or block
   commitment.

Invalid-before-execution transactions MUST NOT become valid merely because an
execution engine accepts some corresponding request.

The exact nonce and fee consequences of cases 2-4 remain to be locked before
production V1.

## Replay protection

V1 replay protection includes at least:

- `network_id`;
- native `chain_id`;
- sender-derived identity;
- account transaction `nonce`;
- signing-purpose domain separation.

An execution chain ID does not replace the native NIAHCIA chain ID.

## Required interoperability vectors

Before this specification is LOCKED, vectors MUST cover at least:

1. canonical unsigned-body serialization;
2. signing digest;
3. secp256k1 public-key validation;
4. low-S signature acceptance;
5. high-S signature rejection;
6. signature mismatch rejection;
7. sender Account derivation;
8. mainnet/testnet/devnet replay separation;
9. wrong native chain-ID rejection;
10. nonce validation;
11. Account-to-Account zero-data transfer;
12. Account-to-Contract calldata transaction;
13. zero-value transaction;
14. maximum valid `u128` field serialization;
15. fee-reserve multiplication overflow;
16. required-balance addition overflow;
17. insufficient-balance rejection;
18. transaction ID;
19. Transaction Merkle leaf compatibility;
20. malformed/truncated transaction rejection;
21. unknown schema-version rejection;
22. unknown recipient-kind rejection.

## Open items before lock

The following remain intentionally unresolved:

- exact native-value to execution-value conversion;
- execution gas-price/base-fee mapping;
- nonce consumption on EVM revert/out-of-gas;
- contract-creation transaction representation;
- transaction expiry/deadline, if any;
- access-list/blob or future execution transaction features;
- production EVM chain IDs;
- final fee disposition policy.

These items require explicit review rather than silent inheritance from
Ethereum or Reth behavior.
