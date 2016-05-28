#!/usr/bin/env python

from setuptools import setup

setup(
    name="sshrpc",
    version="0.2",
    author="Jakub Szafrański",
    description="A very simple RPC client/server working only over SSH",
    install_requires=['jsonpickle'],
    packages=['sshrpc']
)
