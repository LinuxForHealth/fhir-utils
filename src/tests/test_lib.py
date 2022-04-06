"""
test_lib.py

Used to validate that the fhir tools behave as expected.
"""
import pytest
import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from src.linuxforhealth.fhir_utils.fhir_text_utils import humanname_as_string
from src.linuxforhealth.fhir_utils.fhir_text_utils import address_as_string
from src.linuxforhealth.fhir_utils.fhir_text_utils import telecom_as_string
from src.linuxforhealth.fhir_utils.fhir_text_utils import resource_to_reference


@pytest.fixture
def test_patient() -> Patient:
    patient_file = open('patient.json')
    patient_json_dict = json.load(patient_file)
    return Patient.parse_obj(patient_json_dict)

# check that last-first order works as expected
def run_test_name(test_patient):
    assert test_patient is not None
    assert humanname_as_string(test_patient.name).strip() == "Hart  III, Dr. Julia"

# check that the natural order name works as expected
def reun_test_name_natural(test_patient):
    assert test_patient is not None
    assert humanname_as_string(test_patient.name, last_first_order=False).strip() == "Dr. Julia  Hart  III"

# check that address works as expected
def run_test_address(test_patient):
    assert test_patient is not None
    with open('address_text.txt') as adress_file:
        address_test = adress_file.read()
    assert address_as_string(test_patient.address) == address_test

# check that telecom (contact info) works as expected
def run_test_telecom(test_patient):
    assert test_patient is not None
    with open("telecom_text.txt") as telecom_file:
        telecom_test = telecom_file.read()
    assert telecom_as_string(test_patient.telecom) == telecom_test

# check that resource to reference conversion is working as expected
def run_test_reference(test_patient):
    assert test_patient is not None
    assert resource_to_reference(test_patient, humanname_as_string(test_patient.name)).reference == \
           "Patient/a9831a75-3ff9-458c-9dbb-081ea3d71684"