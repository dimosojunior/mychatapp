
from django.urls import path
from . import views

urlpatterns = [
    path('homepage', views.homepage, name="homepage"),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),

    path('sample', views.sample, name="sample"),

    #path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
        
]