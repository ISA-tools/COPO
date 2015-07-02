from pprint import pprint
from threading import Thread

from django.shortcuts import render, render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
import jsonpickle


# import error codes

from project_copo.settings.error_codes import *
from apps.web_copo.mongo.copo_base_da import Profile, Collection_Head
from apps.web_copo.mongo.ena_da import *
import apps.web_copo.mongo.figshare_da as figshare
from apps.web_copo.repos.irods import *
from apps.web_copo.repos.aspera import *
from apps.chunked_upload.models import ChunkedUpload
from apps.web_copo.mongo.mongo_util import *
import apps.web_copo.uiconfigs.utils.data_formats as dfmts
import apps.web_copo.uiconfigs.utils.lookup as lkup


# Create your views here.


@login_required(login_url='/copo/login/')
def index(request):
    username = User(username=request.user)
    profiles = Profile().GET_ALL()
    context = {'user': request.user, 'profiles': profiles}
    # c = Collection.objects.filter(user = username)

    return render(request, 'copo/index.html', context)


@login_required(login_url='/copo/login/')
def new_profile(request):
    if request.method == 'POST':
        Profile().PUT(request)
        return HttpResponseRedirect(reverse('copo:index'))


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

    return render_to_response(
        'copo/login.html',
        {'login_err_message': login_err_message, 'username': username, 'next': next_loc},
        context_instance=RequestContext(request)
    )


def copo_logout(request):
    logout(request)
    return render(request, 'copo/login.html')


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

        return render(request, 'copo/login.html')


@login_required(login_url='/copo/login/')
def view_profile(request, profile_id):
    # profile = mongo.connection.Profile.one({"_id":to_mongo_id(profile_id)})
    profile = Profile().GET(profile_id)
    request.session['profile_id'] = profile_id
    collections = []
    try:
        for id in profile['collections']:
            collections.append(Collection_Head().GET(id))

    except:
        pass

    # get collection types
    collection_types = lkup.DROP_DOWNS['COLLECTION_TYPES']

    # get study types
    study_types = lkup.DROP_DOWNS['STUDY_TYPES']

    context = {'profile_id': profile_id, 'profile_title': profile['title'],
               'profile_abstract': profile['short_abstract'], 'collections': collections,
               'collection_types': collection_types, 'study_types': study_types}
    return render(request, 'copo/profile.html', context)


@login_required(login_url='/copo/login/')
def new_collection_head(request):
    # create the new collection
    collection_id = Collection_Head().PUT(request)

    # add a template for ENA submission
    coll_type = request.POST['collection_type']
    if coll_type.lower() == 'ena submission':
        # create a new db template
        ena_d = dfmts.json_to_dict(lkup.SCHEMAS["ENA"]['PATHS_AND_URIS']['ISA_json'])
        ena_coll = get_collection_ref("EnaCollections")
        ena_collection_id = ena_coll.insert(ena_d)

        # add collection details
        Collection_Head().add_collection_details(collection_id, ena_collection_id)

        # add study types
        study_type_list = [value for key, value in request.POST.items() if key.startswith("studytypeselect_")]
        # study_type_list = list(set(study_type_list))
        EnaCollection().add_study_types(ena_collection_id, study_type_list)

    profile_id = request.session['profile_id']
    Profile().add_collection_head(profile_id, collection_id)
    return HttpResponseRedirect(reverse('copo:view_profile', kwargs={'profile_id': profile_id}))


@login_required(login_url='/copo/login/')
def view_collection(request, collection_id):
    collection = Collection_Head().GET(collection_id)
    # get profile id for breadcrumb
    profile_id = request.session['profile_id']
    # set collection id in session
    request.session['collection_id'] = collection_id
    # check type of collection
    if collection['type'] == 'ENA Submission':
        schema = "ENA"
        ena_full_json = dfmts.json_to_object(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
        ena_d = ena_full_json.studies.study
        ena_sample = ena_full_json.studies.study.studySamples.sampleCollection

        # get study types
        study_types = lkup.DROP_DOWNS['STUDY_TYPES']

        if 'collection_details' in collection:
            request.session['study_id'] = str(collection['collection_details'])
            profile = Profile().GET(profile_id)
            study = EnaCollection().GET(request.session['study_id'])

            data_dict = {'collection': collection, 'collection_id': collection_id,
                         'study_id': request.session['study_id'], 'profile_id': profile_id,
                         'study': study,
                         'profile': profile,
                         'ena_d': ena_d,
                         'study_types': study_types
                         }
        else:
            data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id}
        return render(request, 'copo/ena_collection_multi.html', data_dict, context_instance=RequestContext(request))
    elif collection['type'] == 'PDF File' or collection['type'] == 'Image':
        articles = figshare.FigshareCollection().get_articles_in_collection(collection_id)
        data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id,
                     'articles': articles}
        return render(request, 'copo/article.html', data_dict, context_instance=RequestContext(request))


def add_to_collection(request):
    profile_id = request.session['profile_id']
    study_type_list = request.POST['study_types']
    ena_collection_id = request.POST['collection_id']
    study_type_list = study_type_list.split(",")
    EnaCollection().add_study_types(ena_collection_id, study_type_list)

    return_structure = {'exit_status': 'success'}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')

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
            path_to_files = os.path.join(settings.MEDIA_ROOT, file_object.file.name)

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


def ena_template(request):
    schema = "ENA"
    ena_o = dfmts.json_to_object(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])
    ena_d = dfmts.json_to_dict(lkup.SCHEMAS[schema]['PATHS_AND_URIS']['UI_TEMPLATE_json'])

    # can also work with traditional python dictionaries, but i prefer the dot notation
    ena_d = ena_d["studies"]["study"]["assays"]["assaysTable"]["genomeSeq"]

    ena_o = ena_o.studies.study.assays.assaysTable.genomeSeq.nucleicAcidSequencing

    return render_to_response(
        'copo/ena_template.html',
        {'ena_o': ena_o},
        context_instance=RequestContext(request)
    )
