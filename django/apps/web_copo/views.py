from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from apps.web_copo.mongo.mongo_util import *
from datetime import datetime
from mongokit import Document
import uuid
from mongo.copo_base_objects import Profile

from apps.web_copo.models import Collection, EnaStudy, EnaSample



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
    profile = mongo.connection.Profile.one({"_id":to_mongo_id(profile_id)})

    request.session['profile_id'] = profile_id
    collections = profile.collections
    context = {'profile_id': profile_id, 'profile_title': profile.title, 'profile_abstract': profile.short_abstract, 'collections': collections}
    return render(request, 'copo/profile.html', context)


def view_test(request):
    context = {}
    return render(request, 'copo/testing.html', context)


def new_collection(request):

    c_type = request.POST['collection_type']
    c_name = request.POST['collection_name']
    profile_id = request.session['profile_id']
    id = str(uuid.uuid1())
    #get profile
    p = mongo.connection.Profile.one({'_id':to_mongo_id(profile_id)})
    c = {'id': id, 'name': c_name, 'type': c_type}
    p.collections.append(c)
    p.save()
    context = {'request_type': c_type, 'bundle': c}
    return HttpResponseRedirect(reverse('copo:view_profile', kwargs={'profile_id': profile_id}))


def view_collection(request, collection_id):
    # collection = Collection.objects.get(id=pk)
    collection = get_object_or_404(Collection, pk=collection_id)
    #get profile id for breadcrumb
    profile_id = collection.profile.id
    #check type of collection
    if collection.type == 'ENA Submission':
        #get samples for enastudy association
        try:
            study = EnaStudy.objects.get(collection__id=int(collection_id))
            samples = EnaSample.objects.filter(ena_study__id=study.id)
            data_dict = {'collection': collection, 'samples': samples, 'collection_id': collection_id,
                         'study_id': study.id, 'profile_id': profile_id}
            return render_to_response('copo/ena_collection_multi.html', data_dict,
                                      context_instance=RequestContext(request))
        except ObjectDoesNotExist as e:
            data_dict = {'collection': collection, 'collection_id': collection_id, 'profile_id': profile_id}
            return render(request, 'copo/ena_collection_multi.html', data_dict,
                          context_instance=RequestContext(request))


def view_test2(request):
    return render(request, 'copo/testing2.html')
