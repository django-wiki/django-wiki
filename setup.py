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
    return ["%s/%s*.%s" % (base_folder, "*/"*x, file_extension) if base_folder else "%s*.%s" % ("*/"*x, file_extension) for x in range(10)]

media_patterns = ( build_media_pattern("templates", "html") +
                   build_media_pattern("static", "js") +
                   build_media_pattern("static", "css") +
                   build_media_pattern("static", "png") +
                   build_media_pattern("static", "jpeg") +
                   build_media_pattern("static", "gif") +
                   build_media_pattern("", "rst")
)

packages = find_packages()

package_data = dict(
    (package_name, media_patterns)
    for package_name in packages
)

setup(
    name = "wiki",
    version = "0.0.1",
    author = "Benjamin Bach",
    author_email = "benjamin@overtag.dk",
    url = "http://www.django-wiki.org",
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
        'south',
        'django-mptt',
      ],
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
    package_data=package_data,
)
