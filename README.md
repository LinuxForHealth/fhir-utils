# FHIR-Utils
A Handy set of utilities with convenience methods to make working with FHIR easier and saner (such as common display of
[HumanName](http://hl7.org/fhir/datatypes.html#HumanName), [Address](http://hl7.org/fhir/datatypes.html#Address), etc 
resource types where many parent types include lists of these requiring frequent display.

## Overview

One of the good/bad things about [FHIR resources](http://hl7.org/fhir/resourcelist.html) is they are designed to 
accommodate a huge array of data formats that healthcare users around the globe use. This means that the flexibility 
of data formats is also extremely flexible and accomodating that flexibility can be frustrating when doing simple 
tasks such as displaying a patient's name, since a large number of fields are both optional and can be single elements 
or lists. This does of course take into account **your** specific use case, but provides a pretty good general use 
case output.

## Target User
This is a python library so is oriented towards a python developer working with FHIR in a healthcare context where
you need to display FHIR data in a human readable format (rather than the typical demo of dumping the JSON, even if
pretty-printed to the screen).

## QuickStart
Including the fhir_text_utils class will make parsing Fhir data elements easier when outputting for display. 
**Note** each of the methods takes an *optional* parameter to make the output either plain text or HTML formatted.

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
### Usage
In python applications that deal with [FHIR](http://hl7.org/fhir/) resources, you can import the fhir_text_utils.py module and inside you will find a collection of useful utility methods for frequently performed FHIR tasks (such as printing a patient's address or HumanName)

The 2 most commonly used methods will be: 

turning FHIR [HumanName](http://hl7.org/fhir/datatypes.html#HumanName)) lists into strings:

    ```
    patient_name: str = humannameasstring(test_patient.name, False)
    # it can also return a HTML formatted version with the second parameter to true (by default it is plain-text)
    # note: you will typically wrap that in a <div></div> or some other structure
    patient_name_html: str = humannameasstring(test_patient.name, True)
    ```
and turning FHIR [Address](http://hl7.org/fhir/datatypes.html#Address) information into a usual looking address: 
 
    ```
    practicioner_address: str = addressasstring(practicioner.address, False)
    #like the HumanName it can be either HTML or plain-text based on the second parameter
    ```

```
from fhir_text_utils import FhirTextUtils
from fhir.resources.patient import Patient

# pseudocode for the fhir server here. To see this happen via a local file look at the test_lib.py unit test
patient: Patient = myFhirServer.fetch(patientId)
print('patient: '+FhirTextUtils.humanNameAsString(patient.name))

>>> patient: Washington Jr., Dr. Fred Lawrence
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
