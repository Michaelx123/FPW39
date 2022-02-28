from django.db import models
from django.contrib.auth.models import User
from tinymce import HTMLField
from django.utils.encoding import smart_str


class Poster(models.Model):
    CATEGORIES = [
        ('TK', 'Танки'),
        ('HL', 'Хилы'),
        ('DD', 'ДД'),
        ('TR', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('SM', 'Кузнецы'),
        ('TN', 'Кожевники'),
        ('PT', 'Зельевары'),
        ('SP', 'Мастера заклинаний')
    ]

    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_category = models.CharField(max_length=2, choices=CATEGORIES, default='TK')
    header_txt = models.CharField(max_length=255)
    content = HTMLField('Content')


class Response(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_poster = models.ForeignKey(Poster, on_delete=models.CASCADE)
    response_txt = models.TextField()
    is_accepted = models.BooleanField(default=False)