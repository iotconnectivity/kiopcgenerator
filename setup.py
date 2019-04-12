#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2019 Pod Group Ltd
# Authors : J. Félix Ontañón <felix.ontanon@podgroup.com>

from setuptools import setup

setup(
    name="opcgenerator",
    author="J. Félix Ontañón",
    author_email="felix.ontanon@podgroup.com",
    url="https://github.com/PodgroupConnectivity/opcgenerator",
    description="OPc USIM card keys geneartion. This script will produce the OPc given the Op and Ki.",
    long_description=open("README.md", "r").read(),
    classifiers=[
        'Development Status :: 0.1.0 - Beta',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
    keywords = ['python', 'sim', 'simcard', 'telecoms'],
    version="0.1.0",
    license="GPLv3",
    install_requires=[
        'pycrypto',
        'card==0.3'
    ],
    dependency_links=[
    'git+https://git@github.com/PodgroupConnectivity/card.git@4cafa061b82b0cc2872fe040688d59ecde3750d0#egg=card-0.3'
    ],
    scripts = ["opcgenerator"]
)

