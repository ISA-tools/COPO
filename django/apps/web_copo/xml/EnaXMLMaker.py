__author__ = 'fshaw'
from xml.etree.ElementTree import ElementTree, Element, SubElement
from apps.web_copo.models import Collection, EnaExperiment, EnaStudy, EnaStudyAttr, EnaSample, EnaSampleAttr, ExpFile
from chunked_upload.models import ChunkedUpload

def make_submissions(c):


    #start with study.xml
    s = EnaStudy.objects.get(collection__id=c.id)

    f = open('/Users/fshaw/Desktop/study.xml', "w")
    #must write the xml version in manually
    f.write('<?xml version="1.0" encoding="UTF-8"?>')

    #STUDY_SET is the root
    root = Element("STUDY_SET")

    #next is STUDY with alias the same as STUDY_TITLE
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

    root.append(study)

    #output whole tree to file
    tree = ElementTree(root)
    tree.write(f)
    f.close()
