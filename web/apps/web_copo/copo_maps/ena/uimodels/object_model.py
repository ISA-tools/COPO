__author__ = 'tonietuk'

# Model used for defining output dictionary
# Also provides info on how to access the entries
# For instance, access the elements associated with 'investigation'
# as: investigation.fields, or, investigation.investigationContacts.fields
# or as a dictionary: ['investigation']['fields']
OUT_DICT = {
    "investigation": {
        "fields": [],
        "investigationContacts": {
            "fields": []
        },
        "investigationPublications": {
            "fields": []
        }
    },
    "studies": {
        "fields": [],
        "study": {
            "fields": [],
            "studyContacts": {
                "fields": []
            },
            "studyPublications": {
                "fields": []
            },
            "studyFactors": {
                "fields": []
            },
            "studyDesignDescriptors": {
                "fields": []
            },
            "assays": {
                "fields": [],
                "assaysTable": {
                    "fields": [],
                    "genomeSeq": {
                        "fields": [],
                        "nucleicAcidExtraction": {
                            "fields": []
                        },
                        "libraryConstruction": {
                            "fields": []
                        },
                        "nucleicAcidSequencing": {
                            "fields": []
                        },
                        "sequenceAssembly": {
                            "fields": []
                        }
                    },
                    "metagenomeSeq": {
                        "fields": [],
                        "nucleicAcidExtraction": {
                            "fields": []
                        },
                        "libraryConstruction": {
                            "fields": []
                        },
                        "nucleicAcidSequencing": {
                            "fields": []
                        },
                        "sequenceAssembly": {
                            "fields": []
                        }
                    }
                }
            },
            "studyProtocols": {
                "fields": []
            },
            "studySamples": {
                "fields": [],
                "sampleCollection": {
                    "fields": []
                }
            }
        }
    }}
