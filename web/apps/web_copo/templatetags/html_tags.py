__author__ = 'tonietuk'

from django.utils.safestring import mark_safe
from django import template

from apps.web_copo.mongo.copo_base_da import Collection_Head
import apps.web_copo.uiconfigs.utils.data_formats as dfmts
from apps.web_copo.mongo.ena_da import EnaCollection
import apps.web_copo.uiconfigs.utils.lookup as lkup

register = template.Library()


@register.filter("generate_ena_tags")
def generate_ena_tags(field_id):
    out_list = get_fields_list("ENA", field_id)
    for f in out_list:
        if f["id"] == field_id:
            return mark_safe(do_tag(f))
    return ""  # in order to render 'nothing' if no tag was generated


@register.filter("generate_ena_labels")
def generate_ena_labels(field_id):
    out_list = get_fields_list("ENA", field_id)
    for f in out_list:
        if f["id"] == field_id:
            return f["label"]
    return ""

@register.filter("add_strings")
def add_strings(string_1, string_2):
    return string_1+"/"+string_2

@register.filter("get_sample_type_value")
def get_sample_type_value(param_1, param_2):
    params_split = param_1.split("/")
    study_id = params_split[1]
    study = EnaCollection().GET(study_id)
    sample_types = study["copoInternal"]["sampleTypes"]

    st_dict = {}
    for st in sample_types:
        if st['ref'] == params_split[0]:
            st_dict = st
            break

    key_split = param_2.split(".")
    target_field = key_split[len(key_split) - 1]

    return st[target_field]

@register.filter("get_study_samples")
def get_study_samples(study_type_id, collection_head_id):
    collection_head = Collection_Head().GET(collection_head_id)
    ena_collection_id = str(collection_head['collection_details'])

    collection = EnaCollection().GET(ena_collection_id)
    sample_types = collection["copoInternal"]["sampleTypes"]
    study_samples = collection["copoInternal"]["studySamples"]

    ena_full_json = dfmts.json_to_object(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    ena_d = ena_full_json.studies.study.studySamples.fields

    fields_list = []
    for f in ena_d:
        key_split = f.id.split(".")
        target_field = key_split[len(key_split) - 1]
        fields_list.append(target_field)

    ena_d = ena_full_json.studies.study.studySamples.sampleCollection.fields

    for f in ena_d:
        key_split = f.id.split(".")
        target_field = key_split[len(key_split) - 1]
        fields_list.append(target_field)

    html_tag = ""

    for ss in study_samples:
        if ss['studyType_ref'] == study_type_id and ss['deleted'] == "0":
            for st in sample_types:
                if ss['sampleType_ref'] == st['ref']:
                    study_samples_id = ss['_id']
                    html_tag += "<li>"
                    for f in fields_list:
                        html_tag += st[f] + "/"
            arg = "remove_study_sample/"+study_samples_id
            html_tag += "&nbsp;<a id='"+arg+"' class='type_remove' href='#' title='Remove Sample'>"
            html_tag += "<i class='glyphicon glyphicon-remove'></i></a><br/>"

    return mark_safe(html_tag)


@register.filter("lookup_study_type_label")
def lookup_study_type_label(val):
    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    for st in study_types:
        if st["value"].lower() == val.lower():
            return st["label"]
    return ""


@register.filter("lookup_collection_type_label")
def lookup_collection_type_label(val):
    # get collection types
    collection_types = lkup.DROP_DOWNS['COLLECTION_TYPES']

    for st in collection_types:
        if st["value"].lower() == val.lower():
            return st["label"]
    return ""


def get_fields_list(schema, field_id):
    main_dict = dfmts.json_to_dict(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    out_list = []

    key_split = field_id.split(".")
    fmtout = "main_dict"
    if len(key_split) >= 2:
        order = len(key_split) - 1
        for i in range(0, order):
            fmtout += "['" + key_split[i] + "']"
        fmtout += "['fields']"
        out_list = eval(fmtout)

    return out_list


def do_tag(the_elem):
    elem_id = the_elem["id"]
    elem_label = the_elem["label"]
    elem_value = the_elem["default_value"]
    elem_control = the_elem["control"].lower()
    option_values = ""
    html_tag = ""

    if elem_control == "select" and the_elem["option_values"]:
        for ov in the_elem["option_values"]:
            selected = ""
            if elem_value == ov:
                selected = "selected"
            option_values += "<option value='{ov!s}' {selected!s}>{ov!s}</option>".format(**locals())

    if the_elem["hidden"] == "true":
        html_tag = lkup.HTML_TAGS["hidden"].format(**locals())
    else:
        if elem_control in lkup.HTML_TAGS.keys():
            html_tag = lkup.HTML_TAGS[elem_control].format(**locals())

    return html_tag



#### test snippet
@register.filter("random_table_tag")
def random_table_tag():
    return mark_safe("<tr><td>1</td><td>2</td><td>3</td><td>4</td></tr>")