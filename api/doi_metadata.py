__author__ = 'etuka'

import ast
import rdflib
from urllib.request import Request, urlopen

from services import DOI_SERVICES as ds
from services import NCBI_SERVICES as ncbi


# class handles both DOI and PubMed Id resolutions
class DOI2Metadata:
    def __init__(self, id_handle):
        # id_handle could resolve to either an DOI or PubMed ID
        self.error_messages = []

        self.id_handle = id_handle
        self.id_type = "pmid"  # for PubMed ID
        self.verify_id_type()

        self.data_dict = {}

    def verify_id_type(self):
        # determine the identifier type
        # PubMed ID has a specific format: digits!

        if not self.id_handle.isdigit():
            self.id_type = "doi"

    def get_pmid(self):
        pmid = ""
        if self.id_type == "doi":
            result_dict = self.do_idconvert()
            if result_dict and "records" in result_dict:
                records = result_dict["records"][0]
                if "pmid" in records:
                    pmid = records["pmid"]

        elif self.id_type == "pmid":
            pmid = self.id_handle

        return pmid

    def get_doi(self):
        doi = ""
        if self.id_type == "doi":
            # strip doi of base, if supplied along
            doi = self.id_handle
            if ds["base_url"] in doi:
                doi = doi.split(ds["base_url"])[1]
            doi = doi.strip("/")  # parsers don't like trailing slashes

        elif self.id_type == "pmid":  # try resolving the doi from the PubMed ID
            temp_dict = self.get_esummary()

            if temp_dict and "articleids" in temp_dict:
                for article_id in temp_dict["articleids"]:
                    if article_id["idtype"] == "doi":
                        doi = article_id["value"]
                        break

        return doi

    def do_idconvert(self):  # given doi, find pmid
        doi = self.get_doi()

        result_dict = {}
        r = ncbi["PMC_APIS"]["doi_pmid_idconv"].format(**locals())
        q = Request(r)
        q.add_header('Accept', 'application/json')
        try:
            request = urlopen(q)
            result_dict = request.read().decode("utf-8")
            result_dict = ast.literal_eval(result_dict)
        except:
            self.error_messages.append("Could not access remote resource")
        return result_dict

    def get_esummary(self):  # assuming pmid, get publication metadata
        temp_dict = {}
        if "pmid_esummary" in self.data_dict:
            temp_dict = self.data_dict["pmid_esummary"]
        else:
            pmid = self.get_pmid()

            r = ncbi["PMC_APIS"]["pmid_doi_esummary"].format(**locals())
            q = Request(r)

            result_dict = {}
            try:
                request = urlopen(q)
                result_dict = request.read().decode("utf-8")
                result_dict = ast.literal_eval(result_dict)
            except:
                self.error_messages.append("Could not access remote resource")

            if "result" in result_dict:
                if pmid in result_dict["result"] and "error" not in result_dict["result"][pmid]:
                    self.data_dict["pmid_esummary"] = result_dict["result"][pmid]
                    temp_dict = self.data_dict["pmid_esummary"]
                else:
                    self.error_messages.append("Could get remote resource")

        return temp_dict

    def get_publication_metadata_pmid(self, pub_meta):
        temp_dict = self.get_esummary()
        if temp_dict:
            # other NCBI PMC APIs could potentially be called here, e.g., "E-Fetch"
            # to obtain a richer metadata context
            if "title" in temp_dict:
                pub_meta["dc:title"] = temp_dict["title"]
            if "recordstatus" in temp_dict:
                pub_meta["dc:status"] = temp_dict["recordstatus"]

            if "authors" in temp_dict:
                for author in temp_dict["authors"]:
                    if author["authtype"] == "Author":
                        pub_meta["dc:creator"].append(author["name"])

        return pub_meta

    def get_publication_metadata_doi(self, pub_meta):
        doi = ds["base_url"] + self.get_doi()
        graph = rdflib.Graph()
        try:
            graph.parse(doi)
        except:
            self.error_messages.append("Could not resolve doi")

        # define relevant namespaces
        # this may not be relevant in the pubmed resolution route
        FOAF = rdflib.Namespace(ds["namespaces"]["FOAF"])
        DC = rdflib.Namespace(ds["namespaces"]["DC"])

        # get title
        for triple in graph.triples((None, DC["title"], None)):
            if isinstance(triple[2], rdflib.term.Literal):
                if str(doi) == str(triple[0]):
                    pub_meta["dc:title"] = str(triple[2])

        # get authors
        for triple in graph.triples((None, DC["creator"], None)):
            if isinstance(triple[2], rdflib.term.Literal):
                pub_meta["dc:creator"].append(str(triple[2]))
            elif isinstance(triple[2], rdflib.term.URIRef):
                for x in graph.triples((triple[2], FOAF['name'], None)):
                    pub_meta["dc:creator"].append(str(x[2]))

        return pub_meta

    def publication_metadata(self):
        pub_meta = {
            "dc:title": "",
            "dc:creator": [],
            "dc:status": "",
            "dc:identifier_doi": "",
            "dc:identifier_pmid": ""
        }

        doi = self.get_doi()
        pmid = self.get_pmid()

        if pmid:
            # seems more reliable/richer in context to use NCBI PMC to glean metadata
            pub_meta = self.get_publication_metadata_pmid(pub_meta)
        elif doi:
            # resolve using doi if pmid is non-existing
            pub_meta = self.get_publication_metadata_doi(pub_meta)

        pub_meta["dc:identifier_doi"] = doi
        pub_meta["dc:identifier_pmid"] = pmid

        if not self.error_messages:
            out_dict = {"status": "success", "data": pub_meta}
        else:
            out_dict = {"status": "failed", "messages": self.error_messages, "data": {}}

        return out_dict

    def dataset_metadata(self):
        # will handle resolution of metadata for datasets
        pass
