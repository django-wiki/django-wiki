#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os
import sys
from glob import glob

from setuptools import find_packages, setup

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'src')
)

# noqa
from wiki import __version__  # isort:skip  # noqa


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def get_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read_file(fname):
    """
    Read file and decode in py2k
    """
    if sys.version_info < (3,):
        return open(fname).read().decode("utf-8")
    return open(fname).read()


requirements = [
    "Django>=1.8,<1.12",
    "bleach>=1.5,<2",
    "Pillow",
    "django-nyt>=1.0b1",
    "six",
    "django-mptt>=0.8.6,<0.9",
    "django-sekizai>=0.10",
    "sorl-thumbnail>=12,<13",
    "Markdown>=2.6,<2.7",
]


setup(
    name="wiki",
    version=__version__,
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    url="http://www.django-wiki.org",
    description="A wiki system written for the Django framework.",
    license="GPLv3",
    keywords=["django", "wiki", "markdown"],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    long_description=read_file('README.rst'),
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
    test_suite='runtests',
)
