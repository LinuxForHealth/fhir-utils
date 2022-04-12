"""
test_lib.py

Used to validate that the fhir tools behave as expected.
"""
import pytest
import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from linuxforhealth.fhir_utils.fhir_text_utils import humanname_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import address_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import telecom_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import resource_to_reference
from tests import test_directory
import os

@pytest.fixture
def patient() -> Patient:
    patient_file = open(f'{test_directory}/patient.json')
    patient_json_dict = json.load(patient_file)
    return Patient.parse_obj(patient_json_dict)


def test_name(patient):
    """check that last-first order works as expected"""
    assert patient is not None
    assert humanname_as_string(patient.name).strip() == "Hart  III, Dr. Julia"


def test_name_natural(patient):
    """check that the natural order name works as expected"""
    assert patient is not None
    assert humanname_as_string(patient.name, last_first_order=False).strip() == "Dr. Julia  Hart  III"


def test_address(patient):
    """check that address works as expected"""
    assert patient is not None
    with open(f'{test_directory}/address_text.txt') as address_file:
        address_test = address_file.read()
    assert address_as_string(patient.address) == address_test


def test_telecom(patient):
    """check that telecom (contact info) works as expected"""
    assert patient is not None

    with open(f"{test_directory}/telecom_text.txt") as telecom_file:
        telecom_test = telecom_file.read()
    assert telecom_as_string(patient.telecom) == telecom_test


def test_reference(patient):
    """check that resource to reference conversion is working as expected"""
    assert patient is not None
    assert resource_to_reference(patient, humanname_as_string(patient.name)).reference == \
           "Patient/a9831a75-3ff9-458c-9dbb-081ea3d71684"