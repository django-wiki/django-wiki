#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from setuptools import setup, find_packages

from wiki import VERSION

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def get_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    return open(get_path(fname)).read()


requirements = [
    "Django>=1.4,<1.9",
    "django-sekizai>=0.8.1",
    "Pillow",
    "django-nyt>=0.9.7.2",
    # 0.6.1 broken: https://github.com/django-mptt/django-mptt/issues/316
    "django-mptt==0.7.1",
    "six",
]


dependency_links = [
    'https://github.com/ojii/django-sekizai/archive/master.zip#egg=django-sekizai-0.8.1',
]

# Requirements that depend on Django version: South and sorl-thumbnail
try:
    from django import VERSION as DJANGO_VERSION
except ImportError:
    # No Django so assuming that one will get installed, but we don't know which
    # one.
    # For Django 1.7, we don't need South at all, but installing it
    # doesn't harm anything (as long as it's not added to INSTALLED_APPS).
    # For Django <= 1.6, we need to ensure a recent South version,
    # so to be safe we include South here.
    requirements.append("South>=1.0.1")
    requirements.append("sorl-thumbnail>=11.12.1b")
else:
    if DJANGO_VERSION < (1, 7):
        requirements.append("South>=1.0.1")
    if DJANGO_VERSION < (1, 5):
        # For Django 1.4, use sorl-thumbnail<11.12.1:
        # https://github.com/mariocesar/sorl-thumbnail/issues/255
        requirements.append("sorl-thumbnail<11.12.1")
    else:
        requirements.append("sorl-thumbnail>=11.12.1b")

# Requirements that depend on Python version: Markdown
from sys import version_info as PYTHON_VERSION
if PYTHON_VERSION < (2, 7):
    # For Python 2.6, use Markdown<2.5.0, see
    # https://github.com/waylan/Python-Markdown/issues/349
    requirements.append("Markdown>2.2.0,<2.5.0")
else:
    requirements.append("Markdown>2.2.0")

packages = find_packages()


try:
    import pypandoc
    long_description = pypandoc.convert(get_path('README.md'), 'rst')
    long_description = long_description.split(
        '<!---Illegal PyPi RST data -->')[0]
    f = open(get_path('README.rst'), 'w')
    f.write(long_description)
    f.close()
except (IOError, ImportError):
    # No long description... but nevermind, it's only for PyPi uploads.
    long_description = ""

setup(
    name="wiki",
    version=VERSION,
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    url="http://www.django-wiki.org",
    description="A wiki system written for the Django framework.",
    license="GPLv3",
    keywords="django wiki markdown",
    packages=find_packages(exclude=["testproject", "testproject.*"]),
    # long_description=long_description,
    zip_safe=False,
    install_requires=requirements,
    dependency_links=dependency_links,
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

