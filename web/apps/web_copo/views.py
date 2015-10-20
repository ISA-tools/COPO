from threading import Thread
import logging
from datetime import datetime
import sys
import ast

import os
from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template import RequestContext

from error_codes import DB_ERROR_CODES, UI_ERROR_CODES
from web.apps.web_copo.repos.aspera import AsperaTransfer

log = logging.getLogger(__name__)
log.debug(sys.path)

from dal.copo_base_da import Profile, Collection_Head
from dal.mongo_util import get_collection_ref
from dal.ena_da import EnaCollection
from dal.orcid_da import Orcid
from web.apps.web_copo.copo_maps.utils.data_utils import get_collection_head_dc

from chunked_upload.models import ChunkedUpload
from web.apps.web_copo.api.views import *
import web.apps.web_copo.copo_maps.utils.lookup as lkup
import web.apps.web_copo.templatetags.html_tags as htags
from django_tools.middlewares import ThreadLocal
import web.apps.web_copo.copo_maps.utils.data_utils as d_utils
from web.apps.web_copo.repos.aspera import AsperaTransfer
from dal import ObjectId
from master_settings import MEDIA_ROOT
from dal.copo_base_da import DataSchemas
from api.doi_metadata import DOI2Metadata


@login_required
def index(request):
    username = User(username=request.user)
    profiles = Profile().GET_FOR_USER()
    context = {'user': request.user, 'profiles': profiles}
    # c = Collection.objects.filter(user = username)
    request.META['test'] = 'test'
    return render(request, 'copo/index.html', context)


@login_required
def goto_error(request, message="Something went wrong, but we're not sure what!"):
    context = {'message': message}
    return render(request, 'copo/error_page.html', context)


@login_required
def new_profile(request):
    if request.method == 'POST':

        a = request.POST['study_abstract']
        title = request.POST['study_title']
        uid = request.user.id
        if Profile().PUT(a, title, uid) == False:
            return render(request,
                          'copo/error_page.html',
                          {'message': 'Error creating COPO ID for Profile - Are you on the network?'},
                          )
        return HttpResponseRedirect(reverse('copo:index'))


def copo_logout(request):
    logout(request)
    return render_to_response(request, 'copo/templates/account/login.html')


