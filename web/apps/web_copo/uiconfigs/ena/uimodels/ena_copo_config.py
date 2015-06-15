__author__ = 'tonietuk'

# Model for bootstrapping UI template creation
# Fields assigned here overrides those inherited elsewhere
# Investigation and Study sample are defined here. Assays, are defined in their respective
# files, given the study type

ELEMENTS = {
    'INVESTIGATION_FILE': {  # elements described in investigation.xml
        'investigation.commentCreatedWithConfiguration': {
            'ref': 'Comment[Created with configuration]'
        },
        'investigation.commentLastOpenedWithConfiguration': {
            'ref': 'Comment[Last Opened With Configuration]'
        },
        'investigation.investigationContacts.investigationPersonLastName': {
            'ref': 'Investigation Person Last Name',
            'label': 'Last Name'
        },
        'investigation.investigationContacts.investigationPersonFirstName': {
            'ref': 'Investigation Person First Name'
        },
        'investigation.investigationContacts.investigationPersonMidInitials': {
            'ref': 'Investigation Person Mid Initials'
        },
        'investigation.investigationContacts.investigationPersonEmail': {
            'ref': 'Investigation Person Email'
        },
        'investigation.investigationContacts.investigationPersonPhone': {
            'ref': 'Investigation Person Phone'
        },
        'investigation.investigationContacts.investigationPersonFax': {
            'ref': 'Investigation Person Fax'
        },
        'investigation.investigationContacts.investigationPersonAddress': {
            'ref': 'Investigation Person Address'
        },
        'investigation.investigationContacts.investigationPersonAffiliation': {
            'ref': 'Investigation Person Affiliation'
        },
        'investigation.investigationContacts.investigationPersonRoles': {
            'ref': 'Investigation Person Roles'
        },
        'investigation.investigationContacts.investigationPersonRolesTermAccessionNumber': {
            'ref': ''
        },
        'investigation.investigationContacts.investigationPersonRolesTermSourceREF': {
            'ref': ''
        },
        'investigation.investigationDescription': {
            'ref': 'Investigation Description'
        },
        'investigation.investigationIdentifier': {
            'ref': 'Investigation Identifier'
        },
        'investigation.investigationPublicReleaseDate': {
            'ref': 'Investigation Public Release Date'
        },
        'investigation.investigationPublications.investigationPubMedID': {
            'ref': 'Investigation PubMed ID'
        },
        'investigation.investigationPublications.investigationPublicationDOI': {
            'ref': 'Investigation Publication DOI'
        },
        'investigation.investigationPublications.investigationPublicationAuthorList': {
            'ref': 'Investigation Publication Author List'
        },
        'investigation.investigationPublications.investigationPublicationTitle': {
            'ref': 'Investigation Publication Title'
        },
        'investigation.investigationPublications.investigationPublicationStatus': {
            'ref': 'Investigation Publication Status'
        },
        'investigation.investigationPublications.investigationPublicationStatusTermAccessionNumber': {
            'ref': ''
        },
        'investigation.investigationPublications.investigationPublicationStatusTermSourceREF': {
            'ref': ''
        },
        'investigation.investigationSubmissionDate': {
            'ref': 'Investigation Submission Date'
        },
        'investigation.investigationTitle': {
            'ref': 'Investigation Title'
        },
        'studies.study.studyIdentifier': {
            'ref': 'Study Identifier'
        },
        'studies.study.studyTitle': {
            'ref': 'Study Title'
        },
        'studies.study.studyDescription': {
            'ref': 'Study Description'
        },
        'studies.study.commentStudyGrantNumber': {
            'ref': 'Comment[Study Grant Number]'
        },
        'studies.study.commentStudyFundingAgency': {
            'ref': 'Comment[Study Funding Agency]'
        },
        'studies.study.studySubmissionDate': {
            'ref': 'Study Submission Date'
        },
        'studies.study.studyPublicReleaseDate': {
            'ref': 'Study Public Release Date'
        },
        'studies.study.studyFileName': {
            'ref': 'Study File Name'
        },
        'studies.study.studyPublications.studyPubMedID': {
            'ref': 'Study PubMed ID'
        },
        'studies.study.studyPublications.investigationPublicationDOI': {
            'ref': 'Study Publication DOI'
        },
        'studies.study.studyPublications.investigationPublicationAuthorList': {
            'ref': 'Study Publication Author List'
        },
        'studies.study.studyPublications.investigationPublicationTitle': {
            'ref': 'Study Publication Title'
        },
        'studies.study.studyPublications.investigationPublicationStatus': {
            'ref': 'Study Publication Status'
        },
        'studies.study.studyPublications.investigationPublicationStatusTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyPublications.investigationPublicationStatusTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyContacts.studyPersonLastName': {
            'ref': 'Study Person Last Name'
        },
        'studies.study.studyContacts.studyPersonFirstName': {
            'ref': 'Study Person First Name'
        },
        'studies.study.studyContacts.studyPersonMidInitials': {
            'ref': 'Study Person Mid Initials'
        },
        'studies.study.studyContacts.studyPersonEmail': {
            'ref': 'Study Person Email'
        },
        'studies.study.studyContacts.studyPersonPhone': {
            'ref': 'Study Person Phone'
        },
        'studies.study.studyContacts.studyPersonFax': {
            'ref': 'Study Person Fax'
        },
        'studies.study.studyContacts.studyPersonAddress': {
            'ref': 'Study Person Address'
        },
        'studies.study.studyContacts.studyPersonAffiliation': {
            'ref': 'Study Person Affiliation'
        },
        'studies.study.studyContacts.studyPersonRoles': {
            'ref': 'Study Person Roles'
        },
        'studies.study.studyContacts.studyPersonRolesTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyContacts.studyPersonRolesTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyFactors.studyFactorName': {
            'ref': 'Study Factor Name'
        },
        'studies.study.studyFactors.studyFactorType': {
            'ref': 'Study Factor Type'
        },
        'studies.study.studyFactors.studyFactorTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyFactors.studyFactorTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyDesignDescriptors.studyDesignType': {
            'ref': 'Study Design Type'
        },
        'studies.study.studyDesignDescriptors.studyDesignTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyDesignDescriptors.studyDesignTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.assays.studyAssayMeasurementType': {
            'ref': 'Study Assay Measurement Type'
        },
        'studies.study.assays.studyAssayFileName': {
            'ref': 'Study Assay File Name'
        },
        'studies.study.assays.studyAssayMeasurementTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.assays.studyAssayMeasurementTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.assays.studyAssayTechnologyPlatform': {
            'ref': 'Study Assay Technology Platform'
        },
        'studies.study.assays.studyAssayTechnologyType': {
            'ref': 'Study Assay Technology Type'
        },
        'studies.study.assays.studyAssayTechnologyTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.assays.studyAssayTechnologyTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolComponentsName': {
            'ref': 'Study Protocol Components Name'
        },
        'studies.study.studyProtocols.studyProtocolComponentsType': {
            'ref': 'Study Protocol Components Type'
        },
        'studies.study.studyProtocols.studyProtocolComponentsTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolComponentsTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolDescription': {
            'ref': 'Study Protocol Description'
        },
        'studies.study.studyProtocols.studyProtocolName': {
            'ref': 'Study Protocol Name'
        },
        'studies.study.studyProtocols.studyProtocolParametersName': {
            'ref': 'Study Protocol Parameters Name'
        },
        'studies.study.studyProtocols.studyProtocolParametersNameTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolParametersNameTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolType': {
            'ref': 'Study Protocol Type'
        },
        'studies.study.studyProtocols.studyProtocolTypeTermAccessionNumber': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolTypeTermSourceREF': {
            'ref': ''
        },
        'studies.study.studyProtocols.studyProtocolURI': {
            'ref': 'Study Protocol URI'
        },
        'studies.study.studyProtocols.studyProtocolVersion': {
            'ref': 'Study Protocol Version'
        }
    },
    'STUDY_SAMPLE_FILE': {  # elements described in studysample.xml
        'studies.study.studySamples.sourceName': {
            'ref': 'Source Name'
        },
        'studies.study.studySamples.organism': {
            'ref': 'Characteristics[organism]'
        },
        'studies.study.studySamples.sampleCollection.sampleName': {
            'ref': 'Sample Name'
        }
    },
    'STUDY_ASSAY_GENOME_SEQ_FILE': {  # elements described in genome_seq.xml
        'studies.study.assays.assaysTable.genomeSeq.sampleName': {
            'ref': 'Sample Name'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidExtraction.extractName': {
            'ref': 'Extract Name'
        },
        'studies.study.assays.assaysTable.genomeSeq.libraryConstruction.librarySource': {
            'ref': 'Parameter Value[library source]'
        },
        'studies.study.assays.assaysTable.genomeSeq.libraryConstruction.libraryStrategy': {
            'ref': 'Parameter Value[library strategy]'
        },
        'studies.study.assays.assaysTable.genomeSeq.libraryConstruction.librarySelection': {
            'ref': 'Parameter Value[library selection]'
        },
        'studies.study.assays.assaysTable.genomeSeq.libraryConstruction.libraryLayout': {
            'ref': 'Parameter Value[library layout]'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.sequencingInstrument': {
            'ref': 'Parameter Value[sequencing instrument]'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.qualityScorer': {
            'ref': 'Parameter Value[quality scorer]'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.baseCaller': {
            'ref': 'Parameter Value[base caller]'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.assayName': {
            'ref': 'Assay Name'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.export': {
            'ref': 'Comment[Export]'
        },
        'studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing.rawDataFile': {
            'ref': 'Raw Data File'
        },
        'studies.study.assays.assaysTable.genomeSeq.sequenceAssembly.normalizationName': {
            'ref': 'Normalization Name'
        },
        'studies.study.assays.assaysTable.genomeSeq.sequenceAssembly.dataTransformationName': {
            'ref': 'Data Transformation Name'
        },
        'studies.study.assays.assaysTable.genomeSeq.sequenceAssembly.derivedDataFile': {
            'ref': 'Derived Data File'
        }
    },
    'STUDY_ASSAY_METAGENOME_SEQ_FILE': {  # elements described in genome_seq.xml
        'studies.study.assays.assaysTable.metagenomeSeq.sampleName': {
            'ref': 'Sample Name'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidExtraction.extractName': {
            'ref': 'Extract Name'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.libraryConstruction.libraryStrategy': {
            'ref': 'Parameter Value[library strategy]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.libraryConstruction.librarySelection': {
            'ref': 'Parameter Value[library selection]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.libraryConstruction.libraryLayout': {
            'ref': 'Parameter Value[library layout]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.libraryConstruction.mid': {
            'ref': 'Parameter Value[mid]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.sequencingInstrument': {
            'ref': 'Parameter Value[sequencing instrument]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.baseCaller': {
            'ref': 'Parameter Value[base caller]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.qualityScorer': {
            'ref': 'Parameter Value[quality scorer]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.assayName': {
            'ref': 'Assay Name'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.export': {
            'ref': 'Comment[Export]'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.nucleicAcidSequencing.rawDataFile': {
            'ref': 'Raw Data File'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.sequenceAssembly.normalizationName': {
            'ref': 'Normalization Name'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.sequenceAssembly.dataTransformationName': {
            'ref': 'Data Transformation Name'
        },
        'studies.study.assays.assaysTable.metagenomeSeq.sequenceAssembly.derivedDataFile': {
            'ref': 'Derived Data File'
        }
    }
}
