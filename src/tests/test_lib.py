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


@pytest.fixture
def test_patient()->Patient:
    patient_file = open('patient.json')
    patient_json_dict = json.load(patient_file)
    return Patient.parse_obj(patient_json_dict)


def run_test(test_patient):
    assert test_patient is not None
    assert humannameasstring(test_patient.name).strip() == "Hart  III, Dr. Julia"
