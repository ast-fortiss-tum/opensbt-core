#!/bin/bash

# cleanup existing build
if [ -d "dist" ]; then
    rm dist/*
fi

python -m build

# twine upload --repository testpypi dist/*

twine upload dist/*