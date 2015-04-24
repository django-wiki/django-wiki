#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os
from wiki import VERSION
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def get_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


def read(fname):
    return open(get_path(fname)).read()


requirements = [
    "Django>=1.4,<1.7",
    "django-sekizai>=0.7",
    "Pillow",
    "django-nyt>=0.9.4",
    "django-mptt==0.6.0", # 0.6.1 broken: https://github.com/django-mptt/django-mptt/issues/316
    "six",
    "",
]

# Requirements that depend on Django version: South and sorl-thumbnail
try:
    from django import VERSION as DJANGO_VERSION
except ImportError:
    # No django so assuming that a new one will get installed...
    # TODO/FIXME: Remove the South req line here when Django>=1.7 is accepted
    requirements.append("South>=0.8.4")
    requirements.append("sorl-thumbnail>=11.12.1b")
else:
    if DJANGO_VERSION < (1, 7):
        requirements.append("South>=0.8.4")
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
    requirements.append("Markdown>2.2.0,<2.6")

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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
)
