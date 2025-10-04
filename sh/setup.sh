#!/bin/bash

git submodule update --init --recursive
conda env create -n smt_env boost_cpp gmp boost
conda activate smt_env
