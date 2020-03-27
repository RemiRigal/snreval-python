#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages


setup(
    name='snreval',
    version='1.2',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='This repository provides a small Python wrapper for the Matlab tool SNR Eval provided by Labrosa: https://labrosa.ee.columbia.edu/projects/snreval',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['numpy', 'pandas'],
    url='https://github.com/RemiRigal/snreval-python',
    author='Rémi Rigal',
    author_email='remi.rigal@ensta-bretagne.org'
)
