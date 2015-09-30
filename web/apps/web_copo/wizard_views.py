__author__ = 'felix.shaw@tgac.ac.uk - 22/09/15'
from django.http import HttpResponse
import jsonpickle

from dal.copo_base_da import DataSchemas
from error_codes import UI_ERROR_CODES
from web_copo.templatetags.html_tags import generate_ena_tags_2


def get_next_wizard_stage(request):

    # get the ui_template for the required study
    study_type = request.GET['study_type']
    prev_question = request.GET['prev_question']
    ui_template = DataSchemas("ENA").get_ui_template()
    if not ui_template:
        return HttpResponse(
            UI_ERROR_CODES["TEMPLATE_NOT_FOUND"]
        )

    # create blank field list
    field_track = []

    # get list of fields which are not hidden
    study_type = ui_template['studies']['study']['assays']['assaysTable'][study_type]
    for index in study_type:
        field_set = study_type[index]

        if type(field_set) is dict:
            for f in field_set['fields']:
                if f != 'fields' and f['hidden'] == "false":
                    field_track.append(f)



    if prev_question == '':
        # we are dealing with the first question
        out = generate_wizard_html(field_track[1])
        r = {'response': 1, 'detail': out}
        return HttpResponse(jsonpickle.encode(r))
    elif prev_question != '':
        for idx in range(0, len(field_track)):
            index = field_track[idx]
            if index['id'] == prev_question:
                out = generate_wizard_html(field_track[idx+1])
                r = {'response': 1, 'detail': out}
                return HttpResponse(jsonpickle.encode(r))
    r = {'response': 0}
    return HttpResponse(jsonpickle.encode(r))


def generate_wizard_html(field):

    h = {}
    h['id'] = field['id']
    h['title'] = trim_parameter_value_label(field['label'])


    # create html for select type control
    element =  generate_ena_tags_2(field['id'])
    h['element'] = str(element)
    return h


def trim_parameter_value_label(label):
    if "Parameter Value" in label:
        return str.capitalize(label[label.index('[')+1:label.index(']')])
    else:
        return label

