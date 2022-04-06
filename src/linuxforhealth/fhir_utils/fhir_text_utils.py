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
        order as in Prefix Given Family Suffix.
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
            stringarray.append("".join(last_string_array))
            stringarray.append(", ")
            stringarray.append("".join(first_string_array))
        else:
            stringarray.append("".join(first_string_array))
            stringarray.append(" ")
            stringarray.append("".join(last_string_array))

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
