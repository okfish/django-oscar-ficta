#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import oscar_ficta

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = oscar_ficta.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-oscar-ficta',
    version=version,
    description="""Persona ficta management for Oscar E-commerce""",
    long_description=readme + '\n\n' + history,
    author='Oleg Rybkin aka Fish',
    author_email='okfish@yandex.ru',
    url='https://github.com/okfish/django-oscar-ficta',
    packages=[
        'oscar_ficta',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-oscar-ficta',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
