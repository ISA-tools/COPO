from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from apps.web_copo.mongo.mongo_util import *
from datetime import datetime

import uuid
from apps.web_copo.mongo.copo_base_objects import Profile, Collection_Head
from apps.web_copo.mongo.ena_objects import *
from apps.web_copo.models import EnaStudy, EnaSample



# Create your views here.
# @login_required
def index(request):
    username = User(username=request.user)
    profiles = Profile().GET_ALL()
    context = {'user': request.user, 'profiles': profiles}
    return render(request, 'copo/index.html', context)


def new_profile(request):
    if request.method == 'POST':
        Profile().PUT(request)
        return HttpResponseRedirect(reverse('copo:index'))


def copo_login(request):
    # pdb.set_trace()
    if request.method == 'GET':


        return render(request, 'copo/login.html')

    else:

        username = request.POST['frm_login_username']
        password = request.POST['frm_login_password']

        if not (username or password):
            return HttpResponseRedirect('/copo/login')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return HttpResponseRedirect('/copo/')

                    # Return a 'disabled account' error message

            # Return an 'invalid login' error message.

            return render(request, 'copo/login.html')


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


def view_test(request):
    context = {}
    return render(request, 'copo/testing.html', context)


def new_collection_head(request):

    #create the new collection
    collection_id = Collection_Head().PUT(request)
    profile_id = request.session['profile_id']
    Profile().add_collection_head(profile_id, collection_id)
    return HttpResponseRedirect(reverse('copo:view_profile', kwargs={'profile_id': profile_id}))

def view_collection(request, collection_id):

    collection = Collection_Head().GET(collection_id)

    #get profile id for breadcrumb
    profile_id = request.session['profile_id']


    #check type of collection
    if collection['type'] == 'ENA Submission':
        if('collection_details' in collection):
            request.session['collection_details'] = str(collection['collection_details'])
            data_dict = {'collection': collection, 'collection_id': collection_id, 'study_id': request.session['collection_details'], 'profile_id': profile_id, 'study': EnaCollection().GET(request.session['collection_details'])}
        else:
            data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id}
        return render(request, 'copo/ena_collection_multi.html', data_dict, context_instance=RequestContext(request))


def view_test2(request):
    return render(request, 'copo/testing2.html')
