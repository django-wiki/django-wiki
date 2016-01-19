#!/bin/bash

set -e

# Ensure we're in the right directory
cd "$(dirname "$0")"

CHANGELOG="HISTORY.rst"

echo "Creating HISTORY.rst"
echo "Latest Changes" > $CHANGELOG
echo "==============" >> $CHANGELOG
echo "" >> $CHANGELOG
echo "This file is auto-generated upon every new release. To review the latest commits in the master branch, please refer to: https://github.com/django-wiki/django-wiki/commits/master" >> $CHANGELOG
echo "" >> $CHANGELOG
echo "Compiled on: `date`::" >> $CHANGELOG
echo "" >> $CHANGELOG
git log --graph --pretty=format:'%h -%d %s (%cr) <%an>' --abbrev-commit | sed "s/^/    /" >> $CHANGELOG

echo "Compiling LESS files to CSS..."
./build-less.sh

#echo "Building docs..."
#cd docs
#make html
#cd ..

echo "Building Python source distribution..."
rm -Rf *egg-info/
python setup.py sdist

echo "OK, done. But ensure that you have pypandoc installed so the README.rst file is made for PyPi.. otherwise rerun."

echo "Now run python setup.py sdist upload"

