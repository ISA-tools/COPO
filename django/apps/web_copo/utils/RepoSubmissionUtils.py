__author__ = 'fshaw'
import apps.web_copo.xml_tools.EnaXMLMaker as xml

#utility function to upload data to create XML submission files, upload data to ENA-SRA,
# #submit XML files and return accessions
def submit_ena(c):

    #firstly produce xml_tools submission files. Method should take ENA Submission type Collection and
    #return an dictionary of file paths to the produced xml_tools submission files
    submission_files = xml.make_submissions(c)

    return None