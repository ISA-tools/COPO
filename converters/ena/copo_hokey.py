__author__ = 'felix.shaw@tgac.ac.uk - 26/08/15'

from .base_exporter import base_exporter

class exporter(base_exporter):

    def do_validate(self, collection_id):
        return True

    def do_export(self, collection_id, dest):
        from dal import copo_base_da, ena_da, orcid_da
        from bson import ObjectId
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
        study_alias = c['investigation']['investigationTitle']
        STUDY_TITLE.text = study_alias

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


        study_counter = 0
        # must iterate all isa studies to extract sample list from each
        for study in c['studies']:

            for s in study['study']['studySamples']:

                # get source and sample names
                for el in s:
                    if 'name' in el and el['name'] == "Source Name":
                        source_name = el['value']
                    if 'name' in el and el['name'] == "Sample Name":
                        sample_name = el['value']

                # get current affiliation
                user = ThreadLocal.get_current_user()
                affilation = orcid_da.Orcid().get_current_affliation(user).replace(' ', '_')

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

            # create experiment.xml
            EXPERIMENT_SET = ET.Element("ELEMENT_SET")

            assay_counter = 0
            for a in study['study']['assays']:


                # iterate through assay table to get required info

                '''
                    Need to make a map of sample names and keep track of
                    how many times a sample if referenced by the assay lines.
                    Unique sample references in ISA assays replated to Experiment/Run
                    pairs in SRA. Additional sample references in ISA assays relate
                    to additional SRA Runs referencing the same Experiment
                '''

                exp_run = {}
                for row in a['assaysTable']:
                    e = {'datafiles': [], 'multiplexed': False}
                    for index, cell in enumerate(row):

                        datafiles = []
                        if 'name' in cell and cell['name'] == 'Sample Name':
                            experiment_sample = cell['value']

                        if 'name' in cell and cell['name'] == 'Protocol REF' and cell['value'] == 'library construction':
                            # get the next element
                            lib = row[index+1]

                            for l in lib['items']:
                                if 'parameterTerm' in l and 'parameterValue' in l:
                                    term = l['parameterTerm']
                                    value = l['parameterValue']
                                    if term == 'library source':
                                        e['library_source'] = str(value).upper()
                                    elif term == 'library strategy':
                                        e['library_stategy'] = str(value).upper()
                                    elif term == 'library selection':
                                        e['library_selection'] = str(value).upper()
                                    elif term == 'library layout':
                                        e['library_layout'] = str(value).upper()

                        if 'name' in cell and cell['name'] == 'Raw Data File' and cell['type'] == 'isaDataNode':

                            e['datafiles'].append(cell['value'])

                        if 'name' in cell and cell['name'] == 'Protocol REF' and cell['type'] == 'isaProtocolExecutionNode' and cell['value'] == "nucleic acid sequencing":
                            machine = row[index+1]
                            for m in machine['items']:
                                if 'parameterTerm' in m and 'parameterValue' in m:
                                    term = m['parameterTerm']
                                    value = m['parameterValue']
                                    if term == "sequencing instrument":
                                        ins = value.split(' ', 1)
                                        e['platform'] = ins[0]
                                        e['model'] = ins[1]


                    if experiment_sample not in exp_run:
                        exp_run[experiment_sample] = e
                    else:
                        # if there is a sample duplication, must check of experiments are the same
                        # if they are, then it is simply an experimental repitition and can be recorded
                        # as an additional run. If there are experimental changes then another
                        # experiment/run pair must be created
                        for f in e['datafiles']:
                            exp_run[experiment_sample]['datafiles'].append(f)
                        exp_run[experiment_sample]['multiplexed'] = True



                    '''
                    EXPERIMENT = ET.SubElement(EXPERIMENT_SET, "EXPERIMENT")
                    alias = ('EXP_AUTOGEN_' + a['studyAssayTechnologyType'] + '_' + str(study_counter) + '_' + str(assay_counter)).replace(' ', '_')

                    EXPERIMENT.set('alias', alias)
                    EXPERIMENT.set('center_name', affilation)
                    EXPERIMENT_TITLE = ET.SubElement(EXPERIMENT, 'TITLE')
                    exp_title = (a['studyAssayMeasurementType'] + ' (Auto-gen)').replace(' ', '_')
                    EXPERIMENT_TITLE.text = exp_title
                    STUDY_REF = ET.SubElement(EXPERIMENT, 'STUDY_REF')
                    STUDY_REF.set('refcenter', affilation)
                    STUDY_REF.set('refname', study_alias)

                    DESIGN = ET.SubElement(EXPERIMENT, 'DESIGN')
                    DESIGN_DESCRIPTION = ET.SubElement(DESIGN, 'DESIGN_DESCRIPTION')
                    DESIGN_DESCRIPTION.text = study_alias
                    SAMPLE_DESCRIPTOR = ET.SubElement(DESIGN, 'SAMPLE_DESCRIPTOR')
                    SAMPLE_DESCRIPTOR.set('refname', experiment_sample)
                    SAMPLE_DESCRIPTOR.set('refcentre', affilation)
                    LIBRARY_DESCRIPTOR = ET.SubElement(DESIGN, "LIBRARY_DESCRIPTOR")
                    LIBRARY_NAME = ET.SubElement(LIBRARY_DESCRIPTOR, "LIBRARY_NAME")
                    LIBRARY_STRATEGY = ET.SubElement(LIBRARY_DESCRIPTOR, 'LIBRARY_STRATEGY')
                    LIBRARY_STRATEGY.text = library_stategy
                    LIBRARY_SOURCE = ET.SubElement(LIBRARY_DESCRIPTOR, "LIBRARY_SOURCE")
                    LIBRARY_SOURCE.text = library_source
                    LIBRARY_SELECTION = ET.SubElement(LIBRARY_DESCRIPTOR, "LIBRARY_SELECTION")
                    LIBRARY_SELECTION.text = library_selection
                    LIBRARY_LAYOUT = ET.SubElement(LIBRARY_DESCRIPTOR, "LIBRARY_LAYOUT")
                    TYPE = ET.SubElement(LIBRARY_LAYOUT, library_layout)


                    assay_counter += 1
                    '''
            study_counter += 1



        # write to file
        tree = ET.ElementTree(SAMPLE_SET)
        tree.write('/Users/fshaw/Desktop/sample.xml')

        tree = ET.ElementTree(EXPERIMENT_SET)
        tree.write('/Users/fshaw/Desktop/experiment.xml')





