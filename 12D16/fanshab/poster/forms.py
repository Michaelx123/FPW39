from django.forms import ModelForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Poster
from tinymce.widgets import TinyMCE



class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class PosterForm(ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Poster
        #fields = ['id_category', 'header_txt', 'content']
        fields = ['id_category', 'header_txt']
