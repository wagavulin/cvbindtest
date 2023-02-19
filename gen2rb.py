#!/usr/bin/env python

import json
import os
import re
import sys

import hdr_parser


def normalize_class_name(name):
    return re.sub(r"^cv\.", "", name).replace(".", "_")

def split_decl_name(name, namespaces):
    chunks = name.split('.')
    namespace = chunks[:-1]
    classes = []
    while namespace and '.'.join(namespace) not in namespaces:
        classes.insert(0, namespace.pop())
    return namespace, classes, chunks[-1]

class FuncInfo:
    def __init__(self, classname:str, name:str, cname:str, isconstructor:bool, namespace:str, is_static:bool):
        self.classname:str = classname
        self.name:str = name
        self.cname:str = cname
        self.isconstructor:bool = isconstructor
        self.namespace:str = namespace
        self.is_static:bool = is_static

    def dump(self, depth):
        indent = "  " * depth
        print(f"{indent}classname: {self.classname}")
        print(f"{indent}name: {self.name}")
        print(f"{indent}cname: {self.cname}")
        print(f"{indent}isconstructor: {self.isconstructor}")
        print(f"{indent}namespace: {self.namespace}")
        print(f"{indent}is_static: {self.is_static}")

class ClassInfo:
    def __init__(self, name, decl=None):
        self.cname = name.replace(".", "::")
        self.name = normalize_class_name(name)
        self.methods: dict[str, FuncInfo] = {}
        self.constructor: FuncInfo = None

    def dump(self, depth):
        indent = "  " * depth
        print(f"{indent}cname: {self.cname}")
        print(f"{indent}name: {self.name}")
        for i, method_name in enumerate(self.methods):
            print(f"{indent}methods[{i}] {method_name}")
            self.methods[method_name].dump(depth+1)

class Namespace:
    def __init__(self):
        self.funcs = {}

def gen(headers:list[str], out_dir:str):
    classes: dict[str, ClassInfo] = {}
    namespaces = {}
    parser = hdr_parser.CppHeaderParser(generate_umat_decls=False, generate_gpumat_decls=False)
    for hdr in headers:
        decls = parser.parse(hdr)
        hdr_fname = os.path.split(hdr)[1]
        hdr_stem = os.path.splitext(hdr_fname)[0]
        out_json_path = f"tmp-{hdr_stem}.json"
        with open(out_json_path, "w") as f:
            json.dump(decls, f, indent=2)
        for decl in decls:
            name = decl[0]
            if name.startswith("struct") or name.startswith("class"):
                cols = name.split(" ", 1)
                stype = cols[0] # "struct" or "class"
                name = cols[1]
                classinfo = ClassInfo(name, decl)
                if classinfo.name in classes:
                    print(f"Generator error: class {classinfo.name} (cname={classinfo.cname}) already exists")
                    exit(1)
                classes[classinfo.name] = classinfo
            else:
                namespace, classes_list, barename = split_decl_name(decl[0], parser.namespaces)
                #print(f"namespace: {namespace}, classes_list: {classes_list}, barename: {barename}")
                cname = "::".join(namespace+classes_list+[barename])
                name = barename
                classname = ''
                bareclassname = ''
                if classes_list:
                    classname = normalize_class_name('.'.join(namespace+classes_list))
                    bareclassname = classes_list[-1]
                namespace_str = '.'.join(namespace)
                isconstructor = name == bareclassname
                is_static = False
                if isconstructor:
                    name = "_".join(classes_list[:-1]+[name])
                #print(f"  name: {name}, cname: {cname}, bareclassname: {bareclassname}, namespace_str: {namespace_str}, isconstructor: {isconstructor}")
                if is_static:
                    pass
                else:
                    if classname and not isconstructor:
                        func_map = classes[classname].methods
                    else:
                        func_map = namespaces.setdefault(namespace_str, Namespace()).funcs
                    func = func_map.setdefault(name, FuncInfo(classname, name, cname, isconstructor, namespace_str, is_static))
                if classname and isconstructor:
                    classes[classname].constructor = func
    for i, class_name in enumerate(classes):
        print(f"classes{i} {class_name}")
        classes[class_name].dump(1)

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
