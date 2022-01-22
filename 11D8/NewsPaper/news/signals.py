from django.db.models.signals import m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Post, User, Category
from .tasks import task_news_created


#Вариант отправки рассылки через signal + tasks
@receiver(m2m_changed, sender=Post.id_post_category.through)
def Post_created_mailing(sender, **kwargs):
    action = kwargs.pop('action', None)
    if action == 'post_add':
        instance = kwargs.pop('instance', None)
        #Убираем работу с celery, чтобы не мешала
        #task_news_created.delay(instance.pk)


"""
#Вариант отправки рассылки через signal
@receiver(m2m_changed, sender=Post.id_post_category.through)
def Post_created_mailing(sender, **kwargs):
    action = kwargs.pop('action', None)
    if action == 'post_add':
        instance = kwargs.pop('instance', None)
        pk_set = kwargs.pop('pk_set', None)
        post_type = instance.post_type
        if post_type == 'N':
            selected_categories = list(map(int, pk_set))
            post_text = instance.post_text
            post_header = instance.post_header
            pk_post=instance.pk
            for cat in selected_categories:
                print(cat)
                category_name = Category.objects.get(pk=cat).category_name
                #Отбираем всех пользователей, подписанных на данную категорию
                subscribers = User.objects.filter(category__pk=cat)
                for subs in subscribers:
                    print(subs.email)
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
"""