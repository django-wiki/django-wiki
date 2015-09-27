# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def build_media_pattern(base_folder, file_extension):
    return ["%s/%s*.%s" % (base_folder, "*/"*x, file_extension) for x in range(10)]

template_patterns = ( build_media_pattern("templates", "html") +
                      build_media_pattern("static", "js") +
                      build_media_pattern("static", "css") +
                      build_media_pattern("static", "png") + 
                      build_media_pattern("static", "jpeg") + 
                      build_media_pattern("static", "gif"))

packages = find_packages()

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)

setup(
    name = "django-wiki",
    version = "0.0.2",
    author = "Benjamin Bach",
    author_email = "benjamin@overtag.dk",
    description = ("A wiki system written for the Django framework."),
    license = "GPLv3",
    keywords = "django wiki markdown",
    packages=find_packages(exclude=["testproject","testproject.*"]),
    long_description=read('README.md'),
    zip_safe = False,
    install_requires=[
        'Django>=1.4',
        'markdown',
        'django-sekizai',
        'django-mptt',
      ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GPLv3',
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
    package_data=package_data,
)
