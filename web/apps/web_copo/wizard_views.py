__author__ = 'felix.shaw@tgac.ac.uk - 22/09/15'
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
import jsonpickle
from dal.copo_base_da import DataSchemas
from error_codes import DB_ERROR_CODES, UI_ERROR_CODES
from django_tools.middlewares import ThreadLocal


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
        for count, index in field_track:
            if index['id'] == prev_question:
                out = generate_wizard_html(field_track[count+1])
                r = {'response': 1, 'detail': out}
                return HttpResponse(jsonpickle.encode(r))
    r = {'response': 0}
    return HttpResponse(jsonpickle.encode(r))


def generate_wizard_html(field):

    h = '<div class="text-center">'
    h += '<div class="lead">Select ' + field['label'] + '</div>'

    # create html for select type control
    if field['control'] == 'select':
        h += '<select' + ' id="' + field['id'] + '"' + ' name="' + field['id'] + '" class="form-control">'
        for o in field['option_values']:
            h += '<option>' + o + '</option>'
        h += '</select>'

    h += '</div>'

    return h