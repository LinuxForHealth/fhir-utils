import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from linuxforhealth.fhir_utils.fhir_text_utils import humanname_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import address_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import telecom_as_string
from linuxforhealth.fhir_utils.fhir_text_utils import resource_to_reference


patient_file = open('patient.json')
patient_json_dict = json.load(patient_file)
print(patient_json_dict)
test_patient: Patient = Patient.parse_obj(patient_json_dict)
nane: List[HumanName] = test_patient.name
assert test_patient is not None
print(f"Patient Name (last-first): {humanname_as_string(test_patient.name).strip()}")
print(f"Patient Name (natural order): {humanname_as_string(test_patient.name, last_first_order=False).strip()}")

assert humanname_as_string(test_patient.name).strip() == "Hart  III, Dr. Julia"

print(f"|{address_as_string(test_patient.address)}|")
with open('address_text.txt') as adress_file:
    address_test = adress_file.read()
print(test_patient.telecom)
print(telecom_as_string(test_patient.telecom))
assert resource_to_reference(test_patient, humanname_as_string(test_patient.name)).reference == \
       "Patient/a9831a75-3ff9-458c-9dbb-081ea3d71684"
