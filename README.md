# OPc Generator

OPc USIM card keys geneartion. This script will produce the OPc given the Op and Ki. 

OPc was the ultimate key that is generated from OP and Ki (secret Key). Generate your Ki secret keys and grab the OP from your carrier operator. 

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Installation](#installation)
- [Support](#support)
- [Contributing](#contributing)

## Description

OP: Operator Code : It is allotted to an operator and used in key generation algorithms of 3G and 4G. It is not shown as a part of input, because it is not specific to a user/Subscriber/SIM. It remains fix for all Subscriber/SIM of an operator that is why it is not used as an input to key generation algorithms. This OP (a 128-bits Operator Variant Algorithm Configuration Field )value is passed to an encryption algorithm ("RijndaelEncrypt") to generate OPc and OPc is used in all f1,f2,f3,f4,f5 functions internally to generate various keys.

As OP value is single, same to all subscriber/SIM. If someone knows it then there can be a possibility of spoofing of all SIM, because all SIMs are using the same value of OP. So Operator come up with the solution that they shall provision OPc rather than OP in AuC or HLR/HSS. When f1,f2....f5 get the OPc they doesn't generate it from OP; received OPC is used in vector generation. There is no reverse engineering for OP from OPC.

Basically OPc was the ultimate key that is generated from OP and KEy (secret Key) by using  ("RijndaelEncrypt") algorithm which is specific to SIM. if some one able to theft OPc then it can spoof only single SIM not all the SIMs.

OPc=Encypt-Algo(OP,Key)
OPc -[128 Bits]

Transport Key (64-Bits) : This key is used as a Lock to KEY (secret key) and OPc. When authentication credentials are to be provisioned at AuC or HLR/HSS; then they are provisioned in encrypted form rather then plain and this encryption is done by Transport Key. 
When authentication credentials are to be used in Authentication Generation then; all fields are decrypted  to plain key by transport key; and now plain key is used f1,f2,f3,f4,f5 algorithms.

## Usage

Use from the command line with the **opgenereator** tool:

```
$ Usage: opcgenerator [options]

Options:
  -h, --help         show this help message and exit
  -k KEY, --key=KEY  K from USIM
  -o OP, --op=OP     OP operator key

$ opcgenerator -k D7DECB1F50404CC29ECBF989FE73AFC5 -o 2257CC6E9746434B89F346F0276CCAEC
OP: 	2257CC6E9746434B89F346F0276CCAEC
KI: 	D7DECB1F50404CC29ECBF989FE73AFC5
OPc:	5A27120D3C6E32D7053A6B0086F2E312
```

## Installation

From PyPI repository

```
$ sudo pip install opcgenerator
```

From source code

```
~/opcgenerator$ sudo python setup.py install
```

## Support

Please [open an issue](https://github.com/PodgroupConnectivity/opcgenerator/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.