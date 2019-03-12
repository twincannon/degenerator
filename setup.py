#!/usr/bin/env python
from setuptools import setup

setup(
	name = 'degen',
	version = '0.0.0',
	packages = ['degen'],
	entry_points = {
		'console_scripts': [
			'degen = degen:main',
		],
	})