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


# Arrange json
def load_test_patient():
    patient_file = open('../linuxforhealth/{library name}/patient.json')
    patient_json_dict = json.load(patient_file)
    test_patient: Patient = Patient.parse_obj(patient_json_dict)
    assert(test_patient)
    assert(humannameasstring(test_patient.name) == "Hart  III, Dr. Julia")


@pytest.fixture
def test_humanname_to_str(load_test_patient):
    # Act
    name_as_string = humannameasstring(*load_test_patient.name, False)
