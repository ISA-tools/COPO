__author__ = 'felix.shaw@tgac.ac.uk - 22/09/15'
from django.http import HttpResponse
import jsonpickle

from dal.copo_base_da import DataSchemas
from error_codes import UI_ERROR_CODES
from web.apps.web_copo.templatetags.html_tags import generate_ena_tags_2


def get_next_wizard_stage(request):
    # create session variable for collecting wizard data if not already exist
    collected = request.session.setdefault('collected', {})

    last_stage = request.GET['last']
    if last_stage == 'true':
        # commit this data to the submission
        collection_id = request.session['ena_collection_id']

        return HttpResponse(jsonpickle.encode({}))


    # get the ui_template for the required study
    study_type = request.GET['study_type']
    prev_question = request.GET['prev_question']
    answer = request.GET['answer']

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


    r = {'num_steps': len(field_track)}
    if prev_question == '':
        # we are dealing with the first question
        out = generate_wizard_html(field_track[0])
        r['response'] = 1
        r['detail'] = out
        return HttpResponse(jsonpickle.encode(r))
    elif prev_question != '':
        # store the previous question and answer
        collected[prev_question] = answer
        request.session['collected'] = collected
        print(request.session['collected'])
        for idx in range(0, len(field_track)):
            index = field_track[idx]
            if index['id'] == prev_question:

                out = generate_wizard_html(field_track[idx+1])
                r['response'] = 1
                r['detail'] = out
                return HttpResponse(jsonpickle.encode(r))

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

