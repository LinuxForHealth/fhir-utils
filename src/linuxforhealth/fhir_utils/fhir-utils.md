# FHIR-utils
## Toolkit user manual

### Background
Anyone who has ever used FHIR resources are designed to flexibly represent clinical data, able
to accomodate an extremely wide variety of formats. This flexibility is both its power and its
pain point. Simple concepts like a patient's name is an array of arrays which to simply display
a patient's name to a webpage or database requires lot of boilerplate code to combine the series 
of name structures into useful strings. This kind of task is what the utilities here handle.

##fhir_text_utils
### Name Wrangling
In vartious resource types such as [Patient](http://hl7.org/fhir/patient.html), [Practicioner](http://hl7.org/fhir/practitioner.html)
or [RelatedPerson](http://hl7.org/fhir/relatedperson.html) there are names constructed of a List of [HumanName](http://hl7.org/fhir/datatypes.html#HumanName)
resources. The complex logic around prefix, suffixes and given and family names requires. To use the toolkit here is an example:

### Address formatting
Similar to the name, the contact information for a patient is equally complex and tedious to turn into text as it has to
accomodate a wide variety of address information around the world. Similar to the HumanName the
addresstostring function will format the address similarly to how it formats the name.

```
import fhir_text-utils

# fetch patient from the fhir-server
patient: Patient = myFhirService.getPatient(pateint-id)
# get the patient's name as a string
print(fhir_text_utils.humannameasstring(patient.name))
print(fhir_text_utils.addressasstring(patient.contact)
```
