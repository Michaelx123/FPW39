# Generated by Django 4.0.2 on 2022-02-13 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_category', models.CharField(choices=[('TK', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('TR', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QG', 'Квестгиверы'), ('SM', 'Кузнецы'), ('TN', 'Кожевники'), ('PT', 'Зельевары'), ('SP', 'Мастера заклинаний')], default='TK', max_length=2)),
                ('header_txt', models.CharField(max_length=255)),
                ('content', tinymce.models.HTMLField(verbose_name='Content')),
                ('id_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_txt', models.TextField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('id_poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poster.poster')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
