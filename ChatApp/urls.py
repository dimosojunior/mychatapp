
from django.urls import path
from . import views

urlpatterns = [
    
    path('index/', views.index, name="index"),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
    path('followers/', views.followers, name="followers"),
    path('following/', views.following, name="following"),
    #path('choose_friends/', views.choose_friends, name="choose_friends"),
    #path('chat/', views.chat, name="chat"),
    path('AddFriend/<int:pk>/', views.AddFriend.as_view(), name="AddFriend"),
    path('AddFriendToProfileModel/', views.AddFriendToProfileModel.as_view(), name="AddFriendToProfileModel"),

]