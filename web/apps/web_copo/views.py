from threading import Thread
import logging
import sys
import ast

from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template import RequestContext

from error_codes import DB_ERROR_CODES, UI_ERROR_CODES
from settings_dev import MEDIA_ROOT

log = logging.getLogger(__name__)
log.debug(sys.path)


from dal.copo_base_da import Profile, Collection_Head
from dal.ena_da import EnaCollection
from dal.orcid_da import Orcid

from web_copo.repos.irods import *
from web_copo.repos.aspera import *
from chunked_upload.models import ChunkedUpload
from web_copo.api.views import *
import web_copo.uiconfigs.utils.lookup as lkup
import web_copo.templatetags.html_tags as htags
from django_tools.middlewares import ThreadLocal
import web_copo.uiconfigs.utils.data_utils as d_utils


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

'''
def copo_login(request):
    # pdb.set_trace()
    if request.user.is_authenticated():
        copo_logout(request)

    login_err_message = LOGIN_ERROR_CODES["LOGIN_LOGIN_PROMPT"]
    username = password = ''
    next_loc = request.REQUEST.get('next', '')

    if request.method == "POST":
        username = request.POST['frm_login_username']
        password = request.POST['frm_login_password']

        if not (username and password):
            login_err_message = LOGIN_ERROR_CODES["LOGIN_NO_USERNAME_PASSWORD"]
        else:
            user = authenticate(username=username, password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    # successfully logged in!
                    if not next_loc:
                        next_loc = "/copo"
                    return HttpResponseRedirect(next_loc)
                else:
                    login_err_message = LOGIN_ERROR_CODES["LOGIN_INACTIVE_ACCOUNT"]
            else:
                login_err_message = LOGIN_ERROR_CODES["LOGIN_INCORRECT_USERNAME_PASSWORD"]
    else:
        # check if we had a code parameter in the GET, if so
        s = request.GET.get('next', '')
        try:
            index = s.index('=')
        except:
            return render_to_response(
                'copo/templates/account/login.html',
                {'login_err_message': login_err_message, 'username': username, 'next': next_loc},
                context_instance=RequestContext(request)
            )
        orcid_code = s[index + 1:]
        if orcid_code != '':
            handle_orcid_authorise(orcid_code)
        if not next_loc:
            next_loc = "/copo"
        return HttpResponseRedirect(reverse('copo:index'))
    return render_to_response(
        'copo/templates/account/login.html',
        {'login_err_message': login_err_message, 'username': username, 'next': next_loc},
        context_instance=RequestContext(request)
    )
'''

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
    collection_head_id = Collection_Head().PUT(c_type, c_name)

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

        ena_collection_id = get_collection_ref("EnaCollections").insert(db_template)

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
            sample_data = htags.get_samples_data(request.session['ena_collection_id'])
            study_data = htags.get_studies_data(request.session['ena_collection_id'])

            data_dict = {'collection_head': collection_head, 'collection_head_id': collection_head_id,
                         'ena_collection_id': request.session['ena_collection_id'], 'profile_id': profile_id,
                         'ena_collection': ena_collection,
                         'profile': profile,
                         'ui_template': ui_template,
                         'study_types': study_types,
                         'sample_data': sample_data,
                         'study_data': study_data
                         }
        else:
            data_dict = {'collection_head': collection_head, 'collection_head_id': collection_head_id,
                         'profile_id': profile_id}
        return render(request, 'copo/ena_collection_multi.html', data_dict, context_instance=RequestContext(request))
    elif collection_head['type'].lower() == 'pdf file' or collection_head['type'].lower() == 'image':
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

    ena_collection_id = str(collection_head['collection_details'])
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

    data_dict = {'collection_head_id': collection_head_id,
                 'profile_id': profile_id,
                 'study_id': study_id,
                 'profile': profile,
                 'ena_collection_id': ena_collection_id,
                 'study': study,
                 'study_types': study_types,
                 'ui_template': ui_template
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
    if task == "update_study_details":
        auto_fields = request.POST['auto_fields']
        EnaCollection().update_study_details(ena_collection_id, study_id, auto_fields)
        return_structure['study_data'] = EnaCollection().get_ena_study(study_id, ena_collection_id)["study"]

    if task == "get_study_data":
        return_structure['study_data'] = EnaCollection().get_ena_study(study_id, ena_collection_id)["study"]

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
                if 'study_type_reference_' + k[-1:] in study_fields:  # only add if a study reference has been provided
                    st_dict = {'study_type': study_fields[k],
                               'study_type_reference': study_fields['study_type_reference_' + k[-1:]]}
                    st_list.append(st_dict)

        if st_list:
            EnaCollection().add_ena_study(ena_collection_id, st_list)

        return_structure['study_data'] = htags.get_studies_data(ena_collection_id)

    elif task == "get_tree_study":
        return_structure['ena_studies'] = htags.get_studies_tree(ena_collection_id)

    elif task == "get_tree_study_sample":
        return_structure['ena_studies'] = htags.get_study_sample_tree(ena_collection_id)

    elif task == "get_study_sample":
        return_structure['sample_data'] = EnaCollection().get_ena_sample(ena_collection_id, request.POST['sample_id'])
        return_structure['ena_studies'] = htags.get_study_sample_tree_restrict(ena_collection_id,
                                                                               request.POST['sample_id'])

    elif task == "add_new_study_sample" or task == "edit_study_sample":
        auto_fields = request.POST['auto_fields']
        study_type_list = request.POST['study_types']
        study_type_list = study_type_list.split(",")

        if task == "edit_study_sample":
            sample_id = request.POST['sample_id']
            EnaCollection().edit_ena_sample(ena_collection_id, sample_id, study_type_list, auto_fields)
        else:
            EnaCollection().add_ena_sample(ena_collection_id, study_type_list, auto_fields)

        return_structure['sample_data'] = htags.generate_sample_table2(ena_collection_id)
        return_structure['study_data'] = htags.get_studies_data(ena_collection_id)

    return_structure['exit_status'] = 'success'
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def remove_from_collection(request):
    task = request.GET['task']

    collection_head_id = request.GET['collection_head_id']
    collection = Collection_Head().GET(collection_head_id)
    ena_collection_id = str(collection['collection_details'][0])

    if task == "remove_study_sample":
        study_samples_id = request.GET['study_samples_id']
        # EnaCollection().remove_study_sample(ena_collection_id, study_samples_id)

    return_structure = {'exit_status': 'success'}
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

def initiate_repo(request):
    initiate_status = ""
    aspera_transfer_id = ""
    pct_complete = ""
    exit_status = ""
    asperacollections = get_collection_ref("AsperaCollections")

    if request.method == "POST":
        files = request.POST["files"]
        # todo: should expand this to include multiple files

        try:
            file_object = get_object_or_404(ChunkedUpload, pk=files)
            path_to_files = os.path.join(MEDIA_ROOT, file_object.file.name)

            document = {
                "file": path_to_files,
                "user_id": request.user.id,
                "started_on": datetime.now(),
                "completed_on": '',
                "transfer_rate": '',
                "pct_complete": '',
                "exit_status": '',
                "elapsed_time": '',
                "file_size (bytes)": '',
                "bytes_lost": ''
            }

            aspera_transfer_id = asperacollections.insert(document)
            initiate_status = "success"
        except:
            initiate_status = "error"

        process = Thread(target=do_aspera_transfer, args=(aspera_transfer_id,))
        process.start()

    elif request.method == "GET":
        aspera_transfer_id = request.GET["transfer_id"]

        document = list(asperacollections.find({"_id": ObjectId(aspera_transfer_id)},
                                               {"pct_complete": 1, "exit_status": 1}))
        pct_complete = document[0]['pct_complete']
        exit_status = document[0]['exit_status']

    return_structure = {'pct_complete': pct_complete,
                        'exit_status': exit_status,
                        'initiate_status': initiate_status,
                        "transfer_id": str(aspera_transfer_id)
                        }
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def register_to_irods(request):
    status = register_to_irods()
    return_structure = {'exit_status': status}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')
