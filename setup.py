import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
    'static/*.js',
    'static/*.css',
    'static/*/*.js',
    'static/*/*.css',
    'static/*/*/*.js',
    'static/*/*/*.css',
]

packages = find_packages()

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)

setup(
    name = "django-wiki",
    version = "0.0.1",
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
