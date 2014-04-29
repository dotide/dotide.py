#!/usr/bin/env python

from distutils.core import setup


setup(
    name='dotide',
    version='1.0.0',
    description='Official Dotide Python SDK',
    license='MIT',
    packages=['dotide'],
    install_requires=['requests'],
    tests_require=['mock'],
)
