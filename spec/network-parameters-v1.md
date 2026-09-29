# NIAHCIA Network Parameters V1

## Status

Draft framework.

NIAHCIA has three independent network classes from the beginning:

```text
devnet
testnet
mainnet
```

Each network has its own genesis block and identity.

## Required network parameters

Each concrete network definition MUST assign:

- network name
- NIAHCIA chain ID
- EVM chain ID
- P2P network magic / protocol identity
- genesis BlockHeaderV1
- genesis block ID
- genesis execution state
- initial PoW target
- PoW limit
- target block interval
- RandomX epoch length
- RandomX seed lag
- protocol activation heights

## Independence

No NIAHCIA network definition may depend on:

- an Ethereum genesis block,
- Ethereum mainnet state,
- Ethereum validators,
- Ethereum beacon-chain state,
- a public Ethereum RPC provider.

Reth is initialized from a NIAHCIA-specific execution chain specification matching the chosen NIAHCIA network.

## Development genesis shape

The first development genesis should remain deliberately minimal:

```text
version           = 1
parent_hash       = 0x00...00
height            = 0
timestamp         = fixed published value
transactions_root = NIAHCIA empty transaction Merkle root
execution_root    = deterministic genesis execution commitment
target            = development pow_limit
nonce             = fixed published value
extra_nonce       = fixed published value
```

## Mainnet

Mainnet genesis values are not selected during Prototype 0.

They must be generated once, reviewed publicly, published in this repository, and embedded/test-vectored before mainnet launch.
