# define parameters for schemas

from master_settings import PROJ_HOME

SCHEMAS = {
    'ENA': {
        'PATHS_AND_URIS': {
            'ISA_json': PROJ_HOME + '/web/apps/web_copo/copo_maps/ena/dbmodels/isa_ena_model.json',
            'INVESTIGATION_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                  '/isaconfig-default_v2014-01-16/investigation.xml',
            'STUDY_SAMPLE_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                 '/isaconfig-default_v2014-01-16/studySample.xml',

            'STUDY_ASSAY_GENOME_SEQ_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                           '/isaconfig-default_v2014-01-16/genome_seq.xml',
            'STUDY_ASSAY_METAGENOME_SEQ_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                               '/isaconfig-default_v2014-01-16/metagenome_seq.xml',
            'STUDY_ASSAY_TRANSCRIPTOME_ANALYSIS_FILE': 'https://raw.githubusercontent.com/ISA-tools/Configuration-Files/master'
                                                       '/isaconfig-default_v2014-01-16/transcription_seq.xml',

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
        },
        'ENA_DOI_PUBLICATION_MAPPINGS': {
            'studyPublicationTitle': 'dc:title',
            'studyPublicationAuthorList': 'dc:creator',
            'studyPublicationDOI': 'dc:identifier_doi',
            'studyPubMedID': 'dc:identifier_pmid',
            'studyPublicationStatus': 'dc:status'
        }
    },
    'COPO': {
        'PATHS_AND_URIS': {
            'COPO_COLLECTION_HEAD_FILE': PROJ_HOME + '/web/apps/web_copo/copo_maps/copo/dbmodels/collection_head_model.json',
            'ASPERA_COLLECTION': PROJ_HOME + '/web/apps/web_copo/copo_maps/copo/dbmodels/aspera_db_model.json'
        }
    },
    'METABOLIGHTS': {

    }
}  # define options for drop-downs
# wrapping items up in lists to maintain order
# for upgrades, only update the label, but the 'value' field should remain intact
# for referencing in codes.


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
            'value': 'Figshare',
            'label': 'PDF File',
            'description': ''
        },
        {
            'value': 'Figshare',
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
    "text": "<div class='form-group'><label for='{elem_id!s}'>{elem_label!s}</label><br/>"
            "<input class='input-copo form-control' type='text' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'></div>",
    "textarea": "<div class='form-group'><label for='{elem_id!s}'>{elem_label!s}</label><br/>"
                "<textarea class='form-control' rows='6' cols='40' id='{elem_id!s}'  name='{elem_id!s}'>{elem_value!s}</textarea></div>",
    "select": "<div class='form-group'><label for='{elem_id!s}'>{elem_label!s}</label><br/>"
              "<select class='form-control input-copo' id='{elem_id!s}' name='{elem_id!s}'> {option_values!s} </select></div>",
    "date": "<div class='form-group'><label for='{elem_id!s}'>{elem_label!s}</label><br/>"
            "<input type='text' class='pop_date_picker input-copo' id='{elem_id!s}' name='{elem_id!s}' "
            "value='{elem_value!s}'>",
    "hidden": "<input type='hidden' id='{elem_id!s}' name='{elem_id!s}' value='{elem_value!s}'>",
    "file": "",
    "ontology term": "<div class='form-group'><label for='{elem_id!s}'>{elem_label!s}</label><br/>"
                     "<input class='input-copo ontology-field' type='text' id='{elem_id!s}' name='{elem_id!s}' /></div>"
}

# for displaying information/guidance mostly via tooltips
UI_INFO = {
    'study_type_add_info': "Use this form to add new study types",
    'study_type_clone_info': "Use this form to clone existing study types",
    'sample_add_info': "Use this form to add/edit study sample and assign to studies",
    'sample_assign_info': "View allows for assigning samples to current study",
    'sample_unassign_warning': 'Assigned samples about to be deleted!.',
    'publication_add_info': 'Use this form to add a study publication',
    'contact_add_info': 'Use form to add a study contact',
    'publication_doi_resolution': 'Enter a DOI or PubMed ID to be resolved',
    'user_defined_attribute_message': "This will be treated as a user-defined attribute",
    'system_suggested_attribute_message': "This is a system-suggested attribute",
    'files_add_info': 'Use this dialog to specify the specific details of the file you just uploaded',
    'system_suggested_attribute_message': "This is a system-suggested attribute",
    'component_delete_body': "<p>You are about to delete the highlighted {component_name!s}.</p> <p>Do you want to proceed?</p>",
    'component_delete_title': "<h4 class='modal-title'>Confirm <span style='text-transform: capitalize;'>{component_name!s}</span> Delete</h4>",
    'component_unassign_body': "<p>You are about to unassign the highlighted {component_name!s}.</p> <p>Do you want to proceed?</p>",
    'component_unassign_title': "<h4 class='modal-title'>Confirm <span style='text-transform: capitalize;'>{component_name!s}</span> Unassignment</h4>"

}

UI_LABELS = {
    "sample_edit": "Edit Study Sample",
    "sample_add": "Add Study Sample",
    "sample_clone": "Clone Study Sample"
}
