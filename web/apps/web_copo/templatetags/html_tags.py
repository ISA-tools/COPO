__author__ = 'tonietuk'

import datetime
from django import template
from django.utils.safestring import mark_safe

import web.apps.web_copo.copo_maps.utils.data_utils as d_utils
from dal.ena_da import EnaCollection
import web.apps.web_copo.copo_maps.utils.lookup as lkup
from chunked_upload.models import ChunkedUpload
import web.apps.web_copo.utils.EnaUtils as u

register = template.Library()


# given an ENA-based field id, generates the html tag corresponding to the definition in the config
@register.filter("generate_ena_tags")
def generate_ena_tags(field_id):
    return mark_safe(generate_tag(field_id))


# similar to the 'generate_ena_tags' method, but...
# this handles calls from other routes (e.g., AJAX) besides Django
def generate_ena_tags2(field_id):
    return generate_tag(field_id)


def generate_tag(field_id):
    html_tag = ""
    out_list = get_fields_list(field_id)
    for f in out_list:
        if f["id"] == field_id:
            html_tag = mark_safe(do_tag(f))
            break
    return html_tag


@register.filter("generate_ena_labels")
def generate_ena_labels(field_id):
    out_list = get_fields_list(field_id)
    label = ""
    for f in out_list:
        if f["id"] == field_id:
            label = f["label"]
            break
    return label


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
    sample_data = get_samples_data(ena_collection_id)

    if sample_data["data"]:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered' id='samples_table'>"

        html_tag += "<tr>"
        for sh in sample_data["headers"][1:]:
            html_tag += "<th>" + sh + "</th>"
        html_tag += "<th>Attributes</th>"
        html_tag += "<th>&nbsp;</th>"
        html_tag += "</tr>"

        for sdata in sample_data["data"]:
            html_tag += "<tr>"

            for idx, sd in enumerate(sdata[1:]):
                html_tag += "<td>" + sd + "</td>"

            html_tag += " <td>"
            attribute_data = generate_sample_characteristics_html(ena_collection_id, sdata[0])

            html_tag += " <span class='popinfo' data-popinfo-title='Sample Attributes' data-popinfo-trigger='click'>"
            html_tag += " <button title='click for attributes' class='btn btn-xs btn-info' type='button'><span class='fa fa-info-circle'></span></button>"
            html_tag += " <span class='popinfo-content' style='display: none'>{attribute_data!s}</span>".format(
                **locals())
            html_tag += " </span>"
            html_tag += " </td>"

            html_tag += " <td>"
            row_id = "samplerowclonespan_" + sdata[0]
            html_tag += " <span data-toggle='tooltip' title='Clone Sample'> ".format(**locals())
            html_tag += " <a id='{row_id!s}' class='sample-clone' href='#'>".format(**locals())
            html_tag += " <i class='fa fa-clone fa-sm copo-icon-primaryr'></i></a>"
            html_tag += " </span>&nbsp;"

            html_tag += " <span data-toggle='tooltip' title='Update Sample'> "

            row_id = "samplerowupdatespan_" + sdata[0]
            html_tag += " <a id='{row_id!s}' class='sample-edit' href='#'>".format(**locals())
            html_tag += " <i class='fa fa-pencil-square-o fa-sm copo-icon-success'></i></a>"
            html_tag += " </span>"
            html_tag += " </td>"
            html_tag += "</tr>"

        html_tag += "</table>"

    return html_tag


def generate_sample_characteristics_html(ena_collection_id, sample_id):
    characteristics = EnaCollection().get_ena_sample(ena_collection_id, sample_id)["characteristics"]
    html_tag = "No attributes data!"
    if len(characteristics) > 1:  # if we have any other characteristics besides the organism

        header_class = "Headingx"
        cell_class = "Cellx"
        row_class = "Rowx"

        html_tag = "<div class='Tablex'>"
        html_tag += "<div class='{header_class!s}'>".format(**locals())
        html_tag += "<div class='{cell_class!s}'><p>term</p></div>".format(**locals())
        html_tag += "<div class='{cell_class!s}'><p>value</p></div>".format(**locals())
        html_tag += "<div class='{cell_class!s}'><p>unit</p></div>".format(**locals())
        html_tag += "</div>"
        for att in characteristics[1:]:
            term = att["categoryTerm"]
            value = att["characteristics"]
            unit = "n/a"
            if "unit" in att:
                unit = att["unit"]
            html_tag += "<div class='{row_class!s}'>".format(**locals())
            html_tag += "<div class='{cell_class!s}'><p>{term!s}</p></div>".format(**locals())
            html_tag += "<div class='{cell_class!s}'><p>{value!s}</p></div>".format(**locals())
            html_tag += "<div class='{cell_class!s}'><p>{unit!s}</p></div>".format(**locals())
            html_tag += "</div>"
        html_tag += "</div>"
    return html_tag


