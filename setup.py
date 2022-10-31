#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from glob import glob

from setuptools import find_packages
from setuptools import setup

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# noqa
from wiki import __version__  # isort:skip  # noqa


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def get_path(fname):
    return os.path.join(os.path.dirname(__file__), fname)


install_requirements = [
    "Django>=2.1,<4.2",
    "bleach[css]>=5",
    "Pillow",
    "django-nyt>=1.2.2,<1.3",
    "django-mptt>=0.13,<0.15",
    "django-sekizai>=0.10",
    "sorl-thumbnail>=12.8,<13",
    "Markdown>=3.3,<3.4",
]

test_requirements = [
    "django-functest>=1.2,<1.6",
    "pytest>=6.2.5,<7.3",
    "pytest-django",
    "pytest-cov",
    "coverage",
    "codecov",
    "ddt",
    "pytest-pythonpath",
]

test_lint_requirements = [
    "flake8>=3.7,<5.1",
    # Somewhat pin black, such that older code bases can
    # be verified CI without linting them lots
    "black>=22.3.0,<22.11",
    "pre-commit",
]

setup_requirements = [
    "pytest-runner",
]

development_requirements = test_requirements + test_lint_requirements

extras_requirements = {
    "devel": development_requirements,
    "test": test_requirements,
    "testlint": test_lint_requirements,
    "transifex": ["transifex-client"],
}

setup(
    name="wiki",
    version=__version__,
    author="Benjamin Bach",
    author_email="benjamin@overtag.dk",
    url="http://www.django-wiki.org",
    description="A wiki system written for the Django framework.",
    license="GPLv3",
    keywords=["django", "wiki", "markdown"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")
    ],
    long_description=open("README.rst").read(),
    zip_safe=False,
    install_requires=install_requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    include_package_data=True,
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require=extras_requirements,
)
