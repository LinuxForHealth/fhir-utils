from fhir.resources.humanname import HumanName
from fhir.resources.period import Period
from fhir.resources.address import Address
from fhir.resources.fhirtypes import ReferenceType
from fhir.resources.reference import Reference
from fhir.resources.domainresource import DomainResource
from fhir.resources.contactpoint import ContactPoint
from typing import List


class FhirTextUtils:
    """
    this collection of convienence methods provides handy text formatting from common fhir resource internal elements such as names, addresses, etc.
    All methods allow for optional HTML output vs. plain-text
    """

    def humanNameAsString(self, humannames: List[HumanName], useHtml: bool = False) -> str:
        """
        Takes a list of HumanName resources (such as a patient's name) and outputs the names taking into account prefixes, suffixes, etc
        :param humannames:
        :param useHtml:
        :return: text (either plain formatted text or containing a block of HTML
        """
        if (humannames is None):
            raise RuntimeError('humanNameAsString: humanNames cannot be None for conversion')
        if (useHtml):
            newLine = '<br>\n'
            indent = '&nbsp;&nbsp;&nbsp;&nbsp;'
        else:
            newLine = '\n'
            indent = '\t'

        sb: List[str] = []
        for humanName in humannames:
            if (humanName.use):
                sb.append(humanName.use + ": ")
            if (humanName.family):
                sb.append(humanName.family + " ")
            if (humanName.suffix):
                sb.append(', ')
                for suffix in humanName.suffix:
                    sb.append(suffix + " ")
            if (humanName.prefix):
                sb.append(', ')
                for prefix in humanName.prefix:
                    sb.append(prefix + " ")
            else:
                sb.append(', ')
            if (humanName.given):
                for given in humanName.given:
                    sb.append(given + ' ')
            if (humanName.period):
                sb.append("Valid: ")
                per = str(humanName.period['start'])
                sb.append(per)
            if (humanName.period['start'] and humanName.period['end']):
                sb.append(' - ')
            if humanName.period['end']:
                end = str(humanName.period['end'])
                sb.append(end)
            sb.append(newLine)
        return "".join(sb)

    def addressasString(self, addresslist: List[Address], useHtml: bool = False) -> str:
        """
        Takes the address list from resources like Patient, Practicioner, Organisation, Location, etc. The useHTML
        flag decided whether you get back formatted plain-text or HTML (basic html block, not a full page). If using
        HTML you'd want to wrap this is a div or some other container.
        :param addresslist:
        :param useHtml:
        :return: str
        """
        if addresslist is None:
            raise RuntimeError('addressasString: addressList cannot be None for conversion')
        if (useHtml):
            newLine = '<br>\n'
            indent = '&nbsp;&nbsp;&nbsp;&nbsp;'
        else:
            newLine = '\n'
            indent = '\t'

        sb: List[str] = []

        for address in addresslist:
            sb.append(address.type + ' ' + address.use + ':' + newLine)
            for line in address.line:
                sb.append(indent + line + newLine)
                sb.append(indent + address.city + ', ' + address.state + ' ' + address.postalCode + newLine)

        return "".join(sb)

    def telecomasstring(self, contactlist: List[ContactPoint], useHtml: bool = False) -> str:

        """
        Takes the ContactPoint line (such as telecom) for resources like in a Location, Organization, Patient, etc as string.
        The useHTML
            flag decided whether you get back formatted plain-text or HTML (basic html block, not a full page). If using
            HTML you'd want to wrap this is a div or some other container.
            :param contactList:
            :param useHtml:
            :return: str
        """
        if contactlist is None:
            raise RuntimeError('telecomasstring: contactlist cannot be None for conversion')


        if (useHtml):
            newLine = '<br>\n'
            indent = '&nbsp;&nbsp;&nbsp;&nbsp;'
        else:
            newLine = '\n'
            indent = '\t'

        sb: List[str] = []

        for contact in contactlist:
            sb.append(indent+contact.system+':'+newLine)
            if useHtml and +contact.system == 'url':
                sb.append(indent+'url: <a href="'+contact.value+'">'+contact.value+'</a>'+newLine)
            else:
                sb.append(indent+contact.system+': '+contact.value+newLine)
            if contact.period:
                if contact.period['start'] is not None:
                    sb.append(' Valid: ')
                    if contact.period['start']:
                        start = contact.period['start']
                        sb.append(start)
                    if contact.period['end']:
                        start = contact.period['end']
                        sb.append(end)
        return "".join(sb)


    def resourcetoreference(self, resource: DomainResource, displaytext:str)->Reference:
        """ returns a reference type for a given resource by its ID. This does not guarantee that the referenced object
        is in fact persisted on the fhir server instance or that the reference is reachable
            :param resource:
            :return: ReferenceType
       """
        if resource is None:
            raise RuntimeError('resourcetoreference: resource cannot be None for conversion')

        if displaytext is None:
            displayText = resource.resource_type

        reference:Reference = Reference()
        reference.type = resource.resource_type
        reference.value =  resource.resource_type+'/'+resource.id
        reference.display = displayText

        return reference

