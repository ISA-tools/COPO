__author__ = 'tonietuk'

from django import template
from django.utils.safestring import mark_safe

import web_copo.copo_maps.utils.data_utils as d_utils
from dal.ena_da import EnaCollection
import web_copo.copo_maps.utils.lookup as lkup

register = template.Library()


@register.filter("generate_ena_tags")
def generate_ena_tags(field_id):
    out_list = get_fields_list(field_id)
    for f in out_list:
        if f["id"] == field_id:
            return mark_safe(do_tag(f))
    return ""  # in order to render 'nothing' if no tag was generated


@register.filter("generate_ena_labels")
def generate_ena_labels(field_id):
    out_list = get_fields_list(field_id)
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
        html_tag += "<table class='table-bordered' id='samples_table'>"

        html_tag += "<tr>"
        for sh in sample_data["headers"][1:]:
            html_tag += "<th>" + sh + "</th>"
        html_tag += "</tr>"

        for sdata in sample_data["data"]:
            html_tag += "<tr>"
            for idx, sd in enumerate(sdata[1:]):
                if idx == 0:
                    html_tag += " <td><a id='samplerow_" + sdata[0] + "' class='sample_edit' href='#'"
                    html_tag += " title = 'Edit Sample' >" + sd + "</a></td>"
                else:
                    html_tag += "<td>" + sd + "</td>"
            html_tag += "</tr>"

        html_tag += "</table>"

    return html_tag


def get_field_order(prop):
    a = {"db_name": "id", "label": "Id"}
    field_order = ["id"]
    headers = ["Id"]

    fields = [a]

    if prop == "studySamples":
        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields

        for f in ena_d:
            headers.append(generate_ena_labels(f.id))
            key_split = f.id.split(".")
            field_order.append(key_split[len(key_split) - 1])
            a = {"db_name": key_split[len(key_split) - 1], "label": generate_ena_labels(f.id)}
            fields.append(a)

        ena_d = d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields

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
        sample_children = get_study_samples_children(ena_collection_id, study_id)
        composite_attributes = [sample_children]  # add contacts, publications, etc to this list
        study_attributes = get_study_attributes_tree(study, composite_attributes)
        a = {
            "id": study_id + "_study",
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + d_utils.lookup_study_type_label(
                study["studyCOPOMetadata"]['studyType']) + ")",
            "state": "closed",
            "attributes": {"txt": study_attributes},
            "children": [
                {
                    "id": study_id + "_study_type_leaf",
                    "text": "Study Type",
                    "state": "open",
                    "attributes": {"txt": ""}
                },
                {
                    "id": study_id + "_studyTitle_leaf",
                    "text": generate_ena_labels("studies.study.studyTitle"),
                    "state": "open",
                    "attributes": {"txt": ""}
                },
                {
                    "id": study_id + "_commentStudyFundingAgency_leaf",
                    "text": generate_ena_labels("studies.study.commentStudyFundingAgency"),
                    "state": "open",
                    "attributes": {"txt": ""}
                },
                {
                    "id": study_id + "_studyDescription_leaf",
                    "text": generate_ena_labels("studies.study.studyDescription"),
                    "state": "open",
                    "attributes": {"txt": ""}
                },
                {
                    "id": study_id + "_samples_leaf",
                    "text": "Samples",
                    "state": "closed",
                    "children": sample_children,
                    "attributes": {"txt": ""}
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
    if isinstance(node, dict):
        for k, v in node.items():
            display_string += "<div>{k!s}: {v!s}</div>".format(**locals())

    elif isinstance(node, list):
        class_name = lkup.CSS_CLASSES["study_tree_data"]
        status_class_name = lkup.CSS_CLASSES["study_tree_data_not_select"]
        for nd in node:
            child_id = nd["id"] + "_div"
            child_id2 = nd["id"] + "_div2"
            child_data = nd["attributes"]["data"]
            display_data = "<div id='{child_id2!s}' class='{status_class_name!s}'></div>".format(**locals())
            display_data += "<div id='{child_id!s}' class='{class_name!s}'>".format(**locals())
            for k, v in child_data.items():
                display_data += "<div>{k!s}: {v!s}</div>".format(**locals())
            display_data += "</div>"
            display_string += display_data
    return display_string


def get_study_attributes_tree(study, composite_attributes):
    # get css styles
    class_name = lkup.CSS_CLASSES["study_tree_data"]
    status_class_name = lkup.CSS_CLASSES["study_tree_data_not_select"]
    list_class_name = lkup.CSS_CLASSES["study_tree_list_label"]
    list_status_class_name = lkup.CSS_CLASSES["study_tree_list_label_select"]

    study_id = study["studyCOPOMetadata"]["id"]

    class_list = [class_name, status_class_name]

    # begin display
    display_string = "<div class='list-group'>"

    # study type
    id_name = study_id + "_study_type_leaf_div"
    id_name2 = study_id + "_study_type_leaf_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        {"Study Type": lookup_study_type_label(study["studyCOPOMetadata"]['studyType'])}) + "</div>"

    # study title
    id_name = study_id + "_studyTitle_leaf_div"
    id_name2 = study_id + "_studyTitle_leaf_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        {generate_ena_labels("studies.study.studyTitle"): study['study']['studyTitle']}) + "</div>"

    # study funding agency
    id_name = study_id + "_commentStudyFundingAgency_leaf_div"
    id_name2 = study_id + "_commentStudyFundingAgency_leaf_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node({
        generate_ena_labels("studies.study.commentStudyFundingAgency"): study['study'][
            'commentStudyFundingAgency']}) + "</div>"

    # study description
    id_name = study_id + "_studyDescription_leaf_div"
    id_name2 = study_id + "_studyDescription_leaf_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node({
        generate_ena_labels("studies.study.studyDescription"): study['study'][
            'studyDescription']}) + "</div>"

    # study samples label
    display_string += "<div class='{list_status_class_name!s}'></div>".format(**locals())
    display_string += "<div class='{list_class_name!s}'><label>Samples</label></div>".format(**locals())
    # study samples data
    display_string += format_tree_node(composite_attributes[0])

    display_string += "</div>"
    return display_string


def get_study_samples_children(ena_collection_id, study_id):
    fields_property = get_field_order("studySamples")
    sample_children = []

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
            sample["attributes"] = {"data": txt, "txt": ""}

            sample_children.append(sample)

    return sample_children


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
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + d_utils.lookup_study_type_label(
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
            "id": study_id,
            "text": study["studyCOPOMetadata"]['studyReference'] + " (" + d_utils.lookup_study_type_label(
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


def get_fields_list(field_id):
    main_dict = d_utils.get_ena_ui_template_as_dict()
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
