__author__ = 'fshaw'

import lxml.etree as etree
import pdb


class EnaStudyForm:
    # simple class to return parsed data
    def __init__(self, n=None, tn=None, t=None, values=[]):
        self.name = n
        self.tidy_name = tn
        self.type = t
        self.values = []


def get_study_form_controls(path):
    fileHandle = open(path, 'r')
    root = etree.parse(fileHandle)

    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}

    descriptor = root.findall(".//xs:element[@name='DESCRIPTOR']//xs:complexType//xs:all/xs:element", namespaces)

    str = ''

    # out is an array of EnaStudyForm objects
    out = []

    for el in iter(descriptor):
        el_name = el.get('name')
        el_name_tidy = el.get('name').replace('_', ' ').title()
        el_type = el.get('type')
        optional = int(el.get('minOccurs')) == 0
        ena = EnaStudyForm()
        ena.name = el_name
        ena.tidy_name = el_name_tidy

        if (el_type == 'xs:string'):

            if (el.get('name') == 'STUDY_ABSTRACT'):
                ena.type = 'textarea'
                out.append(ena)
            else:
                ena.type = 'input'
                out.append(ena)


        #make dropdown for study type
        if el.get('name') == 'STUDY_TYPE':
            enum = el.findall(".//xs:enumeration", namespaces)
            ena.type = 'select'
            for e in iter(enum):
                ena.values.append(e.get('value'))
                #str += "<option value='" + e.get('value') + "'>" + e.get('value') + "</option>"
            out.append(ena)
            #str += "</select>"
            #str += "</div>"
    return out


def get_sample_form_controls(path):
    fileHandle = open(path, 'r')
    root = etree.parse(fileHandle)
    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}

    sample_name = root.findall("./xs:complexType//xs:element", namespaces)

    str = ''

    for el in iter(sample_name):
        el_name = el.get('name')
        el_name_tidy = el.get('name').replace('_', ' ').title()
        el_type = el.get('type')
        el_required = False
        # pdb.set_trace()
        if (el.get('minOccurs') != None):
            el_required = (int(el.get('minOccurs')) > 0)

        if (el_type == 'xs:string' or el_type == 'xs:int'):
            str += "<div class='form-group'>"
            str += "<label for='" + el_name + "'>" + el_name_tidy + "</label>"
            #pdb.set_trace()
            if el_required:
                str += "<input type='text' class='form-control' id='" + el_name + "' name='" + el_name + "' xml_type='" + el_type + "' required/>"
            else:
                str += "<input type='text' class='form-control' id='" + el_name + "' name='" + el_name + "' xml_type='" + el_type + "'/>"
            str += "</div>"

    return str


def get_library_dropdown(xml_file, lib_part):
    # method to get html for library strategy dropdown
    fileHandle = open(xml_file, 'r')
    root = etree.parse(fileHandle)
    namespaces = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    search_str = ".//xs:element[@name=\"" + lib_part + "\"]//xs:enumeration"
    options = root.findall(search_str, namespaces)
    out = ''
    for o in options:
        out += '<option>' + o.get('value') + '</option>'
    return out