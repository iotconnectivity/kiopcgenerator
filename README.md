# Ki/OPc Generator

Ki/OPc USIM card keys geneartion. This script will produce Ki/eKi/OPc triplets given the Op and Transport keys.

OPc was the ultimate key that is generated from OP and Ki (secret Key). 
Generate your Ki secret keys and grab the OP and Transport keys from your carrier.

**NOTE**: This package has only been tested with Python2.7

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Installation](#installation)
- [Support](#support)
- [ToDo](#todo)
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

Use from the command line with the **kiopcgen** tool:

```
Usage: kiopcgen [options]

Options:
  -h, --help                  show this help message and exit
  -o OP, --op=OP              32 char OP key
  -t TRANS, --transport=TRANS 32 char Transport key
  -k KI, --ki=KI              Optional 32 char Ki key (to avoid random generation)

$ kiopcgen  -o D7DECB1F50404CC29ECBF989FE73AFC5 -t 2257CC6E9746434B89F346F0276CCAEC
{'KI': '780E6AC95A2E43449C15BDCDD0450982',
 'OPC': '2274B84B8043105A28AABBE53EF1D014',
 'eKI': '4601138387FCF7D666ED24BBB3EE37B8'}

$ kiopcgen -o D7DECB1F50404CC29ECBF989FE73AFC5 -t 2257CC6E9746434B89F346F0276CCAEC -k 8978B79E7C104F678FA5C336509DB188
{'KI': '8978B79E7C104F678FA5C336509DB188',
 'OPC': '6F2E82855DEE7C893CB1F7A72FD08B57',
 'eKI': 'FBE8C170F6A5C6C257E5324719674818'}
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
print (kiopcgenerator.gen_eki(transport, ki))
# 8FAC9FE22D306EA4CB86279B3473D8CB
print (kiopcgenerator.gen_opc_eki(op, transport, ki))
# {'KI': 'EBD77DF6CFF949448ACF82B8FE4E59E3', 'eKI': '8FAC9FE22D306EA4CB86279B3473D8CB', 'OPC': '33244F04A86408A53110D1FCAFD04288'}
```

## Installation

Using PyPI repository

```
$ pip install git+https://github.com/PodgroupConnectivity/kiopcgenerator#egg=kiopcgenerator
```

From source code

```
$ python setup.py install
```

NOTE: You may want to install the dependencies in advance, if you haven't yet.
```
$ pip install -r requirements.txt
```

## Support

Please [open an issue](https://github.com/PodgroupConnectivity/kiopcgenerator/issues/new) for support.

## ToDo

* Porting to python3

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.