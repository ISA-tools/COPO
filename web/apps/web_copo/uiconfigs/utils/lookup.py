# define parameters for schemas

SCHEMAS = {
    'ENA': {
        'PATHS_AND_URIS': {
            'ISA_json': 'apps/web_copo/uiconfigs/ena/dbmodels/isa_ena_model.json',
            'UI_TEMPLATE_json': 'apps/web_copo/uiconfigs/ena/uimodels/ena_copo_template.json',
            'INVESTIGATION_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                  '/isaconfig-default_v2014-01-16/investigation.xml',
            'STUDY_SAMPLE_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                 '/isaconfig-default_v2014-01-16/studySample.xml',

            'STUDY_ASSAY_GENOME_SEQ_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                           '/isaconfig-default_v2014-01-16/genome_seq.xml',
            'STUDY_ASSAY_METAGENOME_SEQ_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                               '/isaconfig-default_v2014-01-16/metagenome_seq.xml',
            'STUDY_ASSAY_TRANSCRIPTOME_ANALYSIS_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                                       '/isaconfig-default_v2014-01-16/transcription_seq.xml'

        },
        'ATTRIBUTE_MAPPINGS': {
            'label': 'header',
            'control': 'data-type',
            'required': 'is-required',
            'hidden': 'is-hidden',
            'default_value': '',
            'option_values': '',
            'help_tip': ''
        },
        'CONTROL_MAPPINGS': {
            'String': 'text',
            'Long String': 'textarea',
            'List': 'select'
            # 'Ontology term':?
        }
    },
    'METABOLIGHTS': {

    }
}

# define options for drop-downs
# wrapping items up in lists to maintain order
# for upgrades, only update the label, but the 'value' field should remain intact
# for referencing in codes.
# So, for instance, it would be


DROP_DOWNS = {
    'COLLECTION_TYPES': [
        {
            'value': 'dummy',
            'label': 'Select Collection Type...',
            'description': 'dummy item'
        },
        {
            'value': 'ENA Submission',
            'label': 'ENA Submission',
            'description': 'Submission to the ENA repository'
        },
        {
            'value': 'PDF File',
            'label': 'PDF File',
            'description': ''
        },
        {
            'value': 'Image',
            'label': 'Image',
            'description': ''
        },
        {
            'value': 'Movie',
            'label': 'Movie',
            'description': ''
        },
        {
            'value': 'Other',
            'label': 'Other',
            'description': 'Miscellaneous data file'
        }
    ],
    'STUDY_TYPES': [
        # {
        #     'value': 'dummy',
        #     'label': 'Select Study Type...',
        #     'description': 'dummy item'
        # },
        {
            'value': 'genomeSeq',  # this matches the value defined in the object_model.py
            'label': 'Whole Genome Sequencing',
            'description': 'genome sequencing'
        },
        {
            'value': 'metagenomeSeq',
            'label': 'Metagenomics',
            'description': 'metagenome sequencing'
        },
        {
            'value': 'transcriptomeAnalysis',
            'label': 'Transcriptome Analysis',
            'description': ''
        },
        {
            'value': 'resequencing',
            'label': 'Resequencing',
            'description': ''
        },
        {
            'value': 'epigenetics',
            'label': 'Epigenetics',
            'description': ''
        },
        {
            'value': 'syntheticGenomics',
            'label': 'Synthetic Genomics',
            'description': ''
        },
        {
            'value': 'forensicOrPaleo-genomics',
            'label': 'Forensic or Paleo-genomics',
            'description': ''
        },
        {
            'value': 'geneRegulationStudy',
            'label': 'Gene Regulation Study',
            'description': ''
        },
        {
            'value': 'cancerGenomics',
            'label': 'Cancer Genomics',
            'description': ''
        },
        {
            'value': 'populationGenomics',
            'label': 'Population Genomics',
            'description': ''
        },
        {
            'value': 'rNASeq',
            'label': 'RNASeq',
            'description': ''
        },
        {
            'value': 'exomeSequencing',
            'label': 'Exome Sequencing',
            'description': ''
        },
        {
            'value': 'pooledCloneSequencing',
            'label': 'Pooled Clone Sequencing',
            'description': ''
        },
        {
            'value': 'Other',
            'label': 'Other',
            'description': 'Some random study'
        }
    ]
}

HTML_TAGS = {
    "text": "<label for='{elem_id!s}'>{elem_label!s}</label><br/>"
            "<input type='text' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'>",
    "textarea": "<label for='{elem_id!s}'>{elem_label!s}</label><br/>"
                "<textarea rows='6' cols='40' id='{elem_id!s}'  name='{elem_id!s}'>{elem_value!s}</textarea>",
    "select":  "<select id='{elem_id!s}' name='{elem_id!s}'> {option_values!s} </select>",
    "date": "<label for='{elem_id!s}'>{elem_label!s}</label><br/>"
            "<input type='text' class='pop_date_picker' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'>",
    "hidden": "<input type='hidden' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'>",
    "file": "",
    "Ontology term": "<label for='{elem_id!s}'>{elem_label!s}</label><br/>"
            "<input type='text' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'>"
}
