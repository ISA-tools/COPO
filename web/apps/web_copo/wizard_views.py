__author__ = 'felix.shaw@tgac.ac.uk - 22/09/15'
from django.http import HttpResponse
import jsonpickle
import operator
from dal.copo_base_da import DataSchemas
from dal.ena_da import EnaCollection as da
from error_codes import UI_ERROR_CODES
from web.apps.web_copo.templatetags.html_tags import generate_ena_tags_2

def check_data_file_status(request):
    file_id = request.POST['data_file_id']
    collection_id = request.POST['ena_collection_id']
    study_id = request.POST['study_id']
    result = da().check_data_file_status(collection_id, study_id, file_id)
    request.session['wizard_add_attributes'] = result
    return HttpResponse(jsonpickle.encode({'details': result}))


def process_stage(request):

    # get data from request
    ena_collection_id = request.session['ena_collection_id']
    datafile_id = request.GET['datafile_id']
    study_id = request.GET['study_id']
    last_stage = request.GET['last']
    study_type = request.GET['study_type']
    try:
        prev_question = request.GET['prev_question']
    except:
        prev_question = ''
    try:
        answer = request.GET['answer']
    except:
        answer = ''
    attrib = {'question': prev_question, 'answer': answer}




    # get the ui_template for the required study
    ui_template = DataSchemas("ENA").get_ui_template()
    if not ui_template:
        return HttpResponse(
            UI_ERROR_CODES["TEMPLATE_NOT_FOUND"]
        )

    # create blank field list
    field_track = []

    # get list of attributes which are not hidden
    study_type = ui_template['studies']['study']['assays']['assaysTable'][study_type]
    study_type_sorted = sorted(study_type.items(), key=operator.itemgetter(0))
    for idx in study_type_sorted:
        # deal with non sample fields
        if idx[0] != 'fields':
            f = idx[1]
            if type(f) is dict:
                for field in f['fields']:
                    if field['hidden'] == "false":
                        field_track.append(field)

    r = {'num_steps': len(field_track)}
    # at this point add in create the html for a completed assay set if session flag is set
    if request.session['wizard_add_attributes']:
        request.session['wizard_add_attributes'] = False
        file = da().get_study_datafile(study_id, ena_collection_id, datafile_id)
        for a in file['attributes']:
            for t in field_track:
                if(a['question'] == t['id']):
                    t['default_value'] = a['answer']

        # at this point we have all the default values which have been set so far
        html = []
        for t in field_track:
            if t['default_value'] != '':
                html.append(generate_wizard_html(t))

        r['response'] = 1
        r['detail'] = html
        return HttpResponse(jsonpickle.encode(r))


    if prev_question == '':
        # we are dealing with the first question
        out = generate_wizard_html(field_track[0])
        r['response'] = 1
        r['detail'] = out
        return HttpResponse(jsonpickle.encode(r))

    elif prev_question != '':
        # commit this data to the submission
        da().add_assay_data_to_datafile(study_id, ena_collection_id, datafile_id, attrib)

        # if last stage, simply return
        if last_stage == 'true':
            return HttpResponse(jsonpickle.encode({}))
        for idx in range(0, len(field_track)):
            index = field_track[idx]
            if index['id'] == prev_question:
                out = generate_wizard_html(field_track[idx + 1])
                r['response'] = 1
                r['detail'] = out
                return HttpResponse(jsonpickle.encode(r))

    return HttpResponse(jsonpickle.encode(r))


def generate_wizard_html(field):
    h = {}
    h['id'] = field['id']
    h['title'] = trim_parameter_value_label(field['label'])


    # create html for select type control
    element = generate_ena_tags_2(field['id'], field['default_value'])
    h['element'] = str(element)
    return h


def trim_parameter_value_label(label):
    if "Parameter Value" in label:
        return str.capitalize(label[label.index('[') + 1:label.index(']')])
    else:
        return label
