__author__ = 'etuka'

from master_settings import PROJ_HOME

# Configuration for ENA submission-type UI template
# Fields assigned here overrides those reported elsewhere
# Every dictionary entry must have the "id" and "ref" keys defined:
# "id", to uniquely identify the element; "ref", to map to ISA config
# Other keys may be added (e.g., "label") to override those defined elsewhere

# Order matters! i.e., the order of listed dictionary items (within each list)
# follows through to the display.

# The path to the files holding the configs are defined below:

CONFIG_FILES = {
    'INVESTIGATION_FILE': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/investigation.json',
    'STUDY_SAMPLE_FILE': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/study_sample.json',
    'STUDY_ASSAY_GENOME_SEQ_FILE': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/assay_genome_seq.json',
    'STUDY_ASSAY_METAGENOME_SEQ_FILE': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/assay_metagenome_seq.json'

}


# Model used for defining output dictionary
# Also provides info on how to access the entries
# For instance, access the elements associated with 'investigation'
# as: investigation.fields, or, investigation.investigationContacts.fields
# or as a dictionary: ['investigation']['fields'].
# The path to the model file is defined in the following json:

MODEL_FILES = {
    'ISA_OBJECT_MODEL': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/object_model.json',
    'ISA_JSON_REFACTOR_TYPES': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/isajson_refactor.json',
    'SAMPLE_ATTRIBUTES': PROJ_HOME + '/web/apps/web_copo/schemas/ena/uimodels/sample_characteristics.json'
}