def generate_file_attributes(file_id):
    chunked_upload = ChunkedUpload.objects.get(id=int(file_id))

    header_class = "Headingx"
    cell_class = "Cellx"
    row_class = "Rowx"

    size = u.filesize_toString(chunked_upload.offset)

    uploaded_on = (str(chunked_upload.completed_on)).split(".")[0]
    dt_format1 = '%Y-%m-%d %H:%M:%S'
    dt_format2 = '%d-%m-%Y %H:%M:%S'
    uploaded_on = datetime.datetime.strptime(str(uploaded_on), dt_format1).strftime(dt_format2)
    hash = chunked_upload.hash

    html_tag = "<div class='Tablex'>"
    # row
    html_tag += "<div class='{row_class!s}'>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p><strong>Size:</strong></p></div>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p>{size!s}</p></div>".format(**locals())
    html_tag += "</div>"
    # row
    html_tag += "<div class='{row_class!s}'>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p><strong>Uploaded on:</strong></p></div>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p>{uploaded_on!s}</p></div>".format(**locals())
    html_tag += "</div>"
    # row
    html_tag += "<div class='{row_class!s}'>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p><strong>Hash:</strong></p></div>".format(**locals())
    html_tag += "<div class='{cell_class!s}'><p>{hash!s}</p></div>".format(**locals())
    html_tag += "</div>"

    html_tag += "</div>"

    return html_tag


@register.filter("generate_study_samples_table")
def generate_study_samples_table(ena_collection_id, study_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX calls. for such other calls,
    # use the 'generate_study_samples_table2' function
    return mark_safe(generate_study_samples_html(ena_collection_id, study_id))


def generate_study_samples_table2(ena_collection_id, study_id):
    return generate_study_samples_html(ena_collection_id, study_id)


def generate_study_samples_html(ena_collection_id, study_id):
    html_tag = ""
    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields,
                d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields]
    fields_property = get_field_order(segments)
    samples = EnaCollection().get_study_samples(ena_collection_id, study_id)

    if samples:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered'>"

        html_tag += " <tr>"
        for f_o in fields_property["dblabel"][1:]:
            html_tag += " <th>" + f_o["label"] + "</th>"
        html_tag += " <th>&nbsp;</th>"
        html_tag += " </tr>"

        for sd in samples:
            sample_id = sd["id"]
            sample_details = EnaCollection().get_ena_sample(ena_collection_id, sample_id)
            if sample_details:
                html_tag += " <tr id='{sample_id!s}_sample_row'>".format(**locals())
                for f_o in fields_property["dblabel"][1:]:
                    v = sample_details[f_o["db_name"]]
                    html_tag += " <td>{v!s}</td>".format(**locals())
                html_tag += "<td>"
                html_tag += " <span data-toggle='tooltip' title='Delete Sample'><a target-component='sample' target-id='{sample_id!s}' target-title='sample' class='component-row-delete' ".format(
                    **locals())
                html_tag += " data-toggle='modal' data-target='#studyComponentsDeleteModal' href='#'>"
                html_tag += " <i class='fa fa-trash-o fa-sm copo-icon-danger'></i></a>"
                html_tag += " </span>"

                html_tag += " </td>"
                html_tag += "</tr>"
        html_tag += "</table>"

    return html_tag


