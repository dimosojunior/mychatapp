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
def base(request):
    user_object = User.objects.get(username=request.user.username)
    #we are assigning the username of the login user to a field user in post model
    user_profile = Profile.objects.get(user=user_object)
    context ={


        'user_object':user_object,
        'user_profile': user_profile,

    }
    return render(request, "DimosoApp/base.html",context)

def uchafu(request):
    return render(request, "DimosoApp/uchafu.html")

@login_required(login_url='signin')
def home(request):
  #to get a login username then after getting
    user_object = User.objects.get(username=request.user.username)
    #we are assigning the username of the login user to a field user in post model
    user_profile = Profile.objects.get(user=user_object)
    


    
#to see only following users

    user_following_list = [] #make an empty list first
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    posti = Post.objects.all()

    #zinaishia hapa kuona watu uliowafollow tu

    # user suggestion starts, watu ambao hujawafollow
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    #To count Comments
    post = Post.objects.filter()
    post_count = Comments.objects.all().count()
    
    context ={
        
        'post_count':post_count,
        'user_object':user_object,
		'user_profile': user_profile,
		#'posti':posti, #kuona watu wote
        
		'posti':feed_list, #kuona watu uliowafollow tu
        'suggestions_username_profile_list_one': suggestions_username_profile_list[:1],
		'suggestions_username_profile_list': suggestions_username_profile_list
    }


    return render(request, 'DimosoApp/home.html',context)

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)


#HII NI KWA AJILI YA KUPATA PROFILE IMAGE YA KILA USER KWENYE KILA POST
        user_object = User.objects.get(username=request.user.username)
        #we are assigning the username of the login user to a field user in post model
        user_profile = Profile.objects.get(user=user_object)
        new_post.profileimg = user_profile.profileimg
#ZINAISHIA HAPA HIZO
        new_post.save()
        messages.success(request,"Uploaded successfully")
        return redirect('home')
    else:
        messages.success(request,"Uploaded Failed")

    return redirect('home')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'DimosoApp/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username #to get a current login user
    post_id = request.GET.get('post_id')#to get id of that post

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

#check if that post is not already liked by that user before
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
'''
def like_post_at_profile_page(request):
    username = request.user.username #to get a current login user
    post_id = request.GET.get('post_id')#to get id of that post

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

#check if that post is not already liked by that user before
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/profile/'+user)
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/profile/'+user)

'''




@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    
    

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,

        
    }
    return render(request, 'DimosoApp/profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)

            #HII NI KWA AJILI YA KUPATA PROFILE IMAGE YA KILA USER KWENYE KILA POST
            user_object = User.objects.get(username=request.user.username)
            #we are assigning the username of the login user to a field user in post model
            user_profile = Profile.objects.get(user=user_object)
            new_follower.profileimg = user_profile.profileimg
        #ZINAISHIA HAPA HIZO


            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'DimosoApp/setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                
                user.save()
                #HIZI NI KWA AJILI KUTUMA EMAIL ENDAPO MTU AKIJISAJILI
                
                #subject = "Welcome to UniChatting App"
                #message = f"Thanks {username}  for registering in our system as {email}, sasa unaweza kutembelea mfumo wetu au kuwasiliana nasi kupitia email juniordimoso8@gmail.com au dimosoeljunior8@gmail.com "
                #from_email = settings.EMAIL_HOST_USER
                #recipient_list = [email]
                #send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            #ZINAISHIA HAPA ZA KUTUMA EMAIL

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'DimosoApp/signin.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'DimosoApp/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


def PostDetailView(request, id):
    try:
        post = Post.objects.get(id=id)
    except:
        raise Http404("Post Does Not Exist")    

    #post.read+=1
    #post.save()

    if request.method == 'POST':
        comm = request.POST.get('comm')
        comm_id = request.POST.get('comm_id') #None

        if comm_id:
            SubComment(post=post,
                    user = request.user,
                    comm = comm,
                    comment = Comments.objects.get(id=int(comm_id))
                ).save()
        else:
            Comments(post=post, user=request.user, comm=comm).save()

    post_count = Comments.objects.filter(post=post).count()
    reply_count = SubComment.objects.filter(post=post).count()
    total_count = post_count + reply_count
    comments = []
    for c in Comments.objects.filter(post=post).order_by('-id'):
        comments.append([c, SubComment.objects.filter(comment=c)])
    context = {
        'post_count':post_count,
        'reply_count':reply_count,
        'total_count':total_count,
        'comments':comments,
        'post':post,
        'pop_post': Post.objects.order_by('-id')[:9],
        }
    return render(request, 'DimosoApp/PostDetailView.html', context)
