__author__ = 'tonietuk'

from django.utils.safestring import mark_safe
from django import template

import web_copo.uiconfigs.utils.data_formats as dfmts
from web_copo.mongo.ena_da import EnaCollection
import web_copo.uiconfigs.utils.lookup as lkup

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


@register.filter("generate_sample_table")
def generate_sample_table(ena_collection_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX calls. for those, use
    # 'generate_sample_table2' function
    return mark_safe(generate_sample_html(ena_collection_id))


def generate_sample_table2(ena_collection_id):
    return generate_sample_html(ena_collection_id)


def generate_sample_html(ena_collection_id):
    html_tag = ""
    ena_collection = EnaCollection().GET(ena_collection_id)
    samples = ena_collection["collectionCOPOMetadata"]["samples"]
    sample_data = get_samples_data(ena_collection_id)

    if samples:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered'>"

        html_tag += "<tr>"
        for sh in sample_data["headers"][1:]:
            html_tag += "<th>" + sh + "</th>"
        html_tag += "</tr>"

        for sdata in sample_data["data"]:
            html_tag += "<tr>"
            for idx, sd in enumerate(sdata[1:]):
                if idx == 0:
                    html_tag += " <td><a id='sampleupdate_" + sdata[0] + "' class='sample_edit' href='#'"
                    html_tag += " title = 'Edit Sample' >" + sd + "</a></td>"
                else:
                    html_tag += "<td>" + sd + "</td>"
            html_tag += "</tr>"

        html_tag += "</table>"

    return html_tag


def get_field_order(prop):
    ena_full_json = dfmts.json_to_object(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    a = {"db_name": "id", "label": "Id"}
    field_order = ["id"]
    headers = ["Id"]

    fields = [a]

    if prop == "studySamples":
        ena_d = ena_full_json.studies.study.studySamples.fields

        for f in ena_d:
            headers.append(generate_ena_labels(f.id))
            key_split = f.id.split(".")
            field_order.append(key_split[len(key_split) - 1])
            a = {"db_name": key_split[len(key_split) - 1], "label": generate_ena_labels(f.id)}
            fields.append(a)

        ena_d = ena_full_json.studies.study.studySamples.sampleCollection.fields

        for f in ena_d:
            headers.append(generate_ena_labels(f.id))
            key_split = f.id.split(".")
            field_order.append(key_split[len(key_split) - 1])
            a = {"db_name": key_split[len(key_split) - 1], "label": generate_ena_labels(f.id)}
            fields.append(a)

    ordered_fields = {"headers": headers,
                      "order": field_order,
                      "dblabel": fields
                      }

    return ordered_fields


def get_samples_data(ena_collection_id):
    ena_collection = EnaCollection().GET(ena_collection_id)
    samples = ena_collection["collectionCOPOMetadata"]["samples"]

    ena_full_json = dfmts.json_to_object(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    ena_d = ena_full_json.studies.study.studySamples.fields

    fields_property = get_field_order("studySamples")

    data = []
    for sample in samples:
        field_values = []
        for f_o in fields_property["order"]:
            field_values.append(sample[f_o])
        data.append(field_values)

    sample_data = {"headers": fields_property["headers"],
                   "references": fields_property["order"],
                   "data": data
                   }

    return sample_data


def get_studies_data(ena_collection_id):
    studies = EnaCollection().get_ena_studies(ena_collection_id)
    study_data = []

    for st in studies:
        study_id = st["studyCOPOMetadata"]["id"]
        a = {"id": study_id,
             "studyType": lookup_study_type_label(st["studyCOPOMetadata"]["studyType"]),
             "studyReference": st["studyCOPOMetadata"]["studyReference"]
             }

        samples = EnaCollection().get_study_samples(ena_collection_id, study_id)
        a["samplescount"] = len(samples)
        study_data.append(a)

    return study_data


def get_studies_tree(ena_collection_id):
    studies = EnaCollection().get_ena_studies(ena_collection_id)
    tree_data = []

    for study in studies:
        study_id = study["studyCOPOMetadata"]["id"]
        study_samples = get_study_samples_tree(ena_collection_id, study_id)
        composite_attributes = [study_samples]
        study_attributes = get_study_attributes_tree(study, composite_attributes)
        a = {
            "id": study_id + "_study",
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + dfmts.lookup_study_type_label(
                study["studyCOPOMetadata"]['studyType']) + ")",
            "state": "closed",
            "attributes": {"txt": study_attributes},
            "children": [
                {
                    "id": study_id + "_study_type_leaf",
                    "text": "Study Type",
                    "state": "open",
                    "attributes": {"txt": study_attributes}
                },
                {
                    "id": study_id + "_studyTitle_leaf",
                    "text": generate_ena_labels("studies.study.studyTitle"),
                    "state": "open",
                    "attributes": {"txt": study_attributes}
                },
                {
                    "id": study_id + "_commentStudyFundingAgency_leaf",
                    "text": generate_ena_labels("studies.study.commentStudyFundingAgency"),
                    "state": "open",
                    "attributes": {"txt": study_attributes}
                },
                {
                    "id": study_id + "_studyDescription_leaf",
                    "text": generate_ena_labels("studies.study.studyDescription"),
                    "state": "open",
                    "attributes": {"txt": study_attributes}
                },
                {
                    "id": study_id + "_samples_leaf",
                    "text": "Samples",
                    "state": "closed",
                    "children": study_samples["sample_children"],
                    "attributes": {"txt": study_attributes}
                },
                {
                    "id": study_id + "_publications",
                    "text": "Publications",
                    "state": "closed",
                    "children": []
                },
                {
                    "id": study_id + "_contacts",
                    "text": "Contacts",
                    "state": "closed",
                    "children": []
                }
            ]
        }

        tree_data.append(a)

    return tree_data


def format_tree_node(node):
    display_string = ""
    for nd in node:
        display_data = "<div class='study-tree-info-display-div'>";
        for k, v in nd.items():
            display_data += "<div><span>" + k + "</span>: " + v + "</div>";
        display_data += "</div>";
        display_string += display_data
    return display_string


def get_study_attributes_tree(study, composite_attributes):
    display_string = ""
    class_name = "study-tree-info-data"  # change or add css classes here
    study_id = study["studyCOPOMetadata"]["id"]

    # type
    id_name = study_id+"_study_type_leaf_div"
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        [{"Study Type": lookup_study_type_label(study["studyCOPOMetadata"]['studyType'])}]) + "</div>"

    # title
    id_name = study_id+"_studyTitle_leaf_div"
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        [{generate_ena_labels("studies.study.studyTitle"): study['study']['studyTitle']}]) + "</div>"

    # funding agency
    id_name = study_id+"_commentStudyFundingAgency_leaf_div"
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node([{
        generate_ena_labels("studies.study.commentStudyFundingAgency"): study['study'][
            'commentStudyFundingAgency']}]) + "</div>"

    # description
    id_name = study_id+"_studyDescription_leaf_div"
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node([{
        generate_ena_labels("studies.study.studyDescription"): study['study'][
            'studyDescription']}]) + "</div>"

    # samples
    id_name = study_id+"_samples_leaf_div"
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals())+"<label>Samples</label><br/>" + format_tree_node(
        composite_attributes[0]["sample_attributes"]) + "</div>"

    return display_string