@register.filter("generate_study_data_table")
def generate_study_data_table(ena_collection_id, study_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX calls. for such other calls,
    # use the 'generate_study_data_table2' function
    return mark_safe(generate_study_data_html(ena_collection_id, study_id))


def generate_study_data_table2(ena_collection_id, study_id):
    return generate_study_data_html(ena_collection_id, study_id)


def generate_study_data_html(ena_collection_id, study_id):
    html_tag = ""
    datafiles = EnaCollection().get_study_datafiles(ena_collection_id, study_id)

    if datafiles:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered'>"
        html_tag += "<col width='50%'/>"
        html_tag += "<col width='45%'/>"
        html_tag += "<col width='5%'/>"

        html_tag += "<tr>"
        html_tag += "<th>File</th>"
        html_tag += "<th>Sample</th>"
        html_tag += "<th>Actions</th>"
        html_tag += "</tr>"

        for df in datafiles:
            data_file_id = df["id"]  # id of the record
            data_file_samples = df["samples"]  # samples
            df_file_id = df["fileId"]  # file id

            # get samples assigned to this study to populate list
            samples = EnaCollection().get_study_samples(ena_collection_id, study_id)
            samples_html_tag = ""
            for sd in samples:
                sample_id = sd["id"]
                # get details of sample
                sample_details = EnaCollection().get_ena_sample(ena_collection_id, sample_id)
                if sample_details:
                    selected = ""
                    sample_name = sample_details["sampleName"]
                    item_value = data_file_id + "," + sample_id
                    if sample_id in data_file_samples:
                        selected = "selected"
                    samples_html_tag += " <option value='{item_value!s}' {selected!s}>{sample_name!s}</option>".format(
                        **locals())

            html_tag += "<tr id='{data_file_id!s}_datafile_row'>".format(**locals())

            # get details of the file from the file object
            chunked_upload = ChunkedUpload.objects.get(id=int(df_file_id))

            # get file attributes from chunked upload
            attribute_data = generate_file_attributes(df_file_id)

            html_tag += " <td>"
            html_tag += " <div style='display: inline-block;'>" + chunked_upload.filename + "</div>"
            html_tag += " <div style='display: inline-block;'>"
            html_tag += " <span class='popinfo' data-popinfo-title='File Attributes' data-popinfo-trigger='hover'>"
            html_tag += " <a href='#' class='data-file-attribute'><i class='fa fa-info-circle'></i></a>"
            html_tag += " <span class='popinfo-content' style='display: none'>{attribute_data!s}</span>".format(
                **locals())
            html_tag += " </span>"
            html_tag += " </div>"
            html_tag += "</td>"

            html_tag += "<td>"
            html_tag += "<div class='control-group'>"

            html_tag += "<select class='file-sample-select' multiple placeholder='Attach Sample...'>"
            html_tag += "<option value=""></option>"
            html_tag += samples_html_tag
            html_tag += "</select>"
            html_tag += "</div>"

            html_tag += "</td>"

            html_tag += "<td>"
            html_tag += "<div class='dropdown'>"
            html_tag += "<button class='btn btn-primary btn-sm dropdown-toggle' title='click for actions' type='button' data-toggle='dropdown'>"
            html_tag += "<span class='caret'></span></button>"
            html_tag += "<ul class='dropdown-menu'>"
            html_tag += " <li data-toggle='tooltip' title='Describe Data File'><a target-id='{data_file_id!s}' class='experiment-describe' ".format(
                **locals())
            html_tag += " data-toggle='modal' data-target='#sampleDescriptionModal' href='#'>"
            html_tag += " <i class='fa fa-tags fa-sm copo-icon-info'></i></a>"
            html_tag += " </li>"
            html_tag += " <li data-toggle='tooltip' title='Send to Dropbox'><a target-id='{data_file_id!s}' class='repo-upload' ".format(
                **locals())
            html_tag += " href='#'>"
            html_tag += " <i class='fa fa-cloud fa-sm copo-icon-primary'></i></a>"
            html_tag += " </li>"

            component_name = "data file"
            component_message = lkup.UI_INFO["component_delete_body"].format(**locals())
            component_title = lkup.UI_INFO["component_delete_title"].format(**locals())
            component_title = "Welcome"

            html_tag += " <li data-toggle='tooltip' title='Delete Data File'><a target-name='datafile' target-id='{data_file_id!s}' component-message='{component_message!s}' component-title='{component_title!s}' class='component-row-delete' ".format(
                **locals())
            html_tag += " data-toggle='modal' data-target='#studyComponentsDeleteModal' href='#'><div class='themess' style='display: none'>{component_title2!s}</div>".format(**locals())
            html_tag += " <i class='fa fa-trash-o fa-sm copo-icon-danger'></i></a>"
            html_tag += " </li>"
            html_tag += "</ul></div>"
            html_tag += "</td>"

            html_tag += "</tr>"

        html_tag += "</table>"

    return html_tag


@register.filter("generate_study_publications_table")
def generate_study_publications_table(ena_collection_id, study_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX. for such other calls,
    # use the 'generate_study_publications_table2' function
    return mark_safe(generate_study_publications_html(ena_collection_id, study_id))


def generate_study_publications_table2(ena_collection_id, study_id):
    return generate_study_publications_html(ena_collection_id, study_id)


def generate_study_publications_html(ena_collection_id, study_id):
    html_tag = ""

    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studyPublications.fields]
    fields_property = get_field_order(segments)

    publications = EnaCollection().get_study_publications(study_id, ena_collection_id)

    if publications:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered' id='study_publications_table'>"

        html_tag += " <tr>"
        for f_o in fields_property["dblabel"][1:]:
            if f_o["label"]:
                html_tag += " <th>" + f_o["label"] + "</th>"
        html_tag += " <th>&nbsp;</th>"
        html_tag += " </tr>"

        for pb in publications:
            publication_id = pb["id"]
            html_tag += " <tr id='{publication_id!s}_publication_row'>".format(**locals())
            for f_o in fields_property["dblabel"][1:]:
                if f_o["label"]:
                    v = pb[f_o["db_name"]]
                    html_tag += " <td>{v!s}</td>".format(**locals())
            html_tag += "<td>"

            html_tag += " <span data-toggle='tooltip' title='Delete Publication'><a target-component='publication' target-id='{publication_id!s}' target-title='publication' class='component-row-delete' ".format(
                **locals())
            html_tag += " data-toggle='modal' data-target='#studyComponentsDeleteModal' href='#'>"
            html_tag += " <i class='fa fa-trash-o fa-sm copo-icon-danger'></i></a>"
            html_tag += " </span>"

            html_tag += " </td>"
            html_tag += "</tr>"
        html_tag += "</table>"

    return html_tag


@register.filter("generate_study_contacts_table")
def generate_study_contacts_table(ena_collection_id, study_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX. for such other calls,
    # use the 'generate_study_contact_table2' function
    return mark_safe(generate_study_contacts_html(ena_collection_id, study_id))


def generate_study_contacts_table2(ena_collection_id, study_id):
    return generate_study_contacts_html(ena_collection_id, study_id)


def generate_study_contacts_html(ena_collection_id, study_id):
    html_tag = ""

    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studyContacts.fields]
    fields_property = get_field_order(segments)

    contacts = EnaCollection().get_study_contacts(study_id, ena_collection_id)

    if contacts:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered' id='study_contacts_table'>"

        html_tag += " <tr>"
        for f_o in fields_property["dblabel"][1:]:
            if f_o["label"]:
                html_tag += " <th>" + f_o["label"] + "</th>"
        html_tag += " <th>&nbsp;</th>"
        html_tag += " </tr>"

        for pb in contacts:
            contact_id = pb["id"]
            html_tag += " <tr id='{contact_id!s}_contact_row'>".format(**locals())
            for f_o in fields_property["dblabel"][1:]:
                if f_o["label"]:
                    v = pb[f_o["db_name"]]
                    html_tag += " <td>{v!s}</td>".format(**locals())
            html_tag += "<td>"

            html_tag += " <span data-toggle='tooltip' title='Delete Contact'><a target-component='contact' target-id='{contact_id!s}' target-title='contact' class='component-row-delete' ".format(
                **locals())
            html_tag += " data-toggle='modal' data-target='#studyComponentsDeleteModal' href='#'>"
            html_tag += " <i class='fa fa-trash-o fa-sm copo-icon-danger'></i></a>"
            html_tag += " </span>"

            html_tag += " </td>"
            html_tag += "</tr>"
        html_tag += "</table>"

    return html_tag


# segments is a list of end-points, i.e. list of grouped fields from the ui config
# e.g., studies.study.studySamples.fields
def get_field_order(segments):
    a = {"db_name": "id", "label": "Id"}
    field_order = ["id"]
    headers = ["Id"]

    fields = [a]

    for sg in segments:
        for f in sg:
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
    samples = EnaCollection().get_all_samples(ena_collection_id)

    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields,
                d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields]
    fields_property = get_field_order(segments)

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


