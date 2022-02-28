from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Poster, Response
from .forms import PosterForm
from django.shortcuts import redirect
#from django.shortcuts import render
# Create your views here.


class PosterList(ListView):
    model = Poster
    template_name = 'posters.html'
    context_object_name = 'posterList'
    queryset = Poster.objects.all()
    paginate_by = 10


class PosterCreateView(LoginRequiredMixin, CreateView):
    model = Poster
    template_name = '../templates/create.html'
    form_class = PosterForm

    def post(self, request, *args, **kwargs):
        post = Poster(
            id_user=request.user,
            id_category=request.POST['id_category'],
            header_txt=request.POST['header_txt']
            #content=request.POST['content']
        )
        post.save()

        return redirect('../posters/')