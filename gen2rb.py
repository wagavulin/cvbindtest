#!/usr/bin/env python

import os
import sys
import hdr_parser

def gen(headers:list[str], out_dir:str):
    parser = hdr_parser.CppHeaderParser(generate_umat_decls=False, generate_gpumat_decls=False)
    for hdr in headers:
        decls = parser.parse(hdr)
        for decl in decls:
            name = decl[0]
            if name.startswith("struct") or name.startswith("class"):
                cols = name.split(" ", 1)
                stype = cols[0] # "struct" or "class"
                name = cols[1]

headers_txt = "./headers.txt"
if len(sys.argv) == 2:
    headers_txt = sys.argv[1]
headers = []
with open(headers_txt) as f:
    for line in f:
        line = line.strip()
        if not line.startswith("#"):
            headers.append(line)
dstdir = "./autogen"
os.makedirs(dstdir, exist_ok=True)
gen(headers, dstdir)