@register.filter("generate_study_table")
def generate_study_table(ena_collection_id):
    # serves Django template via the mark_safe pipe
    # not necessarily supported by calls via other routes e.g., AJAX calls. for those, use
    # 'generate_sample_table2' function
    return mark_safe(generate_study_html(ena_collection_id))


def generate_study_table2(ena_collection_id):
    return generate_study_html(ena_collection_id)


def generate_study_html(ena_collection_id):
    html_tag = ""
    row_class = 'study-table-row'
    study_data = get_studies_data(ena_collection_id)

    if study_data:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered' id='study_table'>"
        html_tag += "<tr>"
        html_tag += "<th>Study Reference</th>"
        html_tag += "<th>Study Type</th>"
        html_tag += "<th># Samples</th>"
        html_tag += "<th>&nbsp;</th>"
        html_tag += "</tr>"

        for sd in study_data:
            study_id = sd["id"]
            row_id = study_id + "_study_row"
            delete_id = study_id + "_st_delete"
            study_reference = sd["studyReference"]
            study_type = sd["studyType"]
            samples_count = sd["samplescount"]
            edit_link = "/copo/study/" + study_id + "/view"

            html_tag += " <tr class='{row_class!s}' id='{row_id!s}'>".format(**locals())
            html_tag += " <td><a href='{edit_link!s}'>{study_reference!s}</a></td>".format(**locals())
            html_tag += " <td>{study_type!s}</td>".format(**locals())
            html_tag += " <td>{samples_count!s}</td>".format(**locals())
            html_tag += " <td>"

            html_tag += " <span data-toggle='tooltip' title='Update Study'> "
            html_tag += " <a href='{edit_link!s}'>".format(**locals())
            html_tag += " <i class='fa fa-pencil-square-o fa-sm copo-icon-success'></i></a>"
            html_tag += " </span>&nbsp;"

            html_tag += " <span data-toggle='tooltip' title='Delete Study'><a id='{delete_id!s}' class='study-delete' ".format(
                **locals())
            html_tag += " data-toggle='modal' data-target='#studyDeleteModal' custom-data-reference='{study_reference!s}' custom-data-type='{study_type!s}' href='#'>".format(
                **locals())
            html_tag += " <i class='fa fa-trash-o fa-sm copo-icon-danger'></i></a>"
            html_tag += " </span>"

            html_tag += " </td>"
            html_tag += " </tr>"
        html_tag += " </table>"

    return html_tag


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
                    "id": study_id + "_studyType",
                    "text": "Study Type",
                    "state": "open",
                    "attributes": {"txt": "", "label": lookup_study_type_label(
                        study["studyCOPOMetadata"]['studyType']), "value": study["studyCOPOMetadata"]['studyType']}
                },
                {
                    "id": study_id + "_studyTitle",
                    "text": generate_ena_labels("studies.study.studyTitle"),
                    "state": "open",
                    "attributes": {"txt": "", "label": study['study']['studyTitle'],
                                   "value": study['study']['studyTitle']}
                },
                {
                    "id": study_id + "_commentStudyFundingAgency",
                    "text": generate_ena_labels("studies.study.commentStudyFundingAgency"),
                    "state": "open",
                    "attributes": {"txt": "", "label": study['study']['commentStudyFundingAgency'],
                                   "value": study['study']['commentStudyFundingAgency']}
                },
                {
                    "id": study_id + "_studyDescription",
                    "text": generate_ena_labels("studies.study.studyDescription"),
                    "state": "open",
                    "attributes": {"txt": "", "label": study['study']['studyDescription'],
                                   "value": study['study']['studyDescription']}
                },
                {
                    "id": study_id + "_samples",
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
            display_string += "<div><span class='study-node-title'>{k!s}</span>: {v!s}</div>".format(**locals())

    elif isinstance(node, list):
        class_name = "study-node-data"
        status_class_name = "study-view-select-status"
        for nd in node:
            child_id = nd["id"] + "_div"
            child_id2 = nd["id"] + "_div2"
            child_data = nd["attributes"]["data"]
            display_data = "<div id='{child_id2!s}' class='{status_class_name!s}'></div>".format(**locals())
            display_data += "<div id='{child_id!s}' class='{class_name!s}'>".format(**locals())
            display_data += nd["attributes"]["label"]
            display_data += "</div>"
            display_string += display_data
    return display_string


def get_study_attributes_tree(study, composite_attributes):
    # define css styles
    class_name = "study-node-data"
    status_class_name = "study-view-select-status"
    list_class_name = "study-node-list-data"
    list_status_class_name = "study-list-status"

    study_id = study["studyCOPOMetadata"]["id"]

    class_list = [class_name, status_class_name]

    # begin display
    display_string = "<div class='list-group'>"

    # study type
    id_name = study_id + "_studyType_div"
    id_name2 = study_id + "_studyType_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        {"<span class='study-node-title'>Study Type</span>": lookup_study_type_label(
            study["studyCOPOMetadata"]['studyType'])}) + "</div>"

    # study title
    id_name = study_id + "_studyTitle_div"
    id_name2 = study_id + "_studyTitle_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node(
        {generate_ena_labels("studies.study.studyTitle"): study['study']['studyTitle']}) + "</div>"

    # study funding agency
    id_name = study_id + "_commentStudyFundingAgency_div"
    id_name2 = study_id + "_commentStudyFundingAgency_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node({
        generate_ena_labels("studies.study.commentStudyFundingAgency"): study['study'][
            'commentStudyFundingAgency']}) + "</div>"

    # study description
    id_name = study_id + "_studyDescription_div"
    id_name2 = study_id + "_studyDescription_div2"
    display_string += "<div id='{id_name2!s}' class='{status_class_name!s}'></div>".format(**locals())
    display_string += "<div id='{id_name!s}' class='{class_name!s}'>".format(**locals()) + format_tree_node({
        generate_ena_labels("studies.study.studyDescription"): study['study'][
            'studyDescription']}) + "</div>"

    # study samples label
    display_string += "<div class='{list_status_class_name!s}'></div>".format(**locals())
    display_string += "<div class='{list_class_name!s}'><label>Samples</label></div>".format(**locals())
    # study samples data
    display_string += format_tree_node(composite_attributes[0])

    # study publications label
    display_string += "<div class='{list_status_class_name!s}'></div>".format(**locals())
    display_string += "<div class='{list_class_name!s}'><label>Publications</label></div>".format(**locals())
    # study publications data
    # display_string += format_tree_node(composite_attributes[1])

    # study contacts label
    display_string += "<div class='{list_status_class_name!s}'></div>".format(**locals())
    display_string += "<div class='{list_class_name!s}'><label>Contacts</label></div>".format(**locals())
    # study contacts data
    # display_string += format_tree_node(composite_attributes[2])

    display_string += "</div>"
    return display_string


