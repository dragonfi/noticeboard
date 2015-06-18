#!/bin/bash

python3 -m unittest discover
find . -iname '*.py' | entr python3 -m unittest discover
