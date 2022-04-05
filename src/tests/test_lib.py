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


@pytest.fixture
def test_patient() -> Patient:
    patient_file = open('patient.json')
    patient_json_dict = json.load(patient_file)
    return Patient.parse_obj(patient_json_dict)


def run_test_name(test_patient):
    assert test_patient is not None
    assert humanname_as_string(test_patient.name).strip() == "Hart  III, Dr. Julia"


def run_test_address(test_patient):
    assert test_patient
    with open('address_text.txt') as adress_file:
        address_test = adress_file.read()
    assert address_as_string(test_patient.address) == address_test
