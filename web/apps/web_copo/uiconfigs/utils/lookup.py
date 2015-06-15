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
