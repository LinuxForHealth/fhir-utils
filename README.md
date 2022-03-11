# python-library-template
Quick Start Project for Developing Python Libraries

## Overview

The Python Library Template provides the boiler-plate code for bootstrapping a setuptools based Python 3.x library project.
Assets provided include:
- setup.cfg and pyproject.toml with pytest and black dependencies
- this README with the beginnings of a QuickStart
- a single unit test in src/tests/test_lib.py

To update the template replace the {library name} placeholder with the name of the library.
## QuickStart

### Pre-requisites
The LinuxForHealth {library name} development environment relies on the following software packages:

- [git](https://git-scm.com) for project version control
- [Python 3.8 or higher](https://www.python.org/downloads/) for runtime/coding support

### Project Setup and Validation
```shell
pip install --upgrade pip setuptools

git clone https://github.com/LinuxForHealth/{library name}
cd {library name}

python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip setuptools 
pip install -e .[dev]
pytest
```


### Code Formatting

LinuxForHealth {library name} adheres to the [Black Code Style and Convention](https://black.readthedocs.io/en/stable/index.html)

The following command executes the black formatter with default options

```shell
user@mbp {library name} % source venv/bin/activate
(venv) user@mbp {library name} % black ./src
```

Use the `--help` flag to view all available options for the black code formatter

```shell
(venv) user@mbp {library name} % black --help
```

## Building The Project
LinuxForHealth {library name} is aligned, to a degree, with the PEP-517 standard. `setup.cfg` stores build metadata/configuration.
`pyproject.toml` contains the build toolchain specification and black formatter configurations.

The commands below creates a source and wheel distribution within a clean build environment.

```shell
python3 -m venv build-venv && source build-venv/bin/activate && pip install --upgrade pip setuptools build wheel twine
python3 -m build --no-isolation
```
