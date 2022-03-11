# FHIR-Utils
A Handy set of utilities with convienence methods to make working with FHIR easier and saner (such as common display of HumanName, Address, etc resource types where many parent types include lists of these requiring frequent display.

## Overview

One of the good/bad things about FHIR resources is they are designed to accomodate a huge array of data formats that healthcare users around the globe use. This means that the flexibility of data formats is also extremely flexible and accomodating that flexibility can be frustrating when doing simple tasks such as displaying a patient's name, since a large number of fields are both optional and can be single elements or lists. This does of course take into account **your** specific use case, but provides a pretty good general use case output.

## QuickStart
Including the Resource-Text-Utils class will make parsing Fhir data elements easier when outputting to display. Note each of the methods takes an optional parameter to make the output eithr plain text or HTML formatted.

### Pre-requisites
The LinuxForHealth {library name} development environment relies on the following software packages:

- [git](https://git-scm.com) for project version control
- [Python 3.8 or higher](https://www.python.org/downloads/) for runtime/coding support
- [fhir.resources](https://pypi.org/project/fhir.resources/)
- 
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
