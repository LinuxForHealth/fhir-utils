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
    patient_name: str = humanname_as_string(test_patient.name, False)
    # it can also return a HTML formatted version with the second parameter to true (by default it is plain-text)
    # note: you will typically wrap that in a <div></div> or some other structure
    patient_name_html: str = humanname_as_string(test_patient.name, True)
    ```
and turning FHIR [Address](http://hl7.org/fhir/datatypes.html#Address) information into a usual looking address: 
 
    ```

    from fhir_text_utils import FhirTextUtils
    from fhir.resources.patient import Patient
    from fhir.resources.practicioner import Practicioner

    patient: Patient = myFhirServer.fetch(patient_id)
    practicioner: Practicioner = myFhirServer.fetch(practicioner_id)
    practicioner_address: str = address_as_string(practicioner.address, False)
    #like the HumanName it can be either HTML or plain-text based on the second parameter
    print(practicioner_address)
    >>>postal home:
	202 Clinton St. 
	Woburn, MA 01807
    
    # pseudocode for the fhir server here. To see this happen via a local file look at the test_lib.py unit test
    print('patient: '+FhirTextUtils.humanname_as_string(patient.name))

    >>> patient: Washington Jr., Dr. Fred Lawrence
    ```
### Functions:
#### humanname_as_string(humannames: List[HumanName], usehtml: bool = False, last_first_order: bool = True)
this will turn a HumanName list from a resource (e.g. Patient.name) into a readable name. It supports HTML
formatting (off by default) and last-first or natural order naming (last-first default)
Example:

    ```
        Patient Name (last-first): Hart  III, Dr. Julia (last-first)
        Patient Name (natural order): Dr. Julia  Hart  III (natural)
    ```

#### address_as_string(addresslist: List[Address], usehtml: bool = False)
this will return an Address List from a resource (e.g. Patient.address) into a readble address string. It supports
HTML formatting (off by default)
Example:

    ```
        postal home:
            202 Clinton St.
            Woburn, MA 01807
    ```

#### telecom_as_string(contactlist: List[ContactPoint], usehtml: bool = False)
this will return a Telecom List from a resource (e.g. Practitioner.address) into a human readable list of
contact information.
    Example:

    ```
        phone:
         work phone : (505) 555 1212 
        phone:
         mobile phone : (418) 555 5613 
        url:
         home url : http://wwww.juliahart.com/about/ 
        phone:
         old phone : (702) 555 8834 
    ```
         
#### resource_to_reference(resource: DomainResource, displaytext: str)
 this is a simple routine that takes any FHIR resource and returns a Reference to it. For those unfamiliar with
 FHIR references you can think of FHIR references as equivalent to Foreign Keys in a relational Database, except
 unlike relational databases these are generic so the type is included in the value: Type/id
    Example:

    ```
        Patient/a9831a75-3ff9-458c-9dbb-081ea3d71684
    ```

### Unit Tests
Unit Tests are contained in test_lib.py inside of the tests folder which utilizes pytest to test using a static
Patient FHIR Resource contained in [patient.json](https://github.com/LinuxForHealth/fhir-utils/blob/main/src/tests/patient.json). Since the address is a longer multi-line string we use a test file
to compare to via the assertion

### Code Formatting

LinuxForHealth {library name} adheres to the [Black Code Style and Convention](https://black.readthedocs.io/en/stable/index.html)

The following command executes the black formatter with default options

    ```
    user@mbp {library name} % source venv/bin/activate
    (venv) user@mbp {library name} % black ./src
    ```

Use the `--help` flag to view all available options for the black code formatter

    ```
    (venv) user@mbp {library name} % black --help
    ```

## Building The Project
LinuxForHealth {library name} is aligned, to a degree, with the PEP-517 standard. `setup.cfg` stores build metadata/configuration.
`pyproject.toml` contains the build toolchain specification and black formatter configurations.

The commands below creates a source and wheel distribution within a clean build environment.

    ```
    python3 -m venv build-venv && source build-venv/bin/activate && pip install --upgrade pip setuptools build wheel twine
    python3 -m build --no-isolation
    ```
