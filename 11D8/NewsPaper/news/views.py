from django.shortcuts import render,  redirect
from django.template.loader import render_to_string
from django.views.generic import ListView,  UpdateView, CreateView, DetailView, DeleteView, FormView, View
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from django.core.cache import cache

from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm, SubscribeForm
from .tasks import task_news_created


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-post_created')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = NewsForm()
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)



@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
        if not obj:
            obj = super().get_object(queryset=kwargs['queryset'])
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj



class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'search'
    ordering = ['-post_created']
    paginate_by = 10

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }


#дженерик для получения деталей о товаре
class NewsDetailView(DetailView):
    template_name = '../templates/news_detail.html'
    queryset = Post.objects.all()


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = '../templates/news_create.html'
    form_class = NewsForm
"""    
    def post(self, request, *args, **kwargs):
        #Проверяем что создается новость, а не другой тип контента
        post_type = request.POST['post_type']
        if post_type == 'N':
            #Отбираем категории данной новости
            category_list = request.POST.getlist('id_post_category')
            selected_categories = list(map(int, category_list))
            post_text = request.POST.get('post_text')
            post_header = request.POST.get('post_header')
            pk_post = request.POST.get('post_pk')
            print(request.POST)
            task_news_created.delay(selected_categories, post_text, post_header, pk_post)
        self.object = None
        return super().post(request, *args,**kwargs)  # Сохраняем новость и переходим по get_absolute_url, прописанный в моделе
"""

#Вариант отправки рассылки через view
"""  
    def post(self, request, *args, **kwargs):
        #Проверяем что создается новость, а не другой тип контента
        post_type = request.POST['post_type']
        if post_type == 'N':
            #Отбираем категории данной новости
            category_list = request.POST.getlist('id_post_category')
            selected_categories = list(map(int, category_list))
            #информация для рассылки
            post_text = request.POST.get('post_text')
            post_header = request.POST.get('post_header')
            for cat in selected_categories:
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
        self.object = None
        return super().post(request, *args, **kwargs) #Сохраняем новость и переходим по get_absolute_url, прописанный в моделе
"""

# дженерик для редактирования объекта
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = '../templates/news_create.html'
    form_class = NewsForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class NewsDeleteView(DeleteView):
    template_name = '../templates/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

class SubscribeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        categories = request.user.category_set.all()
        ids = []
        for cat in categories:
            ids.append(cat.pk)

        form = SubscribeForm({'category': ids} if ids else None)

        context = {
            'form': form
        }
        return render(request, '../templates/news_subscribe.html', context)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        category_id = request.POST.getlist('category')
        all_categories = Category.objects.all()
        selected_categories = list(map(int, category_id))
        for category in all_categories:
            if category.pk in selected_categories:
                category.subscriber.add(user)
                category.save()
            else:
                category.subscriber.remove(user)
                category.save()

        return redirect('/news/')


