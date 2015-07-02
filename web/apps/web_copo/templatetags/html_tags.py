from pprint import pprint
from django.utils.safestring import mark_safe

__author__ = 'tonietuk'
from django import template
import apps.web_copo.uiconfigs.utils.data_formats as dfmts
import apps.web_copo.uiconfigs.utils.lookup as lkup

register = template.Library()

@register.filter("generate_ena_tags")
def generate_ena_tags(field_id, ref):
    print(ref)
    schema = "ENA"
    main_dict = dfmts.json_to_dict(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    out_dict = {}

    key_split = field_id.split(".")
    fmtout = "main_dict"
    if len(key_split) >= 2:
        order = len(key_split) - 1
        for i in range(0, order):
            fmtout += "['" + key_split[i] + "']"
        fmtout += "['fields']"
        out_dict = eval(fmtout)

    for f in out_dict:
        if f["id"] == field_id:
            return mark_safe(do_tag(f, ref))
    return ""


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


def do_tag(the_elem, ref):
    elem_id = the_elem["id"]+"_"+str(ref)
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
