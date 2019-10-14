import argparse
from email.utils import parseaddr
import subprocess
import sys
import os
from pathlib import Path
import re
import tempfile

from packaging import version as packaging_version

from pypi_on_github_indexer.parser.index_html_parser import IndexHTMLParser


def parse_args():
    parser = argparse.ArgumentParser()
    required = (("repo-url", "The repository URL where the Python package officially lives. "
                             "It should start with \"https://\"."),
                ("github-token", "GitHub token to use for pushing to the index repository."),
                ("index-name", "Index repository name on GitHub, e.g. "
                               "\"rporres/python-package-server\"."),
                ("signature", "Git signature for the index repository, in the standard format "
                             "Full Name <email@com>"))
    optional = (("package-path", "Path to the Python package root.", "."),
                ("repo-tag", "The tag to publish.", ""),
                ("target-branch", "The Git branch to which to publish the package.", "master"),
                ("target-dir", "Path in the index repository that is the PyPi root. We are "
                               "assuming GitHub Pages by default.",
                 "docs"))
    required = tuple((p + (None,)) for p in required)
    for arg, help, default in required + optional:
        default = os.getenv(arg.replace("-", "_").upper(), default)
        parser.add_argument("--" + arg, help=help + " Default: \"%s\"." % default, default=default)
    args = parser.parse_args()
    error = False
    required = set(p[0] for p in required)
    for k, v in vars(args).items():
        # required=True will not work here because we need to check the environment variables
        if k.replace("_", "-") not in required:
            continue
        if not v:
            print("Missing argument --%s / environment variable %s" %
                  (k.replace("_", "-"), k.upper()), file=sys.stderr)
            error = True
    name, email = parseaddr(args.signature)
    if not name or not email:
        print("Invalid Git signature: " + args.signature, file=sys.stderr)
        error = True
    return args, error


def shell(*args):
    print(" ".join(args))
    subprocess.run(args, check=True)


def main():
    args, error = parse_args()
    if error:
        return 1

    # Discover the package metadata: name, version, required minimum Python version
    cwd = os.getcwd()
    os.chdir(args.package_path)
    cmd = [sys.executable, str(Path(args.package_path) / "setup.py"), "--name", "--version",
           "--classifiers"]
    print(" ".join(cmd))
    metadata = subprocess.check_output(cmd).decode().split("\n")
    package_name, package_version = metadata[:2]
    # Normalize name
    # See https://www.python.org/dev/peps/pep-0503/#normalized-names
    normalized_package_name = re.sub(r"[-_.]+", "-", package_name).lower()
    index_file = Path(args.target_dir) / normalized_package_name / "index.html"
    python_classifier = "Programming Language :: Python :: "
    try:
        python_version = sorted(packaging_version.parse(line[len(python_classifier):])
                                for line in metadata[2:]
                                if line.startswith(python_classifier))[0]
    except IndexError:
        raise LookupError("setup.py must contain a \"%s\" classifier."
                          % python_classifier.strip()) from None
    if not args.repo_tag:
        args.repo_tag = "v" + package_version
    os.chdir(cwd)

    # Publish the new version
    with tempfile.TemporaryDirectory() as index_dir:
        shell("git", "clone", "--branch=" + args.target_branch, "--depth=1",
              "https://%s@github.com/%s.git" % (args.github_token, args.index_name), index_dir)
        index_file = Path(index_dir) / index_file
        parser = IndexHTMLParser()
        links_data = parser.get_index_data(str(index_file))

        links_data.append({
            "href": "git+%(repo_url)s@%(repo_tag)s#egg=%(package_name)s-%(package_version)s" %
                    dict(repo_url=args.repo_url,
                         repo_tag=args.repo_tag,
                         package_version=package_version,
                         package_name=package_name),
            "data-requires-python": "&gt;=%s" % python_version,
            "data": "-".join([package_name, package_version])
        })

        lt = '<a href="%s" data-requires-python="%s">%s</a><br/>'
        links = [lt % (d["href"], d["data-requires-python"], d["data"]) for d in links_data]
        doc = """<!DOCTYPE html>
<html>
<head>
<title>Links for %(package)s</title>
</head>
<body>
<h1>Links for %(package)s</h1>
%(links)s
</body>
</html>
""" % dict(package=package_name, links="\n".join(links))

        # push the changes
        os.chdir(index_dir)
        name, email = parseaddr(args.signature)
        shell("git", "config", "user.name", name)
        shell("git", "config", "user.email", email)

        if not index_file.exists():
            index_file.parent.mkdir()
        with open(index_file, "w") as f:
            f.write(doc)

        shell("git", "add", "-A")
        shell("git", "commit", "-sm", "Update index for %s-%s" %
              (normalized_package_name, package_version))
        shell("git", "push", "origin", "%s:%s" % (args.target_branch, args.target_branch))


if __name__ == "__main__":
    sys.exit(main())

