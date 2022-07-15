from django.shortcuts import render
from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, FormView, DetailView, DeleteView, UpdateView, ListView

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json
from django.db.models import Q
import datetime
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from reportlab.lib.pagesizes import landscape
#from reportlab.platypus import Image
import os
from django.conf import settings
from django.http import HttpResponse
#from django.template.loader import get_template
#from xhtml2pdf import pisa
#from django.contrib.staticfiles import finders
import calendar
from calendar import HTMLCalendar
from DimosoApp.models import *
from DimosoApp.forms import *
#from hitcount.views import HitCountDetailView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.contrib.auth.models import User, auth
from hitcount.views import HitCountDetailView


# Create your views here.

def followers(request):
    #user = User.objects.all()
    #TO DISPLAY FOLLOWERS OF A SPECIFIC USER
    user_following = FollowersCount.objects.filter(user =request.user.username).order_by('-id')
    
    context = {"user_following": user_following}
    return render(request, "ChatApp/followers.html",context)


def following(request):
    user = User.objects.all()
    #TO DISPLAY FOLLOWERS OF A SPECIFIC USER
    user_following = FollowersCount.objects.filter(user =request.user.username).order_by('-id')
    
    context = {"user_following": user_following}
    return render(request, "ChatApp/following.html",context)





def index(request):
    #all_user = User.objects.all()
    user = request.user.profile
    friends = user.friends.all().order_by('-id')
    context = {
        "user": user, 
        "friends": friends,
        #"all_user":all_user
    }
    return render(request, "ChatApp/index.html",context)
def detail(request,pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user":user,"profile":profile, 
               "chats": chats , "num": rec_chats.count()}
    return render(request, "ChatApp/detail.html", context)

def sentMessages(request, pk):
	user = request.user.profile
	friend = Friend.objects.get(profile_id=pk)
	profile = Profile.objects.get(id=friend.profile.id)
	data = json.loads(request.body)
	new_chat = data["msg"]
	new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False )
	print(new_chat)

	return JsonResponse(new_chat_message.body, safe=False)

def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)


class AddFriend(UpdateView):
    model=Profile
    form_class = CreateProfileForm
    template_name = 'ChatApp/AddFriend.html'
    success_url = reverse_lazy('index')
class AddFriendToProfileModel(CreateView):
    model=Friend
    form_class = AddFriendToProfileForm
    template_name = 'ChatApp/AddFriendToProfileModel.html'
    success_url = reverse_lazy('AddFriendToProfileModel')