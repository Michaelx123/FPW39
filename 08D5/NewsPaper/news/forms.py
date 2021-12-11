from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['id_author', 'post_type', 'post_header', 'post_text']
        
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user