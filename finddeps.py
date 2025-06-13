#!/usr/bin/env python

import json
import requests
from packaging.requirements import Requirement

base_packages = set()
pyodide_packages = open('pyodide-packages.txt').readlines()
for p in pyodide_packages:
    base_packages.add(p.strip())

def get_package_deps(package_name):
    dependencies = set()
    pypi_url = f'https://pypi.org/pypi/{package_name}/json'
    try:
        package_metadata = requests.get(pypi_url).json()
        requires_dist = package_metadata['info']['requires_dist']
        for dep in requires_dist:
            req = Requirement(dep)
            if not req.marker:
                dependencies.add(req.name)
    except Exception as e:
        pass
    return dependencies

def get_all_package_deps_tree(package_name, tree, base_packages):
    if package_name in tree or package_name in base_packages:
        return
    tree[package_name] = get_package_deps(package_name).difference(base_packages)
    if tree[package_name]:
        for dep in tree[package_name]:
            get_all_package_deps_tree(dep, tree, base_packages)

def get_foundation_deps(package_name, tree, base_packages):
    deps = get_package_deps(package_name)
    tree['other_deps'] = deps.difference(base_packages)
    tree['pyodide_deps'] = deps.intersection(base_packages)

if __name__ == '__main__':

    import sys
    import pprint

    if not len(sys.argv) >= 2:
        print('Usage: ./finddeps.py <package name>')
        sys.exit(1)
    root_package = sys.argv[-1]
    tree = {}
    if len(sys.argv) == 2:
        get_all_package_deps_tree(root_package, tree, base_packages)
    else:
        get_foundation_deps(root_package, tree, base_packages)
    pretty_print = pprint.PrettyPrinter()
    pretty_print.pprint(tree)
    if len(sys.argv) != 2:
        if tree['other_deps'] or tree['pyodide_deps']:
            all_deps = tree['other_deps'].union(tree['pyodide_deps'])
            print('requirements:')
            print('  run:')
            for dep in all_deps:
                print(f'    - {dep}')
