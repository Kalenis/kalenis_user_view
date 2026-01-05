#!/usr/bin/env python3
# This file is part of the user_view module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

import io
import os
import re
from configparser import ConfigParser
from setuptools import find_packages, setup

MODULE = 'user_view'
PREFIX = 'kalenis'
MODULE2PREFIX = {}


def read(fname):
    content = io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
    content = re.sub(
        r'(?m)^\.\. toctree::\r?\n((^$|^\s.*$)\r?\n)*', '', content)
    return content


def get_require_version(name):
    require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require


config = ConfigParser()
config.read_file(open(os.path.join(os.path.dirname(__file__), 'tryton.cfg')))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

url = 'https://www.kalenislims.com/'
download_url = 'https://github.com/Kalenis/kalenislims'

requires = []
for dep in info.get('depends', []):
    if re.match(r'^lims*', dep):
        continue
    if not re.match(r'(ir|res)(\W|$)', dep):
        module_name = '%s_%s' % (MODULE2PREFIX.get(dep, 'trytond'), dep)
        requires.append(get_require_version(module_name))
requires.append(get_require_version('trytond'))

tests_require = [get_require_version('proteus')]
for dep in info.get('extras_depend', []):
    module_name = '%s_%s' % (MODULE2PREFIX.get(dep, 'trytond'), dep)
    tests_require.append(get_require_version(module_name))

setup(name='%s_%s' % (PREFIX, MODULE),
    version=version,
    description='',
    long_description='',
    author='Kalenis',
    author_email='info@kalenislims.com',
    url=url,
    download_url=download_url,
    keywords='',
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=(
        ['trytond.modules.%s' % MODULE]
        + ['trytond.modules.%s.%s' % (MODULE, p) for p in find_packages()]
        ),
    package_data={
        'trytond.modules.%s' % MODULE: (info.get('xml', []) + [
            'tryton.cfg', 'view/*.xml', 'locale/*.po',
            ]),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 or later'
        ' (GPLv3+)',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering',
        ],
    license='GPL-3',
    python_requires='>=3.8',
    install_requires=requires,
    extras_require={
        'test': tests_require,
        },
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    )
