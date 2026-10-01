# NIAHCIA Address V1

Status: **LOCKED for V1 interoperability**

NIAHCIA Address V1 is the canonical human-readable address container used by nodes, wallets, miners, explorers, SDKs, and other implementations.

## Encoding

Address V1 uses **Bech32m**. The decoded payload is exactly 22 bytes:

```text
offset  size  field
0       1     version
1       1     kind
2       20    payload
```

V1 version is `0x01`.

Kinds:

```text
0x00 Account
0x01 Contract
```

No other V1 kind is valid.

## Network HRPs

```text
mainnet  niah   niah1...
testnet  tniah  tniah1...
devnet   dniah  dniah1...
```

When the expected network is known, an address from another network is invalid.

## Account payload derivation

For a V1 Account, the secp256k1 public key MUST first be represented as the
65-byte uncompressed SEC1 encoding `0x04 || X || Y`.

The `0x04` SEC1 prefix MUST NOT be included in the hash input. The account
payload is derived as:

    digest = Keccak-256(X || Y)
    account_payload_20 = digest[12..32]

`X || Y` is exactly the 64-byte concatenation of the secp256k1 coordinates.

The native address container encodes:

    0x01 || 0x00 || account_payload_20

using Bech32m and the network HRP.

Compressed SEC1 public-key encoding is not a valid input to the Address V1
account-derivation procedure.

## Contract addresses

A V1 Contract address contains the 20-byte execution-layer contract address
produced by the EVM.

The native address container encodes:

    0x01 || 0x01 || contract_payload_20

where `contract_payload_20` is exactly the 20-byte contract address produced
by the authoritative EVM execution result.

NIAHCIA MUST NOT define a competing contract-creation nonce or independently
reinterpret EVM contract-address derivation.

For ordinary EVM `CREATE`, the creator and execution-state nonce semantics are
owned by the EVM execution protocol.

For EVM `CREATE2`, the deployer, salt, and initialization-code hash semantics
are likewise owned by the EVM execution protocol.

Reth is the current NIAHCIA execution engine and is authoritative for execution
state and execution results. NIAHCIA consensus determines canonical ordering
and validates the committed execution result; it does not replace EVM
contract-creation semantics.

After execution determines the 20-byte contract address, NIAHCIA presents that
same payload through its typed, network-aware Bech32m Address V1 container.

A NIAHCIA registry nonce, object creation nonce, job nonce, or other
protocol-object nonce MUST NOT be substituted for the EVM account nonce used
by EVM contract creation.

## Validation

A V1 decoder rejects:

1. invalid Bech32m checksum;
2. unknown NIAHCIA HRP;
3. decoded payload not exactly 22 bytes;
4. version other than `0x01`;
5. undefined V1 kind;
6. network mismatch where a network is required;
7. kind mismatch where a kind is required.

Malformed native addresses must not be silently reinterpreted as hexadecimal or another network's address.

## Execution boundary

The 20-byte payload permits an internal execution-layer address mapping. That mapping does not replace the native NIAHCIA string as the canonical user-facing representation.

A native mining fee recipient is an Account address for the selected network. The node may decode its 20-byte payload for the Reth Engine API internally.

Legacy hexadecimal configuration is an implementation migration facility and is not part of the canonical native Address V1 representation.

## Interoperability vectors

The reference implementation currently carries byte-for-byte vectors for all six network/kind combinations. The protocol vector suite should mirror these fixtures so independent implementations do not need to treat Rust source code as the long-term vector authority.

## Compatibility rule

An already-defined V1 address must never be reinterpreted. Changes to payload length, kind semantics, derivation semantics, checksum/encoding, or network meaning require a new version or explicitly versioned transition.
