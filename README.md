# pypi-on-github-indexer

This script creates or updates a PyPI index as defined by [PEP 503](https://www.python.org/dev/peps/pep-0503/) that lives in a git repository using `git+https` urls that are supported by pip (see https://pip.pypa.io/en/stable/reference/pip_install/#git).

## Usage

This script is meant to be run in the git repository of the package that you want to index. Let's pick a case:

* You have an package index in https://github.com/user/python-package-index that you serve via GH pages with your documents under `docs`
* You want to add a version `0.1.0` of your `foo-bar` package, that lives in https://github.com/user/foo-bar repository

The following command
```
python3 -m pypi_on_github_indexer \
    --signature "Name Surname <name@domain.com>" \
    --github-token XXXXXXXX \
    --index-name user/python-package-index \
    --repo-url https://github.com/user/foo-bar
    --repo-tag v0.1.0
```
will parse repo's `setup.py` to find the package version, the package name and the minimum python version to add a commit in the repository containing the index with the following index line
```
<a href="git+https://github.com/src-d/foo-bar@v0.1.0#egg=foo-bar-0.1.0" data-requires-python="&gt;=3.5">foo-bar-0.1.0</a><br/>
```
Specifying the repository tag is mandatory, and the tag name is checked against the package version to avoid inconsistencies.

See `--help` for the full list of command's options.
