import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from src.linuxforhealth.fhir_utils.fhir_text_utils import humanname_as_string
from src.linuxforhealth.fhir_utils.fhir_text_utils import address_as_string


patient_file = open('patient.json')
patient_json_dict = json.load(patient_file)
print(patient_json_dict)
test_patient: Patient = Patient.parse_obj(patient_json_dict)
nane: List[HumanName] = test_patient.name
assert test_patient is not None
print(f"Patient Name: [{humanname_as_string(test_patient.name).strip()}]")
assert humanname_as_string(test_patient.name).strip() == "Hart  III, Dr. Julia"

print(f"|{address_as_string(test_patient.address)}|")
with open('address_text.txt') as adress_file:
    address_test = adress_file.read()
assert address_as_string(test_patient.address) == address_test

