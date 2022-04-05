import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
from src.linuxforhealth.fhir_utils.fhir_text_utils import humannameasstring
from src.linuxforhealth.fhir_utils.fhir_text_utils import addressasstring


patient_file = open('patient.json')
patient_json_dict = json.load(patient_file)
print(patient_json_dict)
test_patient: Patient = Patient.parse_obj(patient_json_dict)
nane: List[HumanName] = test_patient.name
assert test_patient is not None
print(f"Patient Name: [{humannameasstring(test_patient.name).strip()}]")
assert humannameasstring(test_patient.name).strip() == "Hart  III, Dr. Julia"

print(f"|{addressasstring(test_patient.address)}|")
adress_file = open('address_text.txt')
address_test = adress_file.read()
adress_file.close()
assert addressasstring(test_patient.address) == address_test

