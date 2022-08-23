#!/usr/bin/env python

from setuptools import setup

setup(name='zebra_filter',
      version="1.0",
      long_description="Zebra: Static and Dynamic Genome Cover Thresholds With Overlapping References",
      license="BSD",
      url='https://github.com/biocore/zebra_filter',
      packages=['zebra'],
      package_dir={'zebra': '.'}
)
