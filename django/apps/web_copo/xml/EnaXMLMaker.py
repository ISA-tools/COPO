__author__ = 'fshaw'
from xml.etree.ElementTree import ElementTree, Element, SubElement
from apps.web_copo.models import Collection, EnaExperiment, EnaStudy, EnaStudyAttr, EnaSample, EnaSampleAttr, ExpFile
from chunked_upload.models import ChunkedUpload



def make_submissions(c):

    study_path = '/Users/fshaw/Desktop/study.xml'
    sample_path = '/Users/fshaw/Desktop/sample.xml'
    exp_path = '/Users/fshaw/Desktop/experiment.xml'
    #make study method creates study.xml submission file and returns
    #the study object associated with the collection_id
    s = make_study_xml(c, study_path)
    #same deal for make_sample_xml
    make_sample_xml(s, sample_path)
    make_exp_xml(s, exp_path)



def stamp_xml_version(f):
    f.write('<?xml version="1.0" encoding="UTF-8"?>')



def make_study_xml(c, output_path):
    s = EnaStudy.objects.get(collection__id=c.id)
    a = EnaStudyAttr.objects.filter(ena_study__id=s.id)

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
    f = open(output_path, "w")
    #must write the xml version in manually
    stamp_xml_version(f)

    tree = ElementTree(root)
    tree.write(f)
    f.close()
    return s


def make_sample_xml(s, output_path):
    #get relevant samples for study
    samples = EnaSample.objects.filter(ena_study__id=s.id)


    root = Element("SAMPLE_SET")

    #iterate over samples and sample attributes
    for sample in samples:
        samp = Element("SAMPLE", {'alias': sample.title, 'center_name': s.center_name})
        title = Element("TITLE")
        title.text = sample.title
        samp.append(title)

        sample_name = Element("SAMPLE_NAME")
        scientific_name = Element("SCIENTIFIC_NAME")
        scientific_name.text = sample.scientific_name
        sample_name.append(scientific_name)
        taxon_id = Element("TAXON_ID")
        taxon_id.text = str(sample.taxon_id)
        sample_name.append(taxon_id)
        common_name = Element("COMMON_NAME")
        common_name.text = sample.common_name
        sample_name.append(common_name)
        samp.append(sample_name)

        description = Element("DESCRIPTION")
        description.text = sample.description
        samp.append(description)

        attribs = EnaSampleAttr.objects.filter(ena_sample__id=sample.id)
        attributes = Element("SAMPLE_ATTRIBUTES")
        for attr in attribs:
            attribute = Element("SAMPLE_ATTRIBUTE")
            tag = Element("TAG")
            tag.text = attr.tag
            attribute.append(tag)
            value = Element("VALUE")
            value.text = attr.value
            attribute.append(value)
            unit = Element("UNIT")
            unit.text = attr.unit
            attribute.append(unit)
            attributes.append(attribute)


        samp.append(attributes)

        root.append(samp)

    f = open(output_path, 'w')
    stamp_xml_version(f)

    tree = ElementTree(root)
    tree.write(f)
    f.close()


def make_exp_xml(s, output_path):
    experiments = EnaExperiment.objects.filter(study__id=s.id)

    root = Element("EXPERIMENT_SET")

    for exp in experiments:
        experiment = Element("EXPERIMENT")

    f = open(output_path, 'w')
    stamp_xml_version(f)

    tree = ElementTree(root)
    tree.write(f)
    f.close()