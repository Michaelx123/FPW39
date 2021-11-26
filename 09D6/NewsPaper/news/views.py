from django.shortcuts import render, redirect
from django.views.generic import ListView,  UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from .models import Post, Subscribe
from .filters import NewsFilter
from .forms import NewsForm, SubscribeForm


class NewsList(LoginRequiredMixin, ListView):
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


class SubscribeUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscribe
    template_name = '../templates/news_subscribe.html'
    form_class = SubscribeForm
    #queryset = Subscribe.objects.filter(id_user=User.objects.get())
