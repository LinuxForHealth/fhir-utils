from fhir.resources.humanname import HumanName
from fhir.resources.address import Address
from fhir.resources.reference import Reference
from fhir.resources.domainresource import DomainResource
from fhir.resources.contactpoint import ContactPoint
from typing import List


def humannameasstring(humannames: List[HumanName], useHtml: bool = False) -> str:
    """
    Takes a list of HumanName resources (such as a patient's name) and outputs the names taking into account prefixes, suffixes, etc
    :param humannames:
    :param useHtml:
    :return: text (either plain formatted text or containing a block of HTML
    """
    if humannames is None:
        raise RuntimeError("humanNameAsString: humanNames cannot be None for conversion")
    if useHtml:
        newLine = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        newLine = "\n"
        indent = "\t"

    stringarray: List[str] = []
    for humanName in humannames:
        if humanName.use:
            stringarray.append(f"{humanName.use}: ")
        if humanName.family:
            stringarray.append(f"{humanName.family} ")
        if humanName.suffix:
            stringarray.append(", ")
            stringarray.extend(f"{suffix} " for suffix in humanName.suffix)
        stringarray.append(", ")
        if humanName.prefix:
            stringarray.extend(f"{prefix} " for prefix in humanName.prefix)
        if humanName.given:
            stringarray.extend(f"{given} " for given in humanName.given)
        if humanName.period:
            stringarray.extend(("Valid: ", str(humanName.period["start"])))
        if humanName.period["start"] and humanName.period['end']:
            stringarray.append(" - ")
        if humanName.period["end"]:
            end = str(humanName.period["end"])
            stringarray.append(end)
        stringarray.append(newLine)
    return "".join(stringarray)


def addressasstring(addresslist: List[Address], useHtml: bool = False) -> str:
    """
    Takes the address list from resources like Patient, Practicioner, Organisation, Location, etc. The useHTML
    flag decided whether you get back formatted plain-text or HTML (basic html block, not a full page). If using
    HTML you'd want to wrap this is a div or some other container.
    :param addresslist:
    :param useHtml:
    :return: str
    """
    if addresslist is None:
        raise TypeError("addressasstring: addressList cannot be None for conversion")
    if useHtml:
        newLine = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        newLine = "\n"
        indent = "\t"

    stringarray: List[str] = []

    for address in addresslist:
        stringarray.append(f"{address.type} {address.use}:{newLine}")
        for line in address.line:
            stringarray.extend(
                (
                    indent + line + newLine,
                    indent
                    + address.city
                    + ", "
                    + address.state
                    + " "
                    + address.postalCode
                    + newLine,
                )
            )

    return "".join(stringarray)


def telecomasstring(contactlist: List[ContactPoint], useHtml: bool = False) -> str:

    """
    Takes the ContactPoint line (such as telecom) for resources like in a Location, Organization, Patient, etc as string.
    The useHTML
        flag decided whether you get back formatted plain-text or HTML (basic html block, not a full page). If using
        HTML you'd want to wrap this is a div or some other container.
        :param contactlist:
        :param useHtml:
        :return: str
    """
    if contactlist is None:
        raise TypeError("telecomasstring: contactlist cannot be None for conversion")


    if useHtml:
        newLine = "<br>\n"
        indent = "&nbsp;&nbsp;&nbsp;&nbsp;"
    else:
        newLine = "\n"
        indent = "\t"

    stringarray: List[str] = []

    for contact in contactlist:
        stringarray.append(indent+contact.system+':'+newLine)
        if useHtml and contact.system == "url":
            stringarray.append(
                f'{indent}url: <a href={contact.value}>{contact.value}</a>{newLine}'
            )

        else:
            stringarray.append(indent+contact.system+': '+contact.value+newLine)
        if contact.period and contact.period["start"] is not None:
            stringarray.append(" Valid: ")
            if contact.period["start"]:
                stringarray.append(contact.period["start"])
            if contact.period["end"]:
                stringarray.append(contact.period["end"])
    return "".join(stringarray)


def resourcetoreference(resource: DomainResource, displaytext:str) -> Reference:
    """ returns a reference type for a given resource by its ID. This does not guarantee that the referenced object
    is in fact persisted on the fhir server instance or that the reference is reachable
        :param resource:
        :return: ReferenceType
   """
    global displayText
    if resource is None:
        raise RuntimeError("resourcetoreference: resource cannot be None for conversion")

    if displaytext is None:
        displayText = resource.resource_type

    reference:Reference = Reference()
    reference.type = resource.resource_type
    reference.value = f"{resource.resource_type}/{resource.id}"
    reference.display = displayText

    return reference

