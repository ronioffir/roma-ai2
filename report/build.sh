#!/bin/sh
# 4-pass build (booklet 13.4). Usage: sh build.sh
cd "$(dirname "$0")"
lualatex -interaction=nonstopmode -jobname=report main.tex > work/build_pass1.txt 2>&1
biber report > work/build_biber.txt 2>&1
lualatex -interaction=nonstopmode -jobname=report main.tex > work/build_pass2.txt 2>&1
lualatex -interaction=nonstopmode -jobname=report main.tex > work/build_pass3.txt 2>&1
tail -2 work/build_pass3.txt
