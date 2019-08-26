#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2019 Pod Group Ltd
# Authors : J. Félix Ontañón <felix.ontanon@podgroup.com>

from setuptools import setup

setup(
    name="kiopcgenerator",
    author="J. Félix Ontañón",
    author_email="felix.ontanon@podgroup.com",
    url="https://github.com/PodgroupConnectivity/kiopcgenerator",
    description="OPc USIM card keys geneartion. This script will produce Ki/eKi/OPc triplets given the Op and Transport keys.",
    long_description=open("README.md", "r").read(),
    classifiers=[
        'Development Status :: 0.1.2 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    keywords = ['python', 'sim', 'simcard', 'telecoms'],
    version="0.1.2",
    license="GPLv3",
    setup_requies=['wheel'],
    install_requires=[
        'pycrypto',
        # I cannot undertstand how such a specific dependency like the following
        # installing card-0.0.1 instead of card-0.3.1. I'm afraid you'll have to manually install this 
        'card @ git+https://github.com/PodgroupConnectivity/card.git@b8eb2c70eaad754a631a9fcbd1ce0dba4b58a662#egg=card-0.3.1'
    ],
    packages=['kiopcgenerator'],
    scripts = ["kiopcgen"]
)
