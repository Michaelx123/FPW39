from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from .models import Post, User, Category, PostCategory


@shared_task
def task_news_created(pk_post):
    post = Post.objects.get(pk=pk_post)
    selected_categories = PostCategory.objects.filter(id_post=pk_post)
    post_text = post.post_text
    post_header = post.post_header
    print(pk_post)
    for cat in selected_categories:
        category_name = cat.id_category
        # Отбираем всех пользователей, подписанных на данную категорию
        subscribers = User.objects.filter(category__pk=cat.id_category.pk)
        for subs in subscribers:
            print(f'{subs.email} ({category_name})')
            html_content = render_to_string(
                '../templates/category_mailing.html',
                {
                    'username': subs.username,
                    'category_name': category_name,
                    'post_text': post_text,
                    'pk_post': pk_post,
                }
            )
            msg = EmailMultiAlternatives(
                subject=post_header,
                body=post_text,
                from_email='mklink@yandex.ru',
                to=[subs.email],
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()

@shared_task
def task_weekly_mailing():
#Подборка статей(A) за неделю, новости(N) не включем, т.к. по ним приходит письмо, при создании новости.
    post_week = Post.objects.filter(post_created__range=[datetime.today()-timedelta(days=7), datetime.today()], post_type='A')
    if post_week.exists():
        subscribers = User.objects.all()
        for subs in subscribers:
            #отбираем все категории на которые подписан пользователь
            subs_category = Category.objects.filter(subscriber__pk=subs.id)
            #подбираем статьи из категорий пользователя
            user_posts = post_week.filter(id_post_category__in=subs_category)
            if user_posts.exists():
                print(subs.email)
                html_content = render_to_string(
                    '../templates/weekly_mailing.html',
                    {
                        'username': subs.username,
                        'user_posts': user_posts,

                    }
                )
                msg = EmailMultiAlternatives(
                    subject='Подборка статей за неделю',
                    body='',
                    from_email='mklink@yandex.ru',
                    to=[subs.email],
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()
    print('Рассылка окончена.')