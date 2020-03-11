#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2019 Podsystem Ltd
# Authors : J. Félix Ontañón <felix.ontanon@podgroup.com>

"""
OPc and eKi generator for python3 and upper version.
More info: https://diameter-protocol.blogspot.com/2013/06/usage-of-opopc-and-transport-key.html
"""
import uuid
import binascii
from Crypto.Cipher import AES

from card.utils import stringToByte, byteToString


# Based on OSMO-SIM-AUTH library: https://osmocom.org/projects/osmo-sim-auth
class AuChss():
    """
    implements a simple AuC / HSS with no persistant storage
    """
    _debug = 0

    def __init__(self, OP_hex="00000000000000000000000000000000", debug=0):
        self.OP_bin = stringToByte(OP_hex)  # Operator Key
        self.OP = byteToString(self.OP_bin)
        self.users = []

    def calc_opc_hex(self, K_hex, OP_hex=None):
        IV = 16 * '\x00'
        KI = binascii.unhexlify(K_hex)

        if not OP_hex == None:
            OP = binascii.unhexlify(OP_hex)
        else:
            OP = binascii.unhexlify(self.OP)
        if self._debug:
            print("[DBG]calc_opc_hex: op(%d) KI(%d) IV(%d)" % (len(OP), len(KI), len(IV)))
            print("[DBG]calc_opc_hex: OP", OP, "KI", KI, "IV", IV)

        aesCrypt = AES.new(KI, mode=AES.MODE_CBC, IV=IV)
        data = OP
        OPc = self._xor_bytes(data, aesCrypt.encrypt(data))
        return OPc.hex().upper()

    def _xor_str(self, s, t):
        """xor two strings together"""
        return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s, t))

    def _xor_bytes(self, s, t):
        """xor two bytes together"""
        return bytes(a ^ b for (a, b) in zip(s, t))


# Using 16bit zeroes as IV for the AES algo
IV = binascii.unhexlify('00000000000000000000000000000000')


def aes_128_cbc_encrypt(key, text):
    """
    implements aes 128b encryption with cbc.
    """
    keyb = binascii.unhexlify(key)
    textb = binascii.unhexlify(text)
    encryptor = AES.new(keyb, AES.MODE_CBC, IV=IV)
    ciphertext = encryptor.encrypt(textb)
    return ciphertext.hex().upper()


def gen_ki():
    """
    Clear ki random generator
    """
    # return str(uuid.uuid4()).replace('-','').upper()
    return "EBD77DF6CFF949448ACF82B8FE4E59E3"


def gen_opc(op, ki):
    """
    generates opc based on op and ki
    """
    hss = AuChss()
    return hss.calc_opc_hex(ki, op).upper()


def gen_eki(transport, ki):
    """
    generates eKI based on ki and transport key
    """
    return aes_128_cbc_encrypt(transport, ki)


def gen_opc_eki(op, transport, ki):
    return {"KI": ki, "OPC": gen_opc(op, ki), "eKI": gen_eki(transport, ki)}