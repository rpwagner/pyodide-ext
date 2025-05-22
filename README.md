# `pyodide-ext`: Extending Pyodide

1. [Overview](#overview)
    1. [Why Use This?](#why-use-this)
    1. [Implementation](#implementation)
    1. [Limitations and Building a Full Stack](#limitations-and-building-a-full-stack)
1. [Generating a New Repository](#generating-a-new-repository)
1. [Configure and Build GitHub Pages](#configure-and-build-github-pages)
1. [Adding Packages](#adding-packages)
    1. [Example: PyJWT](#example-pyjwt)
    1. [Adding Packages from PyPI](#adding-packages-from-pypi)
    1. [Testing the Pyodide Distribution](#testing-the-pyodide-distribution)
    1. [Adding Your Own Package](#adding-your-own-package)
1. [Build All the Packages](#build-all-the-packages)
1. [Using the Pyodide Distribution](#using-the-pyodide-distribution)

## Overview

This is a [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) used to create a custom [Pyodide](https://pyodide.org/) distribution with additional packages. The motivation for this is to build interactive [JupyterLite](http://jupyterlite.readthedocs.io/) sites, but this distribution can be used for whatever you need. Also, the process leverages resources provided by [GitHub Free for personal accounts](https://docs.github.com/en/get-started/learning-about-github/githubs-plans#github-free-for-personal-accounts) making it widely accessible to many users.

### Why Use This?

The base Pyodide distribution [includes over 250 pacakges](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) beyond those in the [Python Standard Library](https://docs.python.org/3/library/index.html). However, your project may need packages that aren't yet included in Pyodide. This repository is intended to help you build a custom distribution of Pyodide with packages from [PyPI](https://pypi.org) and your own packages that may only be available as source code.

This is very helpful when supporting a JupyterLite environment. Otherwise, users are required to use [`micropip.install()`](https://pyodide.org/en/stable/usage/loading-packages.html) in their notebooks to install requirements before importing them. This makes notebooks less portable and can be a challenge for users unfamiliar with Pyodide. There is also an example in this repository of how to [add your own package](#adding-your-own-package) to make it easier to incorporate your own code without publishing it to PyPI. 

### Implementation

This repository uses its Build and Deploy GitHub Actions workflow ([`deploy.yaml`](.github/workflows/deploy.yaml)  to build a custom Pyodide distribution by cloning the latest stable version of Pyodide, adding in the additional package definition files from this repository, building the required packages, and deploying the resulting Pyodide distribution to GitHub Pages. By default, the workflow only builds the [minimum required Pyodide packages](https://pyodide.org/en/stable/development/building-from-sources.html#partial-builds) (`tag:core`), plus the ones defined in this repository. You can update [`deploy.yaml`](.github/workflows/deploy.yaml) to build additional packages by default (e.g., `tag:min-scipy-stack`).

The [`deploy.yaml`](.github/workflows/deploy.yaml) workflow definition file is derived from the Pyodide [`main`](https://github.com/pyodide/pyodide/blob/main/.github/workflows/main.yml) workflow, and currently this template is pinned Pyodide version 0.27.6. You can verify this by checking around [line 35 of `deploy.yaml`](.github/workflows/deploy.yaml#L35):
```yaml
      - uses: actions/checkout@v4
        with:
          repository: 'pyodide/pyodide'
          ref: '0.27.6'
          submodules: 'recursive'
```
The workflow may need be modified for future Pyodide releases.

### Limitations and Building a Full Stack

By default, this repository is configured to build a subset of the [available packages in Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) to save time during the build process. When you've finished developing the build process for your custom packages, you can change what packages are built by default, or run a workflow to build all of the packages you need. See the section [Build All the Packages](#build-all-the-packages).

## Generating a New Repository

Click the "Use this repository" button on the top right of this repo page and select "Create a new repository".

<img src="./img/use-template.png" width="25%" height="25%" style='border:2px solid #555'>

These instructions apply to [`https://github.com/rpwagner/pyodide-ext`](https://github.com/rpwagner/pyodide-ext). If this is a repository generated from the original, it may not be a template, so you will need to fork it or clone it to reuse it. To generate your own repository based on this one, you can follow [GitHub's instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).

Some notes:
- Make sure you create your new repository under an account (likely your personal one) where you can enable GitHub Pages.
- You can give your new repository a different name. These instructions will assume that you named it `pyodide-ext`.

## Configure and Build GitHub Pages

This repository uses a [GitHub Actions workflow](https://docs.github.com/en/actions/writing-workflows/about-workflows) to build a Pyodide distribution and to deploy that distribution to GitHub Pages. First, follow the GitHub instructions to enable [building the distribution using the GitHub Actions workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow) on your new repository.

If you see build work and deploy fail, double check this.

---

After you enable this, go to the "Actions" tab on your repository:

<img src="./img/repo-action-tab.png" width="50%" height="50%" style='border:2px solid #555'>

---

Click on the "Build and Deploy" button below the list of "All workflows":

<img src="./img/build-and-deploy.png" width="50%" height="50%" style='border:2px solid #555'>

---

On the right, click on the "Run workflow" button, and in the dropdown, click on the the next "Run workflow" button. You don't need to change any of the settings at this time.

<img src="./img/run-workflow.png" width="50%" height="50%" style='border:2px solid #555'>

---

The build process will take about 15 minutes. You can monitor the status by looking at the workflow run under the "Actions" tab. This build process will happen every time you make a commit to your repository, either directly or via a pull request. Sometimes you don't want to cause another build to happen and you can [cancel the workflow](https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/canceling-a-workflow).

If you look into the build logs for the workflow run, you can the list of packages being built under the `build Pyodide with packages` step. Since this is the first build, it represents the packages built as part of the `tag:core` list, plus PyJWT.
```
Building the following packages: Jinja2, MarkupSafe, PyJWT, atomicwrites, attrs,
buffer-test, cffi, cpp-exceptions-test, cpp-exceptions-test2, cryptography,     
exceptiongroup, fpcast-test, hashlib, iniconfig, liblzma, lzma, micropip,       
more-itertools, openssl, packaging, pluggy, py, pycparser, pydecimal,           
pydoc_data, pyparsing, pytest, pytest-asyncio, pytz, regex, setuptools,         
sharedlib-test, sharedlib-test-py, six, sqlite3, ssl, tblib, and test
```

Once the workflow completes, you can test the distribution by going to your GitHub Pages site at: `https://{github-username}.github.io/pyodide-ext/`. There will be a landing page with a link to the Pyodide REPL console for your new distribution.

---

You might find it convenient to add a link to your GitHub Pages site to your repository's main page. You can do this by clicking on the "About" setting on the main page:

<img src="./img/repo-about.png" width="50%" height="50%" style='border:2px solid #555'>

And then checking the box "Use your GitHub Pages website".

<img src="./img/use-pages-site.png" width="50%" height="50%" style='border:2px solid #555'>

## Adding Packages

Pyodide packages are [defined by `meta.yaml` files](https://pyodide.org/en/stable/development/new-packages.html#creating-the-meta-yaml-file) that proivde URLs for the source code, lists of dependencies, build instructions, etc. For basic pure-Python packages, these files can be fairly minimal and [created programmatically](https://pyodide.org/en/stable/development/meta-yaml.html#meta-yaml-spec).  

One complication to keep in mind is that you will need to add all of the dependencies for your package, except for those in the [Python Standard Library](https://docs.python.org/3/library/index.html) or already [included with Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html). The `finddeps.py` script described below can help identify the needed dependencies.

The Pyodide documentation has detailed instructions on [how to add packages](https://pyodide.org/en/stable/development/new-packages.html). This also includes the best recommendation, which is to look at packages that have already been ported to Pyodide in [the main repoistory's packages folder](https://github.com/pyodide/pyodide/tree/main/packages). The method used in this this repository is not the only way to add packages (see the [Pyodide "Loading packages" documentation](https://pyodide.org/en/stable/usage/loading-packages.html)). You can directly install many packages using `micropip.install()`, or build packages in or out of the main Pyodide tree. The approach in this repository is to avoid using `micropip.install()` so that Jupyter notebooks and Python modules can remain portable without needing to check the runtime environment. However, you may find it easier to develop and test the build process for a given package and its dependencies by using a local development process and then adding the package definition (`meta.yaml`, patches, etc.) into this repository when it's working as expected.

Adding a new package and rebuilding the distribution uses these steps:
1. Define a new package by creating a new `meta.yaml` file in [`packages`](./packages), under `packages/{package-name}/meta.yaml`.
1. Add any patch files or tests under `packages/{package-name}/`, making sure they're referenced in `meta.yaml`.
1. Update the Build and Deploy workflow to include the new package in the default build.
1. Commit the new package and updated workflow file to the repository.
1. Monitor the workflow run's progress and build status.
1. Test the updated Pyodide distribution. ([jump to section](#testing-the-pyodide-distribution)

### Example: PyJWT

A `meta.yaml` definition file for [PyJWT](https://pyjwt.readthedocs.io/en/stable/) is included in this repository at [`packages/PyJWT/meta.yaml`](packages/PyJWT/meta.yaml). Here is the file's contents:

```yaml
package:
  name: PyJWT
  version: 2.10.1
  top-level:
    - jwt

source:
  url: https://files.pythonhosted.org/packages/py3/p/pyjwt/PyJWT-2.10.1-py3-none-any.whl
  sha256: dcdd193e30abefd5debf142f9adfcdd2b58004e644f25406ffaebd50bd98dacb

requirements:
  run:
    - cryptography
    - ssl

about:
  home: https://github.com/jpadilla/pyjwt
  PyPI: https://pypi.org/project/PyJWT
  summary: JSON Web Token implementation in Python
  license: MIT

extra:
  recipe-maintainers:
    - rpwagner
```

As mentioned above, these `meta.yaml` follow a [specification](https://pyodide.org/en/stable/development/meta-yaml.html#meta-yaml-spec) which is based on the Conda packaging specification. Below, you'll see a basic version can be created programmatically, and which may be sufficient for many packages. Looking in the [`deploy.yaml`](.github/workflows/deploy.yaml) file you will see a couple of places with the text `'tag:core,PyJWT'`, which will tell the Pyodide build process to add PyJWT to the list of packages. The requirements list in the `meta.yaml` definition also ensure that the necessary dependencies also get built.

### Adding Packages from PyPI

This is an example of how to add a package that is being distributed via PyPI. The main advantage of this process is that it creates the `meta.yaml` file for you. This process can also be adapted to other packages where the source code is available as an archive (e.g., a `.tar.gz` or `.zip` file).

---

Clone your repository and change into its directory

```shell
$ git clone https://github.com/{github-username}/pyodide-ext.git
$ cd pyodide-ext
```

---

Create a virtual Python environment. This is not strictly necessary, just a recommended practice.

```shell
$ python -m venv venv
$ source venv/bin/activate
(venv) $
```

---

Install `pyodide-build` and other requirement.

```shell
(venv) $ pip install -r requirements.txt
```

---

Check whether or not you need to build any additional packages. The script `finddeps.py` will list all of the dependendencies for a given package that aren't available in Pyodide or the Python Standard Library. *N.B.* The script is extremely basic and does not check the dependencies of any extras. This may miss packages necessary for building or the feature you're interested in.

You call the script via: `./finddeps.py {package-name}`.

For example, here is the result for the [Seaborn](https://seaborn.pydata.org) data visualization library.
```shell
(venv) $ ./finddeps.py seaborn
{'seaborn': set()}

```

`finddeps.py` prints out a JSON dictionary, where each key is a package name and the values are sets of package names of the dependencies for the given key. In this case, all of Seaborn's required dependencies (`numpy`, `pandas`, and `matplotlib`) are already available in Pyodide. 

---

If we look at [`contextily`](https://contextily.readthedocs.io/), a Python tool for retrieving tile maps, we find there are several additional packages we would need to define and build before we could use `contextily` in Pyodide.
```shell
(venv) $ ./finddeps.py contextily
{'contextily': {'geopy', 'mercantile'},
 'geographiclib': set(),
 'geopy': {'geographiclib'},
 'mercantile': set()}
```
Here's a graph representing these dependencies.

```mermaid
graph TD
  A(contextily) --> B(geopy)
  A --> C(mercantile)
  B --> D(geographiclib)
```
In this case, we would need to build `mercantile` and `geographiclib` (we can build them in either order), then `geopy` since it depends on `geographiclib`, before we can build `contextily`. 

---

To get started, we can use the `pyodide-build` tool installed as part of the `requirements.txt` to create a [skeleton yaml file](https://pyodide.org/en/stable/development/new-packages.html#creating-the-meta-yaml-file) for our packages.

```shell
(venv) $ pyodide skeleton pypi <package name>
```

Using Seaborn as the example
```shell
$ pyodide skeleton pypi seaborn       
Creating meta.yaml package for seaborn                                                                                                           
packages/seaborn/meta.yaml 11ms
Output written to /home/username/pyodide-ext/packages/seaborn/meta.yaml
```

This produces this YAML file
```yaml
package:
  name: seaborn
  version: 0.13.2
  top-level:
    - seaborn
source:
  url: https://files.pythonhosted.org/packages/py3/s/seaborn/seaborn-0.13.2-py3-none-any.whl
  sha256: 636f8336facf092165e27924f223d3c62ca560b1f2bb5dff7ab7fad265361987
about:
  home: null
  PyPI: https://pypi.org/project/seaborn
  summary: Statistical data visualization
  license: null
extra:
  recipe-maintainers:
    - PUT_YOUR_GITHUB_USERNAME_HERE
```

Looking at the Seaborn source code, we can fill in a few things. Most importantly, the run time dependencies. Specifying these ensures that they will be built if Seaborn is requested, and they will be loaded (and [installed](https://pyodide.org/en/stable/usage/loading-packages.html#loading-packages)) when Seaborn is imported.
```yaml
package:
  name: seaborn
  version: 0.13.2
  top-level:
    - seaborn
source:
  url: https://files.pythonhosted.org/packages/py3/s/seaborn/seaborn-0.13.2-py3-none-any.whl
  sha256: 636f8336facf092165e27924f223d3c62ca560b1f2bb5dff7ab7fad265361987
requirements:
  run:
    - numpy
    - pandas
    - matplotlib
about:
  home: https://seaborn.pydata.org
  PyPI: https://pypi.org/project/seaborn
  summary: Statistical data visualization
  license: BSD-3-Clause
extra:
  recipe-maintainers:
    - {github-username}
```

Seaborn has extras, so anything provided by its [optional dependencies](https://seaborn.pydata.org/installing.html#optional-dependencies) won't be available unless those packages are loaded by another route.

---

Now that the new package is defined, it needs to be added to the list of default packages to build. There are two places in [`deploy.yaml`](./.github/workflows/deploy.yaml) where the defualt is defined, the dispatch input and the environment. (This needs to be improved and provide a single point of truth.)
```yaml
  workflow_dispatch:
    inputs:
      pyodide_packages:
        description: 'Pyodide packages to build, will set PYODIDE_PACKAGES'
        required: true
        default: 'tag:core,PyJWT'
        type: string
...
    env:
      EMSDK_NUM_CORES: 2
      EMCC_CORES: 2
      PYODIDE_JOBS: 2
      CCACHE_DIR: /tmp/ccache
      PYODIDE_PACKAGES: ${{ inputs.pyodide_packages || 'tag:core,PyJWT' }}
```

This file needs to update this to add Seaborn alongside PyJWT.
```yaml
  workflow_dispatch:
    inputs:
      pyodide_packages:
        description: 'Pyodide packages to build, will set PYODIDE_PACKAGES'
        required: true
        default: 'tag:core,PyJWT,seaborn'
        type: string
...
    env:
      EMSDK_NUM_CORES: 2
      EMCC_CORES: 2
      PYODIDE_JOBS: 2
      CCACHE_DIR: /tmp/ccache
      PYODIDE_PACKAGES: ${{ inputs.pyodide_packages || 'tag:core,PyJWT,seaborn' }}
```

---

At this point, the changes can be added, committed, and pushed to the repository
```shell
(venv) $ git add packages/seaborn/meta.yaml .github/workflows/deploy.yaml
(venv) $ git commit -m 'added seaborn'
(venv) $ git push origin main
```

This will trigger a build, which can be monitored by going to the Actions tab and clicking on the "added seaborn" workflow run.

<img src="./img/added-seaborn.png" width="75%" height="75%" style='border:2px solid #555'>

Looking at the workflow logs under the `build Pyodide with packages` step we can see that `numpy`, `matplotlib`, and `pandas` are now included in the build, in addition to Seaborn. These new packages will add quite a bit to the build time.
```
Building the following packages: Jinja2, MarkupSafe, Pillow, PyJWT,             
atomicwrites, attrs, buffer-test, cffi, contourpy, cpp-exceptions-test,         
cpp-exceptions-test2, cryptography, cycler, exceptiongroup, fonttools,          
fpcast-test, hashlib, iniconfig, kiwisolver, liblzma, libtiff, libwebp, lzma,   
matplotlib, matplotlib-pyodide, micropip, more-itertools, numpy, openssl,       
packaging, pandas, pluggy, py, pycparser, pydecimal, pydoc_data, pyparsing,     
pytest, pytest-asyncio, python-dateutil, pytz, regex, seaborn, setuptools,      
sharedlib-test, sharedlib-test-py, six, sqlite3, ssl, tblib, and test
```

### Testing the Pyodide Distribution

Test the build in the REPL console at: `https://{github-username}.github.io/pyodide-ext/console.html`. May need to clear your website data reguarly, in case the REPL files are being cached in your browser.

At a minimum, import the package to ensure the dependencies are declared correctly. 

```python
Welcome to the Pyodide 0.27.5 terminal emulator 🐍
Python 3.12.7 (main, May  5 2025 08:30:39) on WebAssembly/Emscripten
Type "help", "copyright", "credits" or "license" for more information.
>>> import seaborn
Matplotlib is building the font cache; this may take a moment.
>>> 
```
Everything loads correctly. When this distribution is used in a JupyterLite site, the plotting capabilities of Seaborn can be tested.

### Adding Your Own Package

In addition to building packages from source code hosted on PyPI and other sites, you can include your own package in this repository. This is a convenient way to gather modules and script that you use frequently, but haven't published to PyPI. To demonstrate this, in the `packages/` folder [`extpackage`](./packages/extpackage) is a minimal Python package, with the source code included in the folder rather than referenced in the `meta.yaml` file.

In the `meta.yaml` for `extpackage`, there `source` is specified using a `path`, rather than a `url` field. Here the path points to the `source` folder in the `packages/extpackage/` folder, i.e., `packages/extpackage/source/`.

`packages/extpackage/meta.yaml`:
```yaml
package:
  name: extpackage
  version: 0.0.1
  top-level:
    - extpackage

source:
  path: source

about:
  home: https://github.com/rpwagner/pyodide-ext
  summary: A sample Python package
  license: BSD-3-Clause

extra:
  recipe-maintainers:
    - rpwagner
```

Including the source code in `packages/` can lead to a deep folder hierarchy that requires some tracking. The `source` subfolder contains the contents usually expected in a Python package, including its `pyproject.toml` file and a `src` folder. The `src` folder contains the toplevel `expackage` folder that will eventually be imported, and the two Python files that provide a minimal text of functionality.

`packages/extpackage/source/`:
```
pyproject.toml
src

./src:
extpackage

./src/extpackage:
__init__.py
dog.py
```

`__init__.py`:
```python
from .dog import cat
```

`dog.py`:
```python
def cat():
    """Example function"""
    print('mouse')
```

---

To build `extpackage`, we need to add it to the list of packages in [`deploy.yaml`](./.github/workflows/deploy.yaml). Assuming that you already added Seaborn, we can add `extpackages` after it.

```yaml
  workflow_dispatch:
    inputs:
      pyodide_packages:
        description: 'Pyodide packages to build, will set PYODIDE_PACKAGES'
        required: true
        default: 'tag:core,PyJWT,seaborn,extpackage'
        type: string
...
    env:
      EMSDK_NUM_CORES: 2
      EMCC_CORES: 2
      PYODIDE_JOBS: 2
      CCACHE_DIR: /tmp/ccache
      PYODIDE_PACKAGES: ${{ inputs.pyodide_packages || 'tag:core,PyJWT,seaborn,extpackage' }}
```

After you make this change you'll need to go through the same `git add`, `git commit`, etc., steps as in the previous section and make sure the workflow completes successfully.

---

To test `extpackage`, we can go to the console, import the package and execute the one included function. Remember that you may need to clear your browser's cache of your GitHub Pages subdomain to make sure it has the correct list of available packages.

```python
Welcome to the Pyodide 0.27.5 terminal emulator 🐍
Python 3.12.7 (main, May  7 2025 05:44:43) on WebAssembly/Emscripten
Type "help", "copyright", "credits" or "license" for more information.
>>> import extpackage
>>> help(extpackage.cat)
Help on function cat in module extpackage.dog:
cat()
    Example function
>>> extpackage.cat()
mouse
>>> 
```

---

This process can also be used to build packages that are available source on GitHub. Here are the basic steps:

1. Create a new folder and `meta.yaml` file in `packages` similar to the previous example.
1. Update [`deploy.yaml`](./.github/workflows/deploy.yaml) to clone the other repository into an unused path using the [checkout action](https://github.com/actions/checkout). Look at how portions of this repository are cloned using a sparse checkout for an example.
1. Copy the source of the other repository into the `source` folder of the new package.

## Build All the Packages

As described in [Limitations and Building a Full Stack](#limitations-and-building-a-full-stack), the set of packages built by default based [`deploy.yaml`](./.github/workflows/deploy.yaml) are a small subset of what's available to minimize the development time to add new packages. When that stage is complete, you will probably want to build either all of the packages available (including the new ones defined) or, the scientific computing stack, which includes Numpy, Matplotlib, and SciPy (`tag:min-scipy-stack`, plus your new packages, e.g., `tag:min-scipy-stack,seaborn`).

My suggestion is to set the default to build all of the packages, so that when you make a change you don't inadvertently build just a subset of what you need. You can also use a fork of your repository for testing, but I won't go into that here.

To build all of the packages in both the Pyodide distribution and your new ones, change the text in [`deploy.yaml`](./.github/workflows/deploy.yaml) like `'tag:core,PyJWT,seaborn'` to `'*'`. Note that the build will likely take a few hours (see [this recent workflow run](https://github.com/rpwagner/pyodide-ext/actions/runs/15179839466)).

```yaml
  workflow_dispatch:
    inputs:
      pyodide_packages:
        description: 'Pyodide packages to build, will set PYODIDE_PACKAGES'
        required: true
        default: '*'
        type: string
...
    env:
      EMSDK_NUM_CORES: 2
      EMCC_CORES: 2
      PYODIDE_JOBS: 2
      CCACHE_DIR: /tmp/ccache
      PYODIDE_PACKAGES: ${{ inputs.pyodide_packages || '*' }}
```

You can still build a reduced set of packages when needed by running the workflow manually and specifying which packages as described in [Configure and Build GitHub Pages](#configure-and-build-github-pages).

## Using the Pyodide Distribution

The Pyodide documentation describes [how to use Pyodide](https://pyodide.org/en/stable/usage/index.html) in a web browser or environments like Node.js. For those use cases and to [use it in JupyterLite](https://jupyterlite.readthedocs.io/en/stable/howto/pyodide/pyodide.html#using-a-custom-pyodide-distribution), you will usually point to the `pyodide.js` file in the distribution. This can be fund at:

`https://{github-username}.github.io/pyodide-ext/pyodide.js`