def get_study_samples_children(ena_collection_id, study_id):
    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields,
                d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields]
    fields_property = get_field_order(segments)
    sample_children = []

    samples = EnaCollection().get_study_samples(ena_collection_id, study_id)

    for idx, sd in enumerate(samples):
        sample_details = EnaCollection().get_ena_sample(ena_collection_id, sd["id"])

        if sample_details:
            sample = {"id": study_id + "_" + sd['id'] + "_sample",
                      "state": "open"}
            txt = {}
            display_string = ""

            for f_o in fields_property["dblabel"][1:]:
                txt[f_o["label"]] = sample_details[f_o["db_name"]]
                k = f_o["label"]
                v = sample_details[f_o["db_name"]]
                display_string += "<div><span class='study-node-title'>{k!s}</span>: {v!s}</div>".format(**locals())

            sample["text"] = idx
            sample["attributes"] = {"data": txt, "txt": "", "label": display_string, "value": sd['id']}

            sample_children.append(sample)

    return sample_children


# used in the context of adding new study sample
def get_study_sample_tree(ena_collection_id):
    html_tag = ""
    study_data = get_studies_data(ena_collection_id)

    if study_data:
        html_tag += " <hr/>"
        html_tag += " <table class='table-bordered'>"
        html_tag += " <tr>"
        html_tag += " <th>Study Reference</th>"
        html_tag += " <th>Study Type</th>"
        html_tag += " <th># Samples</th>"
        html_tag += " <th><input id='assign_sample_studies' name='assign_sample_studies' class='check-pointer' type='checkbox' value='yes'></th>"
        html_tag += " </tr>"

        for sd in study_data:
            study_id = sd["id"]
            study_reference = sd["studyReference"]
            study_type = sd["studyType"]
            samples_count = sd["samplescount"]

            html_tag += " <tr>"
            html_tag += " <td>{study_reference!s}</td>".format(**locals())
            html_tag += " <td>{study_type!s}</td>".format(**locals())
            html_tag += " <td>{samples_count!s}</td>".format(**locals())
            html_tag += " <td>"
            html_tag += " <input class='check-pointer' type='checkbox' name='study_sample_assign_chk' value='{study_id!s}'>".format(
                **locals())
            html_tag += " </td>"
            html_tag += " </tr>"
        html_tag += " </table>"

    return html_tag


