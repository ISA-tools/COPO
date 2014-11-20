__author__ = 'fshaw'

import lxml.etree as etree
import pdb



def get_study_form_controls(path):

    fileHandle = open(path, 'r')
    root = etree.parse(fileHandle)

    namespaces = {'xs':'http://www.w3.org/2001/XMLSchema'}

    descriptor = root.findall(".//xs:element[@name='DESCRIPTOR']//xs:complexType//xs:all/xs:element", namespaces)

    str = ''

    for el in iter(descriptor):
        el_name = el.get('name')
        el_name_tidy = el.get('name').replace('_', ' ').title()
        el_type = el.get('type')
        optional = int(el.get('minOccurs')) == 0

        if(el_type == 'xs:string'):
            str += "<div class='form-group'>"
            str += "<label for='" + el_name + "'>" + el_name_tidy + "</label>"

            if(el.get('name') == 'STUDY_ABSTRACT'):
                str += "<textarea type='text' rows='6' class='form-control' id='" + el_name + "' name='" + el_name + "'/>"
            else:
                str += "<input type='text' class='form-control' id='" + el_name + "' name='" + el_name + "'/>"

            str += "</div>"

        #make dropdown for study type
        if el.get('name') == 'STUDY_TYPE':
            enum = el.findall(".//xs:enumeration", namespaces)
            str += "<div class='form-group'>"
            str += '<label for="' + el_name + '" class="control-label">' + el_name_tidy + '</label>'
            str += "<select class='form-control' name='" + el_name + "' id='" + el_name + "'>"


            for e in iter(enum):
                str += "<option value='" + e.get('value') + "'>" + e.get('value') + "</option>"
            str += "</select>"
            str += "</div>"


    return str

def get_sample_form_controls(path):

    fileHandle = open(path, 'r')
    root = etree.parse(fileHandle)
    namespaces = {'xs':'http://www.w3.org/2001/XMLSchema'}

    sample_name = root.findall("./xs:complexType//xs:element", namespaces)

    str = ''

    for el in iter(sample_name):
        el_name = el.get('name')
        el_name_tidy = el.get('name').replace('_', ' ').title()
        el_type = el.get('type')
        el_required = False
        #pdb.set_trace()
        if(el.get('minOccurs') != None):
            el_required = (int(el.get('minOccurs')) > 0)

        if(el_type == 'xs:string' or el_type == 'xs:int'):
            str += "<div class='form-group'>"
            str += "<label for='" + el_name + "'>" + el_name_tidy + "</label>"
            #pdb.set_trace()
            if el_required:
                str += "<input type='text' class='form-control' id='" + el_name + "' name='" + el_name + "' xml_type='" + el_type + "' required/>"
            else:
                str += "<input type='text' class='form-control' id='" + el_name + "' name='" + el_name + "' xml_type='" + el_type + "'/>"
            str += "</div>"

    return str