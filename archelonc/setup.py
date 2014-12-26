#!/usr/bin/env python
"""
Package installer for archelon client
"""

from setuptools import setup, find_packages


VERSION = __import__('archelonc').VERSION

with open('README.rst') as readme:
    README = readme.read()

setup(
    name='archelonc',
    version=VERSION,
    packages=find_packages(),
    package_data={},
    license='AGPLv3',
    author='Carson Gee',
    author_email='x@carsongee.com',
    url="http://github.com/carsongee/arcelon",
    description=("Client connected to archelonc for Web shell history"),
    long_description=README,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        ('License :: OSI Approved :: '
         'GNU Affero General Public License v3 (AGPLv3)'),
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'npyscreen',
        ],
    entry_points={'console_scripts': [
        'archelon = archelonc.command:search_form',
        'archelonw = archelonw.command:watcher',
    ]},
    zip_safe=True,
)