# used in the edit sample context
def get_study_sample_tree_restrict(ena_collection_id, sample_id):
    html_tag = ""
    study_data = get_studies_data(ena_collection_id)

    if study_data:
        html_tag += " <hr/>"
        html_tag += " <table class='table-bordered'>"
        html_tag += " <tr>"
        html_tag += " <th>Study Reference</th>"
        html_tag += " <th>Study Type</th>"
        html_tag += " <th># Samples</th>"
        html_tag += " <th><input id='assign_sample_studies' name='assign_sample_studies' class='check-pointer' type='checkbox' value='yes'></th>"
        html_tag += " </tr>"

        for sd in study_data:
            study_id = sd["id"]
            study_reference = sd["studyReference"]
            study_type = sd["studyType"]
            samples_count = sd["samplescount"]

            study_samples = EnaCollection().get_study_samples(ena_collection_id, study_id)
            checked = ""
            if any(d['id'] == sample_id for d in study_samples):
                checked = "checked"

            html_tag += " <tr>"
            html_tag += " <td>{study_reference!s}</td>".format(**locals())
            html_tag += " <td>{study_type!s}</td>".format(**locals())
            html_tag += " <td>{samples_count!s}</td>".format(**locals())
            html_tag += " <td>"
            html_tag += " <input class='check-pointer' type='checkbox' name='study_sample_assign_chk' value='{study_id!s}' {checked!s}>".format(
                **locals())
            html_tag += " </td>"
            html_tag += " </tr>"
        html_tag += " </table>"

    return html_tag


