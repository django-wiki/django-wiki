# -*- coding: utf-8 -*-
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

packages = find_packages()


try:
    import pypandoc
    long_description = pypandoc.convert(get_path('README.md'), 'rst')
    long_description = long_description.split('<!---Illegal PyPi RST data -->')[0]
    f = open(get_path('README.rst'), 'w')
    f.write(long_description)
    f.close()
except (IOError, ImportError):
    # No long description... but nevermind, it's only for PyPi uploads.
    long_description = ""

setup(
    name = "wiki",
    version = VERSION,
    author = "Benjamin Bach",
    author_email = "benjamin@overtag.dk",
    url = "http://www.django-wiki.org",
    description = "A wiki system written for the Django framework.",
    license = "GPLv3",
    keywords = "django wiki markdown",
    packages=find_packages(exclude=["testproject","testproject.*"]),
    #long_description=long_description,
    zip_safe=False,
    install_requires=read('requirements.txt').split("\n"),
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
