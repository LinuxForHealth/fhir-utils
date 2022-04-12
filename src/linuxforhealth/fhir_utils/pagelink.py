from fhir.resources.bundle import BundleLink
from urllib.parse import urlparse, parse_qs
from typing import List


class PageLink:
    """
    This class is a structured object that breaks out the FHIR bundle Link object into a usable object for managing
    paging through FHIR data; when using this to subsequently page through a fhir resource via a search method set the
    **page** parameter to the value
    of this query page.
    """

    title: str
    page: int
    count: int

    def __init__(self, link: BundleLink):
        """
        this initializor, allows conversion of a fhir link which is returned in the response to a resource fhir search
        query.
        :param link:
        :return: a pagelink object
        """
        self.title = link.relation
        parsed_url = urlparse(link.url)
        arguments: dict[str, List[str]] = dict(parse_qs(parsed_url.query))
        print(arguments)
        self.page = int(arguments['_page'][0])
        self.count = int(arguments['_count'][0])

    def __str__(self):
        """
        Standard str method for this class produces human-readable text for the values in the link
        :param self:
        :return:
        """
        return f"type: {self.title} on page: {self.page} with count: {self.count}"
