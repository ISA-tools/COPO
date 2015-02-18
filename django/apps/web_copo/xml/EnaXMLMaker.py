__author__ = 'fshaw'
from xml.etree.ElementTree import ElementTree, Element, SubElement
from apps.web_copo.models import Collection, EnaExperiment, EnaStudy, EnaStudyAttr, EnaSample, EnaSampleAttr, ExpFile
from chunked_upload.models import ChunkedUpload

def make_submissions(c):

    output_path = '/Users/fshaw/Desktop/study.xml'

    #make study method creates study.xml submission file and returns
    #the study object associated with the collection_id
    s = make_study_xml(c, output_path )
    #same deal for make_sample_xml
    make_sample_xml(s.id)

def stamp_xml_version(f):
    f.write('<?xml version="1.0" encoding="UTF-8"?>')

def make_study_xml(c, output_path):
    s = EnaStudy.objects.get(collection__id=c.id)
    a = EnaStudyAttr.objects.filter(ena_study__id=s.id)

    f = open(output_path, "w")

    #must write the xml version in manually
    stamp_xml_version(f)

    #STUDY_SET is the root
    root = Element("STUDY_SET")

    study = Element("STUDY", {'alias': s.study_title})

    descriptor = Element("DESCRIPTOR")
    study.append(descriptor)

    study_title = Element("STUDY_TITLE")
    study_title.text = s.study_title
    descriptor.append(study_title)

    study_type = Element("STUDY_TYPE", {'existing_study_type': s.study_type})
    descriptor.append(study_type)

    center_project_name = Element("CENTER_PROJECT_NAME")
    center_project_name.text = s.center_project_name
    descriptor.append(center_project_name)

    study_abstract = Element("STUDY_ABSTRACT")
    study_abstract.text = s.study_abstract
    descriptor.append(study_abstract)

    study_description = Element("STUDY_DESCRIPTION")
    study_description.text = s.study_description
    descriptor.append(study_description)

    attributes = Element("STUDY_ATTRIBUTES")
    study.append(attributes)
    for attr in a:
        attribute = Element("STUDY_ATTRIBUTE")
        tag = Element("TAG")
        tag.text = attr.tag
        value = Element("VALUE")
        value.text = attr.value
        unit = Element("UNIT")
        unit.text = attr.unit
        attribute.append(tag)
        attribute.append(value)
        attribute.append(unit)
        attributes.append(attribute)

    root.append(study)

    #output whole tree to file
    tree = ElementTree(root)
    tree.write(f)
    f.close()
    return s


def make_sample_xml(s):
    pass