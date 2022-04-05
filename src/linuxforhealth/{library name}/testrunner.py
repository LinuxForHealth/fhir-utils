import json
from fhir.resources.humanname import HumanName
from fhir.resources.patient import Patient
from typing import List
import fhir_text_utils


patient_file = open('patient.json')
patient_json_dict = json.load(patient_file)
print(patient_json_dict)
test_patient: Patient = Patient.parse_obj(patient_json_dict)
nane: List[HumanName] = test_patient.name
assert test_patient
print(test_patient)
print (test_patient.name)
print("Patient Name: " + fhir_text_utils.humannameasstring(test_patient.name))


