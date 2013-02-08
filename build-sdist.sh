#!/bin/sh

echo "Compiling LESS files to CSS"
./build-less.sh

echo "Building model chart PDF (needs graphviz)"
cd testproject/
./manage.py wikiviz wiki --inheritance | dot -Tpdf -o ../model_chart_wiki.pdf
cd ..

echo "Building Python source distribution"
rm -Rf *egg-info/
python setup.py sdist

