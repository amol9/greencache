import ez_setup
ez_setup.use_setuptools()

import platform
import sys
from setuptools import setup, find_packages

from greencache.version import __version__


setup(	
	name			= 'greencache',
	version			= __version__,
	description		= 'A python library for various kinds of cache.',
	author			= 'Amol Umrale',
	author_email 		= 'babaiscool@gmail.com',
	url			= 'http://pypi.python.org/pypi/greencache/',
	packages		= find_packages(),
	include_package_data	= True,
	scripts			= ['ez_setup.py'],
	install_requires	= ['redlib>=1.5.7'],
	classifiers		= [
					'Development Status :: 4 - Beta',
					'Environment :: Console',
					'License :: OSI Approved :: MIT License',
					'Natural Language :: English',
					'Operating System :: Microsoft :: Windows',
					'Programming Language :: Python :: 3.4',
				]
)
