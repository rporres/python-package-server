from setuptools import find_packages, setup

setup(
    name="pypi-on-github-indexer",
    description="Proprietary package publisher to the GitHub index repository.",
    version="1.0.0",
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
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Version Control :: Git",
    ],
)