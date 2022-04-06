"""
Module: fhir_text_utils is a collection of tools to use FHIR resources in text use-cases, such as displaying a patient
resource on a screen or prinout. As anyone who has worked with FHIR knows, there is a lot of repetitive coding to parse
items such as displaying a Name or Address. This is more complicated than your typical database record for a person
as it is somewhat self definable inside the data where the data provider can specify how to interpret the record. This
is both FHIR's power and weakness in that it is infinitely flexible and unfortunately infinitely flexible.

Functions:
    humanname_as_string(humannames: List[HumanName], usehtml: bool = False, last_first_order: bool = True)
    this will turn a HumanName list from a resource (e.g. Patient.name) into a readable name. It supports HTML
    formatting (off by default) and last-first or natural order naming (last-first default)
    Example:
        Patient Name (last-first): Hart  III, Dr. Julia (last-first)
        Patient Name (natural order): Dr. Julia  Hart  III (natural)

    address_as_string(addresslist: List[Address], usehtml: bool = False)
    this will return an Address List from a resource (e.g. Patient.address) into a readble address string. It supports
    HTML formatting (off by default)
    Example:
        postal home:
            202 Clinton St.
            Woburn, MA 01807

    telecom_as_string(contactlist: List[ContactPoint], usehtml: bool = False)
    this will return a Telecom List from a resource (e.g. Practitioner.address) into a human readable list of
    contact information.
    Example:
        phone:
         work phone : (505) 555 1212
        phone:
         mobile phone : (418) 555 5613
        url:
         home url : http://wwww.juliahart.com/about/
        phone:
         old phone : (702) 555 8834

     resource_to_reference(resource: DomainResource, displaytext: str)
     this is a simple routine that takes any FHIR resource and returns a Reference to it. For those unfamiliar with
     FHIR references you can think of FHIR references as equivalent to Foreign Keys in a relational Database, except
     unlike relational databases these are generic so the type is included in the value: Type/id
     Example:
         Patient/a9831a75-3ff9-458c-9dbb-081ea3d71684
"""

from fhir.resources.humanname import HumanName
from fhir.resources.address import Address
from fhir.resources.reference import Reference
from fhir.resources.domainresource import DomainResource
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.period import Period
from fhir.resources.identifier import Identifier
from typing import List

def humanname_as_string(humannames: List[HumanName], usehtml: bool = False, last_first_order: bool = True) -> str:
    """
    Takes a list of HumanName resources (such as a patient's name) and outputs the names taking into account prefixes,
    suffixes, etc
    :param humannames:
    :param usehtml:
    :paran last_first_order: if True (default) name will be Family suffix,Prefix Given... if False will be in natural
        order as in Prefix Given Family Suffix. e.g. Dr. Sara Smith Jr. (natural order) vs. Smith Jr., Dr. Sara
    :return: text (either plain formatted text or containing a block of HTML
    """

    if humannames is None:
        raise RuntimeError("humanNameAsString: humanNames cannot be None for conversion")
    if usehtml:
        new_line = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        new_line = "\n"
        indent = "\t"
    stringarray: List[str] = []
    last_string_array: List[str] = []
    first_string_array: List[str] = []
    humanname: HumanName
    for humanname in humannames:
        stringarray.append(indent)
        if humanname.use:
            stringarray.append(f"{humanname.use}: ")
        if humanname.family:
            last_string_array.append(f"{humanname.family} ")
        suffix_space = False
        if humanname.suffix:
            last_string_array.append(" ")
            last_string_array.extend(f"{suffix}" for suffix in humanname.suffix)
            if suffix_space:
                last_string_array.append(" ")
            if not suffix_space:
                suffix_space = True
        if humanname.prefix:
            first_string_array.extend(f"{prefix} " for prefix in humanname.prefix)
        if humanname.given:
            first_string_array.extend(f"{given} " for given in humanname.given)
        if humanname.period:
            last_string_array.extend(("Valid: ", str(humanname.period["start"])))
            if humanname.period["start"] and humanname.period['end']:
                last_string_array.append(" - ")
            if humanname.period["end"]:
                end = str(humanname.period["end"])
                last_string_array.append(end)
        if last_first_order:
            stringarray.extend(("".join(last_string_array), ", ", "".join(first_string_array)))

        else:
            stringarray.extend(("".join(first_string_array), " ", "".join(last_string_array)))

        stringarray.append(new_line)
    return "".join(stringarray)


def address_as_string(addresslist: List[Address], usehtml: bool = False) -> str:
    """
    Takes the address list from resources like Patient, Practicioner, Organisation, Location, etc. The useHTML
    flag decided whether you get back formatted plain-text or HTML (basic html block, not a full page). If using
    HTML you'd want to wrap this is a div or some other container.
    :param addresslist: the list of fhir addresses from a resource
    :param usehtml: should the output be formatted as an HTML string (default plain text)
    :return: str
    """
    if addresslist is None:
        raise TypeError("addressasstring: addressList cannot be None for conversion")
    if usehtml:
        new_line = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        new_line = "\n"
        indent = "\t"

    stringarray: List[str] = []

    for address in addresslist:
        stringarray.append(f"{address.type} {address.use}:{new_line}")
        for line in address.line:
            stringarray.extend(
                (
                    indent + line + new_line,
                    indent
                    + address.city
                    + ", "
                    + address.state
                    + " "
                    + address.postalCode
                    + new_line,
                )
            )

    return "".join(stringarray)


def telecom_as_string(contactlist: List[ContactPoint], usehtml: bool = False) -> str:
    """
    Takes the ContactPoint line (such as telecom) for resources like in a Location, Organization, Patient, etc
    as string. The useHTML flag decides whether you get back formatted plain-text or HTML (basic html block, not a
    full page). If using HTML you'd want to wrap this is a div or some other container.
        :param contactlist:
        :param usehtml: whether the output is plain text or html in the string
        :return: str
    """
    if contactlist is None:
        raise TypeError("telecomasstring: contactlist cannot be None for conversion")

    if usehtml:
        new_line = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        new_line = "\n"
        indent = "\t"

    stringarray: List[str] = []

    for contact in contactlist:
        stringarray.append(indent + contact.system + ':' + new_line)
        if usehtml and contact.system == "url":
            stringarray.append(
                f'{indent}url: <a href={contact.value}>{contact.value}</a>{new_line}'
            )

        else:
            stringarray.append(f"{indent} {contact.use} {contact.system} : {contact.value} {new_line}")
        # this is separate from the other period none checks as it saves more and statement
        if contact.period:
            print(f"Period: {contact.period}")
            if contact.period.start is not None:
                stringarray.append(" Valid: ")
                if contact.period.start:
                    stringarray.append(contact.period.start)
                if contact.period.end:
                    stringarray.append(contact.period.end)
    return "".join(stringarray)


def resource_to_reference(resource: DomainResource, displaytext: str) -> Reference:
    """ returns a reference type for a given resource by its ID. This does not guarantee that the referenced object
    is in fact persisted on the fhir server instance or that the reference is reachable
        :param resource:
        :param displaytext: is the human-readable version of the reference (mostly so the reader can skip dereferencing)
        :return: ReferenceType
   """
    if resource is None:
        raise RuntimeError("resourcetoreference: resource cannot be None for conversion")

    if displaytext is None:
        displaytext = resource.resource_type

    reference: Reference = Reference()
    reference.reference = f"{resource.resource_type}/{resource.id}"
    reference.display = f"{resource.resource_type}: {displaytext}/{resource.id}"

    return reference
