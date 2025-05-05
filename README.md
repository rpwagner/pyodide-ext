# `pyodide-ext`: Extending Pyodide

This is a [template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) used to create a custom [Pyodide](https://pyodide.org/) distribution with additional packages. The motivation for this is to build interactive [JupyterLite](http://jupyterlite.readthedocs.io/) sites, but this distribution can be used for whatever you need.

The base Pyodide distribution [includes over 250 pacakges](https://pyodide.org/en/stable/usage/packages-in-pyodide.html) beyond those in the [Python Standard Library](https://docs.python.org/3/library/index.html). However, your project may need packages that aren't yet available, and this repository and its documentation can help you get things working in Pyodide. 

TODO: Mention something about being able to do this wihtin the free level of GitHub usage and the scaling available from GitHub Pages.

This repository uses its [Build and Deploy](.github/workflows/deploy.yaml) GitHub Actions workflow to build a custom Pyodide distribution by cloning the latest stable version of Pyodide, adding in the additional package definition files from this repository, building the required packages, and deploying the resulting Pyodide distribution to GitHub Pages. By default, the workflow only builds the [minimum required Pyodide packages](https://pyodide.org/en/stable/development/building-from-sources.html#partial-builds) (`tag:core`), plus the ones defined in this repository. You can update the [Build and Deploy workflow](.github/workflows/deploy.yaml) to build additional packages by default (e.g., `tag:min-scipy-stack`).

The [Build and Deploy](.github/workflows/deploy.yaml) workflow is derived from the Pyodide [`main`](https://github.com/pyodide/pyodide/blob/main/.github/workflows/main.yml) workflow, and currently this template is pinned Pyodide version 0.27.5. You can verify this by checking around [line 35 of Build and Deploy](.github/workflows/deploy.yaml#L35)
```yaml
      - uses: actions/checkout@v4
        with:
          repository: 'pyodide/pyodide'
          ref: '0.27.5'
          submodules: 'recursive'
```
The [Build and Deploy](.github/workflows/deploy.yaml) workflow may need be modified for future Pyodide releases.

To get started, the basic steps are:
1. Create a new GitHub repository using this template. ([jump to section](#generating-a-new-repository))
1. Configure GitHub Pages to build using the [Build and Deploy](.github/workflows/deploy.yaml) workflow. ([jump to section](#configure-and-build-github-pages))
1. Add new package folders and `meta.yaml` files in the [`packages/`](./packages/) folder. ([jump to section](#adding-packages))
1. Check the build status in the Actions tab.
1. Test the build in the REPL console at: `https://{your-github-username}.github.io/{repo-name}/console.html`.

## Generating a New Repository

These instructions apply to [`https://github.com/rpwagner/pyodide-ext`](https://github.com/rpwagner/pyodide-ext). If this is a repository generated from the original, it may not be a template, so you will need to fork it or clone it to reuse it. To generate your own repository based on this one, you can follow [GitHub's instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).

Some notes:
- Make sure you create your new repository under an account (likely your personal one) where you can enable GitHub Pages.
- You can give your new repository a different name. These instructions will assume that you named it `pyodide-ext`.

## Configure and Build GitHub Pages

This repository uses a [GitHub Actions workflow](https://docs.github.com/en/actions/writing-workflows/about-workflows) to build a Pyodide distribution and to deploy that distribution to GitHub Pages. First, follow the GitHub instructions to enable [building the distribution using the GitHub Actions workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow) on your new repository.

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

Once the workflow completes, you can test the distribution by going to your GitHub Pages site at: `https://{github-username}.github.io/{repo-name}/`. There will be a landing page with a link to the Pyodide REPL console for your new distribution.

---

You might find it convenient to add a link to your GitHub Pages site to your repository's main page. You can do this by clicking on the "About" setting on the main page:

<img src="./img/repo-about.png" width="50%" height="50%" style='border:2px solid #555'>

And then checking the box "Use your GitHub Pages website".

<img src="./img/use-pages-site.png" width="50%" height="50%" style='border:2px solid #555'>


## Adding Packages

Pyodide packages are [defined by `meta.yaml` files](https://pyodide.org/en/stable/development/new-packages.html#creating-the-meta-yaml-file) that proivde URLs for the source code, lists of dependencies, build instructions, etc. For basic pure-Python packages, these files can be fairly minimal and [created programmatically](https://pyodide.org/en/stable/development/meta-yaml.html#meta-yaml-spec).  

One complication to keep in mind is that you will need to add all of the dependencies for your package, except for those in the [Python Standard Library](https://docs.python.org/3/library/index.html) or already [included with Pyodide](https://pyodide.org/en/stable/usage/packages-in-pyodide.html). The `finddeps.py` script described below can help identify the needed dependencies.

Adding a new package and rebuilding the distribution uses these steps:
1. Define a new package by creating a new `meta.yaml` file in [`packages`](./packages), under `packages/{package-name}/meta.yaml`.
1. Add any patch files or tests under `packages/{package-name}/`, making sure they're referenced in `meta.yaml`.
1. Update the Build and Deploy workflow to include the new package in the default build.
1. Commit the new package and updated workflow file to the repository.
1. Monitor the workflow run's progress and build status.
1. Test the updated Pyodide distribution. ([jump to section](#testing-the-pyodide-distribution)

### Adding Packages Using `pyodide-build`

Clone your repository and change into its directory

```shell
$ git clone https://github.com/{github-username}/{repo-name}.git
$ cd {repo-name}
```

---

Create a virtual Python environment. This is not strictly necessary, just a recommended practice.

```shell
$ python -m venv venv
$ source venv/bin/activate
```

---

Install `pyodide-build` and other requirement.

```shell
$ pip install -r requirements.txt
```

---

Check whether or not you need to build any additional packages. The script `finddeps.py` will list all of the dependendencies for a given package that aren't available in Pyodide or the Python Standard Library. *N.B.* The script is extremely basic and does not check the dependencies of any extras. This may miss packages necessary for building or the feature you're interested in.

You call the script via: `./finddeps.py {package-name}`.

For example, here is the result for the [Seaborn](https://seaborn.pydata.org) data visualization library.
```shell
$ ./finddeps.py seaborn
{'seaborn': set()}

```

`finddeps.py` prints out a JSON dictionary, where each key is a package name and the values are sets of package names of the dependencies for the given key. In this case, all of Seaborn's required dependencies (`numpy`, `pandas`, and `matplotlib`) are already available in Pyodide. 


If we look at `contextily`, a Python tool for retrieving tile maps, we find there are several additional packages we would need to define and build before we could use `contextily` in Pyodide.
```shell
$ ./finddeps.py contextily
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
$ pyodide skeleton pypi <package name>
```

Using Seaborn as the exampel
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



- git add, commit, push

- watch the build process
- can also build locally
  - more advanced process
- test by going to your repo and checking the build and deploy action status
- once it's built, go to console and run a test
  - good to test even an import to make sure dependencies were listed correctly
- need to define a way to keep the list of packages to build up-to-date
  - git commit hook?
  - '*'?
- Consider committing these packages to the list of Pyodide packages



## Testing the Pyodide Distribution

Test the build in the REPL console at: `https://{github-username}.github.io/{repo-name}/console.html`.

Do an import and ensure the dependencies are declared correctly.

## Using the Pyodide Distribution

The Pyodide documentation describes [how to use Pyodide](https://pyodide.org/en/stable/usage/index.html) in a web browser or environments like Node.js. For those use cases and to [use it in JupyterLite](https://jupyterlite.readthedocs.io/en/stable/howto/pyodide/pyodide.html#using-a-custom-pyodide-distribution), you will usually point to the `pyodide.js` file in the distribution. This can be fund at:

`https://{github-username}.github.io/{repo-name}/pyodide.js`





