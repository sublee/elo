# -*- coding: utf-8 -*-
"""
Elo
~~~

An implementation of the Elo algorithm for Python. Elo is a rating system among
game players and it is used on many chess tournaments to rank.

.. sourcecode:: pycon

   >>> from elo import rate_1vs1
   >>> rate_1vs1(800, 1200)
   (809.091, 1190.909)

Links
`````

- `GitHub repository <http://github.com/sublee/elo/>`_
- `development version
  <http://github.com/sublee/elo/zipball/master#egg=elo-dev>`_

See Also
````````

- `Multiplayer Elo Calculator <http://elo.divergentinformatics.com/>`_
- `TrueSkill for Python <http://trueskill.org/>`_

"""
from __future__ import with_statement
import re
from setuptools import setup
from setuptools.command.test import test
import sys


# detect the current version
with open('elo.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead
def run_tests(self):
    pyc = re.compile(r'\.pyc|\$py\.class')
    test_file = pyc.sub('.py', __import__(self.test_suite).__file__)
    raise SystemExit(__import__('pytest').main([test_file]))
test.run_tests = run_tests


setup(
    name='elo',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='http://github.com/sublee/elo',
    description='A rating system for chess tournaments',
    long_description=__doc__,
    platforms='any',
    py_modules=['elo'],
    classifiers=['Development Status :: 1 - Planning',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.1',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Programming Language :: Python :: Implementation :: PyPy',
                 'Topic :: Games/Entertainment'],
    test_suite='elotests',
    tests_require=['pytest', 'almost'],
    use_2to3=(sys.version_info[0] >= 3),
)
