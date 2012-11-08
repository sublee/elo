# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='elo',
    version='0.0',
    license='BSD',
    author='Heungsub Lee',
    author_email='h' '@' 'subl.ee',
    url='http://github.com/sublee',
    description='Most famous skill rating system',
    platforms='any',
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    test_suite='elotests.suite',
    test_loader='attest:auto_reporter.test_loader',
    tests_require=['Attest'],
)
