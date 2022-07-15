
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    #path('index/', views.index, name="index"),
    path('base/', views.base, name="base"),
    path('uchafu/', views.uchafu, name="uchafu"),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    #path('like_post_at_profile_page', views.like_post_at_profile_page, name="like_post_at_profile_page"),
    
    path('PostDetailView/<int:id>/', views.PostDetailView, name="PostDetailView"),
]