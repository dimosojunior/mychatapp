from DimosoApp.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    }))

    class Meta:
        model = Comment
        fields = ('content', )
class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
    class Meta:
        model = ChatMessage
        fields = ["body",]

class ExtendedProfileForm(forms.ModelMultipleChoiceField):

    def label_from_instance(self,friends):
        return "%" %friends.user.username

class CreateProfileForm(forms.ModelForm):
    
    
    class Meta:
        model = Profile
        fields = ["friends"]

        friends = ExtendedProfileForm(


                queryset = Friend.objects.all(),
                
                widget=forms.CheckboxSelectMultiple(),

            )

class CreateProfileForm(forms.ModelForm):
    
    
    class Meta:
        model = Profile
        fields = ["friends"]

        friends = ExtendedProfileForm(


                queryset = Friend.objects.all(),
                
                widget=forms.CheckboxSelectMultiple(),

            )

class AddFriendToProfileForm(forms.ModelForm):
    
    
    
    
    class Meta:
        model = Friend
        fields = ["profile"]

        
        