#!/usr/bin/env python

from setuptools import setup

setup(name='EnvComparison',
      version='0.1.5',
      description='Linux Environment Comparison Tool',
      url='https://github.com/adamar/EnvComparison',
      scripts=['compare.py'],
      packages=['EnvComparison'],
      install_requires=['paramiko','tornado']
     )