def get_study_samples_tree(ena_collection_id, study_id):
    fields_property = get_field_order("studySamples")
    sample_children = []
    sample_attributes = []

    samples = EnaCollection().get_study_samples(ena_collection_id, study_id)

    for idx, sd in enumerate(samples):
        sample_details = EnaCollection().get_ena_sample(ena_collection_id, sd["id"])

        if sample_details:
            sample = {"id": study_id + "_" + sd['id'] + "_sample_leaf",
                      "state": "open"}
            txt = {}

            for f_o in fields_property["dblabel"][1:]:
                txt[f_o["label"]] = sample_details[f_o["db_name"]]

            sample["text"] = idx
            sample["attributes"] = {"txt": ""}

            sample_attributes.append(txt)
            sample_children.append(sample)

    return {"sample_children": sample_children, "sample_attributes": sample_attributes}


def get_study_sample_tree(ena_collection_id):
    studies = EnaCollection().get_ena_studies(ena_collection_id)
    ena_studies = []

    parent_node = {
        "id": "all_studies",
        "text": "All studies",
        "state": "closed"
    }

    for study in studies:
        study_id = study["studyCOPOMetadata"]["id"]
        a = {
            "id": study_id,
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + dfmts.lookup_study_type_label(
                study["studyCOPOMetadata"]['studyType']) + ")",
            "state": "open"
        }

        ena_studies.append(a)

    parent_node["children"] = ena_studies
    return [parent_node]


def get_study_sample_tree_restrict(ena_collection_id, sample_id):
    studies = EnaCollection().get_ena_studies(ena_collection_id)
    ena_studies = []

    parent_node = {
        "id": "all_studies",
        "text": "All studies",
        "state": "closed"
    }

    for study in studies:
        study_id = study["studyCOPOMetadata"]["id"]

        a = {
            "id": study_id + "_study",
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + dfmts.lookup_study_type_label(
                study["studyCOPOMetadata"]['studyType']) + ")",
            "state": "open"
        }

        samples = EnaCollection().get_study_samples(ena_collection_id, study_id)

        if any(d['id'] == sample_id for d in samples):
            a["checked"] = True
        ena_studies.append(a)

    parent_node["children"] = ena_studies
    return [parent_node]


@register.filter("lookup_study_type_label")
def lookup_study_type_label(val):
    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    for st in study_types:
        if st["value"].lower() == val.lower():
            return st["label"]
    return ""


@register.filter("lookup_info")
def lookup_info(val):
    if val in lkup.UI_INFO.keys():
        return lkup.UI_INFO[val]
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
    main_dict = dfmts.json_to_dict(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
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


@register.filter("study_type_drop_down")
def study_type_drop_down(curr_val):
    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    option_values = ""
    for stud in study_types:
        sv = stud["value"]
        sl = stud["label"]
        selected = ""
        if curr_val == sv:
            selected = "selected"
        option_values += "<option value='{sv!s}' {selected!s}>{sl!s}</option>".format(**locals())

    return mark_safe(option_values)


def do_tag(the_elem):
    elem_id = the_elem["id"]
    elem_label = the_elem["label"]
    elem_value = the_elem["default_value"]
    elem_control = the_elem["control"].lower()
    option_values = ""
    html_tag = ""

    html_all_tags = lkup.HTML_TAGS

    if elem_control == "select" and the_elem["option_values"]:
        for ov in the_elem["option_values"]:
            selected = ""
            if elem_value == ov:
                selected = "selected"
            option_values += "<option value='{ov!s}' {selected!s}>{ov!s}</option>".format(**locals())

    if the_elem["hidden"] == "true":
        html_tag = html_all_tags["hidden"].format(**locals())
    else:
        if elem_control in [x.lower() for x in list(html_all_tags.keys())]:
            html_tag = html_all_tags[elem_control].format(**locals())

    return html_tag