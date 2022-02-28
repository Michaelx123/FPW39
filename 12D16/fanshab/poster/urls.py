from django.urls import path
from .views import PosterList,PosterCreateView

urlpatterns = [
    path('', PosterList.as_view()),
    path('create/', PosterCreateView.as_view(), name='create'),
]