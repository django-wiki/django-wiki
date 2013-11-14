#!/bin/bash

set -e

# Ensure we're in the right directory
cd "$(dirname "$0")"

CHANGELOG="CHANGELOG.md"

echo "Creating CHANGELOG.md"
echo "Latest Changes" > $CHANGELOG
echo "==============" >> $CHANGELOG
echo "Compiled on: `date`" >> $CHANGELOG
echo "\nThis file is auto-generated upon every new release. To review the latest commits in the master branch, please refer to: https://github.com/benjaoming/django-wiki/commits/master"
echo "" >> $CHANGELOG
git log --graph --pretty=format:'%h -%d %s (%cr) <%an>' --abbrev-commit | sed "s/^/    /" >> $CHANGELOG

echo "Compiling LESS files to CSS..."
./build-less.sh

echo "Building docs..."
cd docs
make html
cd ..

echo "Building model chart PDF (needs graphviz)..."
cd testproject/
./manage.py wikiviz wiki --inheritance | dot -Tpdf -o ../model_chart_wiki.pdf
cd ..

echo "Building Python source distribution..."
rm -Rf *egg-info/
python setup.py sdist

