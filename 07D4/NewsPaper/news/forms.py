from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['id_author', 'post_type', 'post_header', 'id_post_category', 'post_text']