def copo_register(request):
    if request.method == 'GET':
        return render(request, 'copo/register.html')
    else:
        # create user and return to login page
        firstname = request.POST['frm_register_firstname']
        lastname = request.POST['frm_register_lastname']
        email = request.POST['frm_register_email']
        username = request.POST['frm_register_username']
        password = request.POST['frm_register_password']

        user = User.objects.create_user(username, email, password)
        user.set_password(password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()

        return render(request, 'copo/templates/account/login.html')


@login_required
def view_profile(request, profile_id):
    profile = Profile().GET(profile_id)
    request.session['profile_id'] = profile_id
    collections = []
    try:
        for id in profile['collections']:
            collections.append(Collection_Head().GET(id))

    except:
        pass

    collection_types = lkup.DROP_DOWNS['COLLECTION_TYPES']
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    context = {'profile_id': profile_id, 'profile_title': profile['title'],
               'profile_abstract': profile['short_abstract'], 'collections': collections,
               'collection_types': collection_types, 'study_types': study_types}
    return render(request, 'copo/profile.html', context)


@login_required
def new_collection_head(request):
    # create the new collection
    c_type = request.POST['collection_type']
    c_name = request.POST['collection_name']
    collection_head_id = Collection_Head().PUT()
    collection_head_dc = get_collection_head_dc()
    collection_head_dc['name'] = c_name
    collection_head_dc['type'] = c_type
    Collection_Head().update(collection_head_id, collection_head_dc)

    # add a template for ENA submission
    coll_type = request.POST['collection_type']
    if coll_type.lower() == 'ena submission':
        # create a blank ENA collection based on template

        db_template = d_utils.get_ena_db_template()

        if not db_template:
            return render(request,
                          'copo/error_page.html',
                          {'message': DB_ERROR_CODES["TEMPLATE_NOT_FOUND"]},
                          )
            return HttpResponseRedirect(reverse('copo:index'))

        ena_collection_id = EnaCollection().PUT(db_template)

        # add collection details
        Collection_Head().add_collection_details(collection_head_id, ena_collection_id)

        # get studies
        st_list = []

        for k, v in request.POST.items():
            if k.startswith('study_type_select_'):
                st_dict = {'study_type': request.POST.get(k, ""),
                           'study_type_reference': request.POST.get('study_type_reference_' + k[-1:], "")
                           }
                st_list.append(st_dict)

        EnaCollection().add_ena_study(ena_collection_id, st_list)

    profile_id = request.session['profile_id']
    Profile().add_collection_head(profile_id, collection_head_id)
    return HttpResponseRedirect(reverse('copo:view_profile', kwargs={'profile_id': profile_id}))


@login_required
def view_collection(request, collection_head_id):
    collection_head = Collection_Head().GET(collection_head_id)
    # get profile id for breadcrumb
    profile_id = request.session['profile_id']
    request.session['collection_head_id'] = collection_head_id

    # ENA Type Handler-----------------------------------
    if collection_head['type'].lower() == 'ena submission':
        # get template for rendering the UI
        ui_template = DataSchemas("ENA").get_ui_template()
        if not ui_template:
            return render(request,
                          'copo/error_page.html',
                          {'message': UI_ERROR_CODES["TEMPLATE_NOT_FOUND"]},
                          )
            return HttpResponseRedirect(reverse('copo:index'))

        # get study types
        study_types = lkup.DROP_DOWNS['STUDY_TYPES']

        if 'collection_details' in collection_head:
            request.session['ena_collection_id'] = str(collection_head['collection_details'][0])
            profile = Profile().GET(profile_id)
            ena_collection = EnaCollection().GET(request.session['ena_collection_id'])
            sample_attributes = d_utils.get_sample_attributes()

            messages = {}
            messages["user_defined_attribute_message"] = lkup.UI_INFO["user_defined_attribute_message"]
            messages["system_suggested_attribute_message"] = lkup.UI_INFO["system_suggested_attribute_message"]

            data_dict = {'collection_head': collection_head, 'collection_head_id': collection_head_id,
                         'ena_collection_id': request.session['ena_collection_id'], 'profile_id': profile_id,
                         'ena_collection': ena_collection,
                         'profile': profile,
                         'ui_template': ui_template,
                         'study_types': study_types,
                         'sample_attributes': sample_attributes,
                         'messages': messages,
                         }
        else:
            data_dict = {'collection_head': collection_head, 'collection_head_id': collection_head_id,
                         'profile_id': profile_id}
        request.session.delete('collected')
        return render(request, 'copo/ena_collection_multi.html', data_dict, context_instance=RequestContext(request))


    # Figshare Type Handler -------------------------------------

    elif collection_head['type'].lower() == 'figshare':
        articles = FigshareCollection().get_articles_in_collection(collection_head_id)
        data_dict = {'collection_head': collection_head, 'collection_head_id': collection_head_id,
                     'profile_id': profile_id,
                     'articles': articles}
        return render(request, 'copo/article.html', data_dict, context_instance=RequestContext(request))


@login_required
def view_orcid_profile(request):
    user = ThreadLocal.get_current_user()
    op = Orcid().get_orcid_profile(user)
    data_dict = {'op': op}
    # data_dict = jsonpickle.encode(data_dict)
    return render(request, 'copo/orcid_profile.html', data_dict, context_instance=RequestContext(request))


@login_required
def view_study(request, study_id):
    profile_id = request.session['profile_id']
    collection_head_id = request.session['collection_head_id']
    collection_head = Collection_Head().GET(collection_head_id)

    ena_collection_id = str(collection_head['collection_details'][0])
    profile = Profile().GET(profile_id)
    study = EnaCollection().get_ena_study(study_id, ena_collection_id)

    ui_template = DataSchemas("ENA").get_ui_template()
    if not ui_template:
        return render(request,
                      'copo/error_page.html',
                      {'message': UI_ERROR_CODES["TEMPLATE_NOT_FOUND"]},
                      )
        return HttpResponseRedirect(reverse('copo:index'))

    ui_template = ui_template["studies"]["study"]

    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']
    files_already_in_study = 4;

    data_dict = {'collection_head_id': collection_head_id,
                 'profile_id': profile_id,
                 'study_id': study_id,
                 'profile': profile,
                 'ena_collection_id': ena_collection_id,
                 'study': study,
                 'study_types': study_types,
                 'ui_template': ui_template,
                 'files_already_in_study': 4,
                 }
    return render(request, 'copo/ena_study.html', data_dict, context_instance=RequestContext(request))


def add_to_study(request):
    return_structure = {}
    # get task to be performed
    task = request.POST['task']

    ena_collection_id = request.POST['ena_collection_id']
    study_id = request.POST['study_id']

    if task == "update_study_type":
        study_type = request.POST['study_type']
        study_type_reference = request.POST['study_type_reference']
        elem_dict = {"study_type": study_type, "study_type_reference": study_type_reference}

        EnaCollection().update_study_type(ena_collection_id, study_id, elem_dict)
        study = EnaCollection().get_ena_study(study_id, ena_collection_id)
        return_structure['study_type_data'] = {"study_type": study["studyCOPOMetadata"]["studyType"],
                                               "study_type_label": htags.lookup_study_type_label(
                                                   study["studyCOPOMetadata"]["studyType"]),
                                               "study_type_reference": study["studyCOPOMetadata"]["studyReference"]}
    elif task == "update_study_details":
        auto_fields = request.POST['auto_fields']
        EnaCollection().update_study_details(ena_collection_id, study_id, auto_fields)
        return_structure['study_data'] = EnaCollection().get_ena_study(study_id, ena_collection_id)["study"]

    elif task == "delete_sample_from_study":
        sample_id = request.POST['sample_id']
        EnaCollection().hard_delete_sample_from_study(sample_id, study_id, ena_collection_id)
        return_structure['sample_data'] = htags.generate_study_samples_table2(ena_collection_id, study_id)
        # get updated table info to display
        return_structure['data_file_html'] = htags.generate_study_data_table2(ena_collection_id, study_id)

    elif task == "delete_publication_from_study":
        publication_id = request.POST['publication_id']
        field_list = [{"deleted": "1"}]
        EnaCollection().update_study_publication(publication_id, study_id, ena_collection_id, field_list)
        return_structure['publication_data'] = htags.generate_study_publications_table2(ena_collection_id, study_id)

    elif task == "delete_contact_from_study":
        contact_id = request.POST['contact_id']
        field_list = [{"deleted": "1"}]
        EnaCollection().update_study_contact(contact_id, study_id, ena_collection_id, field_list)
        return_structure['contact_data'] = htags.generate_study_contacts_table2(ena_collection_id, study_id)

    elif task == "assign_samples_to_study":
        selected_study_samples_list = request.POST['selected_study_samples']
        if selected_study_samples_list:
            selected_study_samples_list = selected_study_samples_list.split(",")
        else:
            selected_study_samples_list = []

        excluded_study_samples_list = request.POST['excluded_study_samples']
        if excluded_study_samples_list:
            excluded_study_samples_list = excluded_study_samples_list.split(",")
        else:
            excluded_study_samples_list = []
        EnaCollection().assign_samples_in_study(study_id, ena_collection_id, selected_study_samples_list,
                                                excluded_study_samples_list)
        return_structure['sample_data'] = htags.generate_study_samples_table2(ena_collection_id, study_id)
        # get updated table info to display in datafiles panel
        return_structure['data_file_html'] = htags.generate_study_data_table2(ena_collection_id, study_id)

    elif task == "add_new_publication":
        auto_fields = request.POST['auto_fields']
        EnaCollection().add_study_publication(study_id, ena_collection_id, auto_fields)
        return_structure['publication_data'] = htags.generate_study_publications_table2(ena_collection_id, study_id)

    elif task == "add_new_contact":
        auto_fields = request.POST['auto_fields']
        EnaCollection().add_study_contact(study_id, ena_collection_id, auto_fields)
        return_structure['contact_data'] = htags.generate_study_contacts_table2(ena_collection_id, study_id)

    elif task == "add_new_protocol":
        auto_fields = request.POST['auto_fields']
        EnaCollection().add_study_protocol(study_id, ena_collection_id, auto_fields)
        return_structure['protocol_data'] = htags.generate_study_contacts_table2(ena_collection_id, study_id)

    elif task == "resolve_publication_doi":
        doi_handle = request.POST['doi_handle']
        return_structure['publication_doi_data'] = DOI2Metadata(doi_handle).publication_metadata()
        return_structure['ena_fields_mapping'] = lkup.SCHEMAS["ENA"]['ENA_DOI_PUBLICATION_MAPPINGS']

    elif task == "get_tree_samples_4_studies":
        return_structure['samples_tree'] = htags.get_samples_4_study_tree(ena_collection_id, study_id)

    elif task == "get_study_data":
        return_structure['study_data'] = EnaCollection().get_ena_study(study_id, ena_collection_id)["study"]

    elif task == "get_study_sample":
        return_structure['sample_data'] = EnaCollection().get_ena_sample(ena_collection_id, request.POST['sample_id'])

    elif task == "attach_file_sample":
        samples = request.POST['samples']
        samples = ast.literal_eval(samples)
        data_file_id = request.POST['data_file_id']
        fields = {"samples": samples}
        EnaCollection().update_ena_datafile(study_id, ena_collection_id, data_file_id, fields)
    elif task == "delete_datafile_from_study":
        data_file_id = request.POST['data_file_id']
        fields = {"deleted": "1"}
        EnaCollection().update_ena_datafile(study_id, ena_collection_id, data_file_id, fields)
        # get updated table info for UI display
        return_structure['data_file_html'] = htags.generate_study_data_table2(ena_collection_id, study_id)

    return_structure['exit_status'] = 'success'
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def add_to_collection(request):
    return_structure = {}
    # get task to be performed
    task = request.POST['task']

    collection_head_id = request.POST['collection_head_id']
    collection = Collection_Head().GET(collection_head_id)
    ena_collection_id = str(collection['collection_details'][0])

    if task == "add_new_study":
        study_fields = request.POST['study_fields']
        study_fields = ast.literal_eval(study_fields)

        # get studies
        st_list = []

        for k, v in study_fields.items():
            if k.startswith('study_type_select_'):
                index_part = k.split("study_type_select_")[1]
                # only add if a study reference has been provided
                if 'study_type_reference_' + index_part in study_fields:
                    st_dict = {'study_type': study_fields[k],
                               'study_type_reference': study_fields['study_type_reference_' + index_part]}
                    st_list.append(st_dict)

        if st_list:
            EnaCollection().add_ena_study(ena_collection_id, st_list)

        return_structure['study_data'] = htags.generate_study_table2(ena_collection_id)

    elif task == "clone_study":
        cloned_elements = request.POST['cloned_elements']
        cloned_elements = ast.literal_eval(cloned_elements)

        EnaCollection().clone_ena_study(ena_collection_id, cloned_elements)
        return_structure['study_data'] = htags.generate_study_table2(ena_collection_id)

    elif task == "delete_study":
        study_id = request.POST['study_id']
        EnaCollection().delete_study(ena_collection_id, study_id)
        return_structure['study_data'] = htags.generate_study_table2(ena_collection_id)

    elif task == "get_tree_study":
        return_structure['ena_studies'] = htags.get_studies_tree(ena_collection_id)

    elif task == "get_tree_study_sample":
        return_structure['ena_studies'] = htags.get_study_sample_tree(ena_collection_id)

    elif task == "get_study_sample":
        return_structure['sample_data'] = EnaCollection().get_ena_sample(ena_collection_id, request.POST['sample_id'])
        return_structure['ena_studies'] = htags.get_study_sample_tree_restrict(ena_collection_id,
                                                                               request.POST['sample_id'])
        messages = {}
        messages["edit"] = lkup.UI_LABELS["sample_edit"]
        messages["clone"] = lkup.UI_LABELS["sample_clone"]
        messages["add"] = lkup.UI_LABELS["sample_add"]
        return_structure['messages'] = messages

    elif task == "get_sample_attributes":
        return_structure['sample_attributes'] = d_utils.get_sample_attributes()
        messages = {}
        messages["system_suggested_attribute_message"] = lkup.UI_INFO["system_suggested_attribute_message"]
        messages["sample_add"] = lkup.UI_LABELS["sample_add"]
        return_structure['messages'] = messages

    elif task == "add_new_study_sample" or task == "edit_study_sample" or task == "clone_study_sample":
        auto_fields = request.POST['auto_fields']
        study_type_list = request.POST['study_types']
        if study_type_list:
            study_type_list = study_type_list.split(",")
        else:
            study_type_list = []

        if task == "edit_study_sample":
            sample_id = request.POST['sample_id']
            EnaCollection().edit_ena_sample(ena_collection_id, sample_id, study_type_list, auto_fields)
        else:
            EnaCollection().add_ena_sample(ena_collection_id, study_type_list, auto_fields)

        return_structure['sample_data'] = htags.generate_sample_table2(ena_collection_id)
        return_structure['study_data'] = htags.generate_study_table2(ena_collection_id)

    return_structure['exit_status'] = 'success'
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def save_figshare_collection(request):
    # make new entries for collection
    input_files = request.POST.getlist('files[]')
    tags = request.POST.getlist('tags[]')
    article_type = request.POST.get("article_type")
    description = request.POST.get("description")
    collection_head_id = request.session['collection_head_id']
    a = FigshareCollection().save_article(input_files, tags, article_type, description, collection_head_id)
    return HttpResponse(jsonpickle.encode(a))


def upload_to_dropbox(request):
    return_structure = {}
    # set up an Aspera collection handle
    AsperaCollection = get_collection_ref("AsperaCollections")
    transfer_token = ""

    task = request.POST['task']

    if task == "initiate_transfer":  # initiate the transfer process
        # get the target datafile and obtain the file reference
        study_id = request.POST["study_id"]
        ena_collection_id = request.POST["ena_collection_id"]
        data_file_id = request.POST["data_file_id"]
        data_file = EnaCollection().get_study_datafile(study_id, ena_collection_id, data_file_id)
        chunked_upload = ChunkedUpload.objects.get(id=int(data_file["fileId"]))

        # set a new document in the aspera collection,
        # thus obtaining a transfer token to orchestrate the transfer process
        path_to_json = lkup.SCHEMAS["COPO"]['PATHS_AND_URIS']['ASPERA_COLLECTION']
        db_template = d_utils.json_to_pytype(path_to_json)
        transfer_token = AsperaCollection.insert(db_template)
        path_to_file = os.path.join(MEDIA_ROOT, chunked_upload.file.name)

        # update some initial fields
        # assume transfer_status is 'transferring' initially to allow the progress monitor to kick-start
        AsperaCollection.update({"_id": transfer_token},
                                {"$set": {"transfer_commenced": str(datetime.now()),
                                          "file_path": path_to_file,
                                          "transfer_status": "transferring",
                                          "pct_completed": 0}
                                 })

        # instantiate an aspera transfer process
        process = Thread(target=AsperaTransfer, args=(transfer_token,))
        process.start()

        return_structure['initiate_data'] = {"transfer_token": str(transfer_token)}

    elif task == "transfer_progress":
        tokens = ast.literal_eval(request.POST["tokens"])
        progress_list = []

        for key, value in tokens.items():
            doc = AsperaCollection.find_one({"_id": ObjectId(key)})
            if doc:
                progress = {"transfer_token": key, "pct_completed": doc["pct_completed"],
                            "transfer_status": doc["transfer_status"]}
                progress_list.append(progress)

        return_structure['progress_data'] = progress_list

    return_structure['exit_status'] = 'success'
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def submit_to_repo(request):
    pass


def register_to_irods(request):
    status = register_to_irods()
    return_structure = {'exit_status': status}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')
