#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2019 Podsystem Ltd
# Authors : J. Félix Ontañón <felix.ontanon@podgroup.com>
# Modify for python3: Mahfuzur Rahman Khan <mahfuzku11@gmail.com>

"""
OPc and eKi generator for python3 and upper version.
More info: https://diameter-protocol.blogspot.com/2013/06/usage-of-opopc-and-transport-key.html
"""
import uuid
import binascii
from Crypto.Cipher import AES

# from card.utils import stringToByte, byteToString - Removed from package as not needed.

# Based on OSMO-SIM-AUTH library: https://osmocom.org/projects/osmo-sim-auth
class AuChss:
    """
    implements a simple AuC / HSS with no persistent storage
    set _debug = 1 to print out internal debug
    """
    _debug = 0

    def __init__(self, op_hex="00000000000000000000000000000000", debug=0):
        self.op_bin = bytes(op_hex, 'utf-8')  # Operator Key
        self.op = self.op_bin.decode('utf-8')
        self.users = []

    def calc_opc_hex(self, k_hex, op_hex=None):
        iv = binascii.unhexlify(16 * '00')
        ki = binascii.unhexlify(k_hex)

        if not op_hex == None:
            op = binascii.unhexlify(op_hex)
        else:
            op = binascii.unhexlify(self.op)
        if self._debug:
            print(f'[DBG]calc_opc_hex: op({len(op)}) KI({len(ki)}) IV({len(iv)})')
            print(f'[DBG]calc_opc_hex: OP, {op} KI, {ki} IV, {iv}')

        aes_crypt = AES.new(ki, mode=AES.MODE_CBC, IV=iv)
        data = op
        o_pc = self._xor_str(data, aes_crypt.encrypt(data))
        return binascii.hexlify(o_pc)

    def _xor_str(self, s, t):
        """xor two strings together"""
        return bytes([_a ^ _b for _a, _b in zip(s, t)])

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
    return str(uuid.uuid4()).replace('-', '').upper()


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
