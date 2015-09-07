__author__ = 'felix.shaw@tgac.ac.uk - 26/08/15'

from .base_exporter import base_exporter

class exporter(base_exporter):

    def do_validate(self, collection_id):
        return True

    def do_export(self, collection_id, dest):
        from dal import copo_base_da, ena_da, orcid_da
        from bson import ObjectId
        from xml import etree
        import xml.etree.ElementTree as ET
        from django_tools.middlewares import ThreadLocal


        head = copo_base_da.Collection_Head().GET(ObjectId(collection_id))
        c = ena_da.EnaCollection().GET(head['collection_details'][0])
        p = copo_base_da.Profile().get_profile_from_collection_id(collection_id)

        # create study.xml
        STUDY_SET = ET.Element("STUDY_SET")
        STUDY = ET.SubElement(STUDY_SET, "STUDY")
        STUDY.set('alias', c['investigation']['investigationTitle'])

        DESCRIPTOR = ET.SubElement(STUDY, "DESCRIPTOR")
        STUDY_TITLE = ET.SubElement(DESCRIPTOR, "STUDY_TITLE")
        STUDY_TITLE.text = c['investigation']['investigationTitle']

        STUDY_TYPE = ET.SubElement(DESCRIPTOR, "STUDY_TYPE")
        STUDY_TYPE.text = c['studies'][0]['study']['studyDesignDescriptors'][0]['studyDesignType']

        CENTER_PROJECT_NAME = ET.SubElement(DESCRIPTOR, "CENTER_PROJECT_NAME")
        CENTER_PROJECT_NAME.text = c['investigation']['investigationTitle']

        STUDY_ABSTRACT = ET.SubElement(DESCRIPTOR, "STUDY_ABSTRACT")
        STUDY_ABSTRACT.text = p['abstract']

        STUDY_DESCRIPTION = ET.SubElement(DESCRIPTOR, "STUDY_DESCRIPTION")
        STUDY_DESCRIPTION.text = p['abstract']

        # write to file
        tree = ET.ElementTree(STUDY_SET)
        tree.write('/Users/fshaw/Desktop/study.xml')


        # create samples.xml
        SAMPLE_SET = ET.Element("SAMPLE_SET")
        for s in c['studies'][0]['study']['studySamples']:

            # get source and sample names
            for el in s:
                if 'name' in el and el['name'] == "Source Name":
                    source_name = el['value']
                if 'name' in el and el['name'] == "Sample Name":
                    sample_name = el['value']

            # get current affiliation
            user = ThreadLocal.get_current_user()
            affilation = orcid_da.Orcid().get_current_affliation(user)

            SAMPLE = ET.SubElement(SAMPLE_SET, "SAMPLE")
            SAMPLE.set('alias', sample_name)
            SAMPLE.set('center_name', affilation)

            SAMPLE_TITLE = ET.SubElement(SAMPLE, "TITLE")
            SAMPLE_TITLE.text = sample_name

            SAMPLE_NAME = ET.SubElement(SAMPLE, "SAMPLE_NAME")

            SCIENTIFIC_NAME = ET.SubElement(SAMPLE_NAME, "SCIENTIFIC_NAME")
            SCIENTIFIC_NAME.text = s[1]['items'][0]['characteristics']
            TAXON_ID = ET.SubElement(SAMPLE_NAME, "TAXON_ID")
            TAXON_ID.text = s[1]['items'][0]['termAccessionNumber']
            DESCRIPTION = ET.SubElement(SAMPLE, "DESCRIPTION")
            DESCRIPTION.text = source_name

        # write to file
        tree = ET.ElementTree(SAMPLE_SET)
        tree.write('/Users/fshaw/Desktop/sample.xml')