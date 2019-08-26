#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2019 Podsystem Ltd
# Authors : J. Félix Ontañón <felix.ontanon@podgroup.com>

from kiopcgenerator.lib import *

def gen_ki():
    '''
    Clear ki random generator
    '''
    return str(uuid.uuid4()).replace('-','').upper()

def gen_opc(op, ki):
    '''
    generates opc based on op and ki
    '''    
    hss = AuChss()
    return hss.calc_opc_hex(ki, op).upper()

def gen_eki(transport, ki):
    '''
    generates eKI based on ki and transport key
    '''
    return aes_128_cbc_encrypt(transport, ki)

def gen_opc_eki(op, transport, ki):
    return {"KI": ki, "OPC": gen_opc(op, ki), "eKI": gen_eki(transport, ki)}