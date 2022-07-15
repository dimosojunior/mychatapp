from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from DimosoApp.models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=('user', 'caption', 'created_at', 'no_of_likes')
    search_fields=('user', 'caption', 'created_at')
    
    
    list_filter=('created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'post', 'content', 'date')

class CommentsAdmin(admin.ModelAdmin):
    list_display=('user', 'post', 'comm', 'time')
class SubCommentAdmin(admin.ModelAdmin):
    list_display=('user', 'post', 'comm', 'time')

class MessageAdmin(admin.ModelAdmin):
    list_display=('user', 'room', 'value', 'date')
#admin.site.register(MyUser, MyUserAdmin)

admin.site.register(Profile)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(SubComment,SubCommentAdmin)
admin.site.register(Friend)
admin.site.register(ChatMessage)
admin.site.register(Message,MessageAdmin)
admin.site.register(Room)