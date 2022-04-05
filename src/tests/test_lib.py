"""
test_lib.py

Used to validate that the fhir tools behave as expected.
"""
import pytest
import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from src.linuxforhealth.fhir_utils.fhir_text_utils import humannameasstring
from src.linuxforhealth.fhir_utils.fhir_text_utils import addressasstring


@pytest.fixture
def test_patient() -> Patient:
    patient_file = open('patient.json')
    patient_json_dict = json.load(patient_file)
    return Patient.parse_obj(patient_json_dict)


def run_test_name(test_patient):
    assert test_patient is not None
    assert humannameasstring(test_patient.name).strip() == "Hart  III, Dr. Julia"


def run_test_address(test_patient):
    assert test_patient
    with open('address_text.txt') as adress_file:
        address_test = adress_file.read()
    assert addressasstring(test_patient.address) == address_test
