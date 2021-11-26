from django.forms import ModelForm
from .models import Post, Subscribe
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['id_author', 'post_type', 'post_header', 'id_post_category', 'post_text']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user

class SubscribeForm (ModelForm):
    class Meta:
        model = Subscribe
        fields = ['id_user', 'id_category']