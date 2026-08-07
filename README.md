# Ki/OPc Generator

Ki/OPc USIM card key generation. This tool produces Ki/eKi/OPc triplets given the OP and Transport keys, and can recover Ki back from an eKi.

OPc is the subscriber-specific key derived from OP and Ki (the secret subscriber key).
Generate your Ki secret keys and grab the OP and Transport keys from your carrier.

**NOTE**: Requires Python 3.6 or later. The test suite currently runs on Python 3.12.

## Table of Contents

- [Description](#description)
- [Algorithm](#algorithm)
- [Usage](#usage)
- [Installation](#installation)
- [Testing](#testing)
- [References](#references)
- [Support](#support)
- [Contributing](#contributing)

## Description

**OP (Operator Variant Algorithm Configuration Field)**: a 128-bit value allotted to an operator and used in the key generation algorithms of 3G/4G/5G networks. It is not subscriber-specific: it remains the same for all SIMs of an operator. The OP value is passed, together with the subscriber key Ki, to an AES-based (Rijndael) derivation to produce OPc, and it is OPc that the MILENAGE f1–f5 functions use internally to generate authentication vectors.

Since a single OP value is shared by all of an operator's SIMs, a leak of OP would weaken every SIM at once. For that reason operators provision the derived, subscriber-specific OPc — rather than OP — in the AuC or HLR/HSS and on the card. When the f1–f5 functions receive OPc they use it directly, without ever needing OP, and OPc cannot feasibly be reversed to obtain OP. If an OPc is stolen, only that single SIM is compromised.

**Ki (subscriber authentication key K)**: the 128-bit secret key shared between the USIM and the operator's AuC/HSS, as defined by the 3GPP AKA security framework. It is unique per SIM.

**Transport key**: a 128-bit key (32 hex chars in this tool) used to protect credentials in transit. When authentication credentials are exchanged between SIM vendors and operators or provisioned into the AuC or HLR/HSS, Ki is transported in encrypted form (eKi) rather than in the clear, and only decrypted back to the plain Ki where it is actually used.

## Algorithm

This tool implements the standard MILENAGE OPc derivation, specified by 3GPP and published by ETSI:

- **OPc derivation** (3GPP TS 35.205 / TS 35.206; ETSI TS 135 205 / 135 206): `OPc = OP XOR AES-128(Ki, OP)`, i.e. OP encrypted with AES-128 (Rijndael) under Ki, then XORed with OP. The implementation encrypts the single 16-byte block with AES-CBC and an all-zero IV, which is equivalent to AES-ECB for one block. No custom rotations or constants are involved: the MILENAGE rotations (r1..r5) and constants (c1..c5) only apply to the f1–f5* authentication functions, not to the OPc derivation. The output is verified against MILENAGE Test Set 1 from 3GPP TS 35.207 / TS 35.208 (ETSI TS 135 207 / 135 208) in the test suite.
- **Ki generation**: a randomly generated 128-bit value (from a version-4 UUID). Ki plays the role of the subscriber key K in the 3GPP AKA framework (3GPP TS 33.102 for 3G, TS 33.401 for LTE, TS 33.501 for 5G).
- **eKi**: AES-128-CBC encryption of Ki under the Transport key, with an all-zero IV. Recovering Ki from eKi is the corresponding decryption. Encrypting Ki under a per-vendor transport key for exchange follows the industry practice described in GSMA FS.28 (Security Guidelines for Exchange of UICC Credentials), which lists AES-128 among the accepted transport-key algorithms.

MILENAGE is one of the two 3GPP-standardized algorithm sets for AKA — the other being TUAK (3GPP TS 35.231), based on Keccak. This tool covers MILENAGE only.

## Usage

Use from the command line with the **kiopcgen** tool:

```
Usage: kiopcgen [options]

Options:
  -h, --help                  show this help message and exit
  -o OP, --op=OP              32 char OP key
  -t TRANS, --transport=TRANS 32 char Transport key
  -k KI, --ki=KI              Optional 32 char Ki key (to avoid random generation)
  -e EKI, --eki=EKI           32 char eKI key (to recover Ki)

$ kiopcgen  -o D7DECB1F50404CC29ECBF989FE73AFC5 -t 2257CC6E9746434B89F346F0276CCAEC
{'KI': '780E6AC95A2E43449C15BDCDD0450982',
 'OPC': '2274B84B8043105A28AABBE53EF1D014',
 'eKI': '4601138387FCF7D666ED24BBB3EE37B8'}

$ kiopcgen -o D7DECB1F50404CC29ECBF989FE73AFC5 -t 2257CC6E9746434B89F346F0276CCAEC -k 8978B79E7C104F678FA5C336509DB188
{'KI': '8978B79E7C104F678FA5C336509DB188',
 'OPC': '6F2E82855DEE7C893CB1F7A72FD08B57',
 'eKI': 'FBE8C170F6A5C6C257E5324719674818'}

Or recover Ki from an encrypted eKi:

$ kiopcgen -o D7DECB1F50404CC29ECBF989FE73AFC5 -t 2257CC6E9746434B89F346F0276CCAEC -e 4601138387FCF7D666ED24BBB3EE37B8
{'KI': '780E6AC95A2E43449C15BDCDD0450982',
 'OPC': '2274B84B8043105A28AABBE53EF1D014',
 'eKI': '4601138387FCF7D666ED24BBB3EE37B8'}
```

Or import the kiopcgenerator module to use in your scripts

```python
import pprint
import uuid
import kiopcgenerator
 
op = "D7DECB1F50404CC29ECBF989FE73AFC5"
transport = "2257CC6E9746434B89F346F0276CCAEC"
ki = kiopcgenerator.gen_ki() # Generates random ki

print (ki)
# EBD77DF6CFF949448ACF82B8FE4E59E3
print (kiopcgenerator.gen_opc(op, ki))
# 33244F04A86408A53110D1FCAFD04288
eki = kiopcgenerator.gen_eki(transport, ki)
print (eki)
# 8FAC9FE22D306EA4CB86279B3473D8CB
print (kiopcgenerator.gen_opc_eki(op, transport, ki))
# {'KI': 'EBD77DF6CFF949448ACF82B8FE4E59E3', 'eKI': '8FAC9FE22D306EA4CB86279B3473D8CB', 'OPC': '33244F04A86408A53110D1FCAFD04288'}

# Recover Ki from eKi
print (kiopcgenerator.recover_ki(op, transport, eki))
# {'KI': 'EBD77DF6CFF949448ACF82B8FE4E59E3', 'eKI': '8FAC9FE22D306EA4CB86279B3473D8CB', 'OPC': '33244F04A86408A53110D1FCAFD04288'}
```

## Installation

Recent Linux distributions mark the system Python as externally managed ([PEP 668](https://peps.python.org/pep-0668/)), so `sudo pip3 install` fails with an `externally-managed-environment` error. Install with [pipx](https://pipx.pypa.io/) instead, which manages a virtual environment for you (recommended for the `kiopcgen` command-line tool):

```
$ pipx install git+https://github.com/iotconnectivity/kiopcgenerator#egg=kiopcgenerator
```

Or inside a virtual environment (recommended to use the library from your own code):

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install git+https://github.com/iotconnectivity/kiopcgenerator#egg=kiopcgenerator
```

From source code

```
$ pip install .
```

NOTE: You may want to install the dependencies in advance, if you haven't yet.
```
$ pip install -r requirements.txt
```

## Testing

Run the test suite with:

```
$ python -m unittest discover -s tests
```

## References

- [3GPP TS 35.205 (ETSI TS 135 205)](https://www.etsi.org/deliver/etsi_ts/135200_135299/135205/) — MILENAGE algorithm set: General
- [3GPP TS 35.206 (ETSI TS 135 206)](https://www.etsi.org/deliver/etsi_ts/135200_135299/135206/) — MILENAGE algorithm specification (defines the OPc derivation)
- [3GPP TS 35.207 (ETSI TS 135 207)](https://www.etsi.org/deliver/etsi_ts/135200_135299/135207/) — MILENAGE implementers' test data
- [3GPP TS 35.208 (ETSI TS 135 208)](https://www.etsi.org/deliver/etsi_ts/135200_135299/135208/) — MILENAGE design conformance test data
- [3GPP TS 33.102 (ETSI TS 133 102)](https://www.etsi.org/deliver/etsi_ts/133100_133199/133102/) — 3G security architecture (defines the subscriber key K and AKA)
- [GSMA FS.28](https://www.gsma.com/solutions-and-impact/technologies/security/gsma_resources/fs-28-security-guidelines-for-exchange-of-uicc-credentials/) — Security Guidelines for Exchange of UICC Credentials (transport-key protection of Ki)

## Support

Please [open an issue](https://github.com/iotconnectivity/kiopcgenerator/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.
