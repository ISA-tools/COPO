from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Max
import jsonpickle
import pexpect

from apps.web_copo.models import RepositoryFeedback




# import error codes
from project_copo.settings.error_codes import *
from project_copo.settings.repo_settings import *
from project_copo.settings.settings import *
from apps.web_copo.mongo.copo_base_objects import Profile, Collection_Head
from apps.web_copo.mongo.ena_objects import *



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
                    if not (next_loc):
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
    #profile = mongo.connection.Profile.one({"_id":to_mongo_id(profile_id)})
    profile = Profile().GET(profile_id)
    request.session['profile_id'] = profile_id
    collections = []
    try:
        for id in profile['collections']:
            collections.append(Collection_Head().GET(id))

    except:
        pass
    context = {'profile_id': profile_id, 'profile_title': profile['title'], 'profile_abstract': profile['short_abstract'], 'collections': collections}
    return render(request, 'copo/profile.html', context)


@login_required(login_url='/copo/login/')
def new_collection_head(request):

    #create the new collection
    collection_id = Collection_Head().PUT(request)
    profile_id = request.session['profile_id']
    Profile().add_collection_head(profile_id, collection_id)
    return HttpResponseRedirect(reverse('copo:view_profile', kwargs={'profile_id': profile_id}))


@login_required(login_url='/copo/login/')
def view_collection(request, collection_id):

    collection = Collection_Head().GET(collection_id)
    #get profile id for breadcrumb
    profile_id = request.session['profile_id']
    #set collection id in session
    request.session['collection_id'] = collection_id
    #check type of collection
    if collection['type'] == 'ENA Submission':
        if('collection_details' in collection):
            request.session['study_id'] = str(collection['collection_details'])
            data_dict = {'collection': collection, 'collection_id': collection_id, 'study_id': request.session['study_id'], 'profile_id': profile_id, 'study': EnaCollection().GET(request.session['study_id'])}
        else:
            data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id}
        return render(request, 'copo/ena_collection_multi.html', data_dict, context_instance=RequestContext(request))
    elif collection['type'] == 'PDF File' or collection['type'] == 'Image':
            data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id}
            return render(request, 'copo/article.html', data_dict, context_instance=RequestContext(request))


@login_required(login_url='/copo/login/')
def submit_to_figshare(request):
    #result = figshare.make_article(oauth=get_credentials())
    #article_id = result['article_id']
    #add file to article
    #result = figshare.add_file_to_article(oauth=get_credentials(), article_id=article_id, filename='/Users/fshaw/Downloads/COPO-Architecture.pdf')

    result = 'test output'
    context = {'input': jsonpickle.encode(result)}
    return render(request, 'copo/article.html', context)


def manage_repo_feedback(request):
    out = "none"
    sess_key = request.session.session_key
    b = RepositoryFeedback.objects.filter(session_key=sess_key).aggregate(Max('id'))
    feedback_obj = RepositoryFeedback.objects.get(pk=b['id__max'])

    # need to handle exception for none-existing db data
    return_structure = {'pct_complete': feedback_obj.current_pct}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


def initiate_repo(request):
    status = "error"
    if request.method == "POST":
        # remove any existing reference to this session key in the db
        for e in RepositoryFeedback.objects.filter(session_key=request.session.session_key):
            e.delete()

        feedback_obj = RepositoryFeedback(current_pct=0, session_key=request.session.session_key)
        feedback_obj.save()

        # these might potentially come from some request object
        file_path = param['file_path']
        user_name = param['username']
        password = param['password']
        path2library = os.path.join(BASE_DIR, REPO_LIB_PATHS["ASPERA"])
        remote_path = os.path.join("copo", time.strftime("%Y%m%d"))

        cmd = "./ascp -d -QT -l300M -L- {file_path!s} {user_name!s}:{remote_path!s}".format(**locals())

        os.chdir(path2library)

        thread = pexpect.spawn(cmd, timeout=None)
        thread.expect(["assword:", pexpect.EOF])
        thread.sendline(password)

        cpl = thread.compile_pattern_list([pexpect.EOF, '(\d+%)'])

        while True:
            i = thread.expect_list(cpl, timeout=None)
            if i == 0:  # EOF! Possible error point if encountered before transfer completion
                print("the sub process exited")
                break
            elif i == 1:
                trans_pct = thread.match.group(1)
                trans_pct = trans_pct.decode("utf-8")
                print("%s completed" % trans_pct)
                pct_val = trans_pct.rstrip("%")
                feedback_obj.current_pct = pct_val
                feedback_obj.save()
                if int(pct_val) == 100:
                    status = "success"
                    print(status)
                    break
        thread.close()

    return_structure = {'exit_status': status}
    out = jsonpickle.encode(return_structure)
    return HttpResponse(out, content_type='json')


# for testing
path_to_file = "/Users/etuka/Dropbox/Dev/data/888_LIB6842_LDI5660_ACTTGA_L002_R2_013.fastq"

param = {
    'repository': 'ENA',
    'file_path': path_to_file,
    'username': 'Webin-39962@webin.ebi.ac.uk',
    'password': 'toni12'
}
