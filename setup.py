#!/usr/bin/env python

from distutils.core import setup


setup(
    name='dotide',
    version='0.0.1',
    description='Official Dotide Python SDK',
    license='MIT',
    packages=['dotide'],
    install_requires=['requests'],
    tests_require=['nose', 'mock'],
)
