import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from datetime import datetime, timedelta
from ...models import Post, Category, User

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
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


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            #trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week=0, hour=10, minute=25),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")