# samples already assigned to this study are highlighted (checked)
def get_samples_4_study_tree(ena_collection_id, study_id):
    html_tag = ""
    segments = [d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.sampleCollection.fields,
                d_utils.get_ena_ui_template_as_obj().studies.study.studySamples.fields]
    fields_property = get_field_order(segments)
    all_samples = EnaCollection().get_all_samples(ena_collection_id)
    study_samples = EnaCollection().get_study_samples(ena_collection_id, study_id)

    if all_samples:
        html_tag += "<hr/>"
        html_tag += "<table class='table-bordered'>"

        html_tag += " <tr>"
        for f_o in fields_property["dblabel"][1:]:
            html_tag += " <th>" + f_o["label"] + "</th>"
        html_tag += " <th><input id='assign_samples_study' name='assign_samples_study' class='check-pointer' type='checkbox' value='yes'></th>"
        html_tag += " </tr>"

        for all_sample in all_samples:
            sample_id = all_sample['id']
            row_id = sample_id + "_sample_assignment_row"

            checked = ""
            if any(study_sample['id'] == all_sample['id'] for study_sample in study_samples):
                checked = "checked"

            html_tag += " <tr id='{row_id!s}'>".format(**locals())
            for f_o in fields_property["dblabel"][1:]:
                v = all_sample[f_o["db_name"]]
                html_tag += " <td>{v!s}</td>".format(**locals())
            html_tag += "<td>"
            html_tag += " <input class='check-pointer' type='checkbox' name='study_samples_assign_chk' value='{sample_id!s}' {checked!s}>".format(
                **locals())
            html_tag += " </td>"
            html_tag += "</tr>"
        html_tag += "</table>"

    return html_tag


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
    key_split = field_id.split(".")
    new_dict = d_utils.get_ena_ui_template_as_dict()

    for kp in key_split[:-1]:
        new_dict = new_dict[kp]

    return new_dict["fields"]


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


@register.filter("id_to_class")
def id_to_class(val):
    return val.replace(".", "_")


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
