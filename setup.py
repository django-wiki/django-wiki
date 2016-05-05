#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from sys import version_info as PYTHON_VERSION

from setuptools import find_packages, setup

from wiki import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def get_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requirements = [
    "Django>=1.5",
    "Pillow",
    "django-nyt>=0.9.7.2,<1.0",
    "six",
]


# Requirements that depend on Django version: South and sorl-thumbnail
try:
    from django import VERSION as DJANGO_VERSION
except ImportError:
    # No Django so assuming that one will get installed, but we don't know which
    # one.
    # We will assume it's a very recent one and base the requirements on that...
    requirements.append("sorl-thumbnail>=12")
    # 0.6.1 broken: https://github.com/django-mptt/django-mptt/issues/316
    requirements.append("django-mptt>=0.8")
    requirements.append("django-sekizai>=0.9")
else:
    if DJANGO_VERSION < (1, 7):
        requirements.append("South>=1.0.1")
        requirements.append("django-mptt>=0.7.1,<0.8")
        requirements.append("django-sekizai<0.9")
    elif DJANGO_VERSION < (1, 8):
        # Fixes
        # AttributeError: 'URLPath' object has no attribute 'get_deferred_fields'
        requirements.append("django-mptt>=0.7.1,<0.8")
        requirements.append("django-sekizai>=0.9")
    else:
        # Latest django-mptt only works for Django 1.8+
        requirements.append("django-mptt>=0.8,<0.9")
        requirements.append("django-sekizai>=0.9")
    if DJANGO_VERSION < (1, 5):
        # For Django 1.4, use sorl-thumbnail<11.12.1:
        # https://github.com/mariocesar/sorl-thumbnail/issues/255
        requirements.append("sorl-thumbnail<11.12.1")
    else:
        requirements.append("sorl-thumbnail>=12,<13")

if PYTHON_VERSION < (2, 7):
    # For Python 2.6, use Markdown<2.5.0, see
    # https://github.com/waylan/Python-Markdown/issues/349
    requirements.append("Markdown>2.2.0,<2.5.0")
else:
    requirements.append("Markdown>2.2.0,<2.7")

packages = find_packages()


setup(
    name="wiki",
    version=__version__,
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    url="http://www.django-wiki.org",
    description="A wiki system written for the Django framework.",
    license="GPLv3",
    keywords="django wiki markdown",
    packages=find_packages(exclude=["testproject", "testproject.*"]),
    long_description=read('README'),
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
    test_suite='runtests',
)
