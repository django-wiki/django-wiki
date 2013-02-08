#!/bin/sh

./build-less.sh
rm -Rf *egg-info/
python setup.py sdist
