#!/bin/sh
# 4-pass build (booklet 13.4). Usage: sh build.sh
# v1.3.0: each pass has a timeout so a hung pass fails fast instead of blocking;
# if a pass is killed, delete report.aux/.out/.toc before rebuilding (they may be truncated).
cd "$(dirname "$0")"
L="timeout 300 lualatex -interaction=nonstopmode -jobname=report main.tex"
$L > work/build_pass1.txt 2>&1
biber report > work/build_biber.txt 2>&1
$L > work/build_pass2.txt 2>&1
$L > work/build_pass3.txt 2>&1
tail -2 work/build_pass3.txt
