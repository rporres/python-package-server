from setuptools import find_packages, setup
import os

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pypi-on-github-indexer",
    description="Proprietary package publisher to the GitHub index repository.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.1.1",
    license="Apache-2.0",
    author="source{d}",
    author_email="infrastructure@sourced.tech",
    url="https://github.com/src-d/pypi-on-github-indexer",
    download_url="https://github.com/src-d/pypi-on-github-indexer",
    packages=find_packages(),
    keywords=["pypi", "pip"],
    install_requires=[
        "packaging>=16.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Version Control :: Git",
    ],
)
