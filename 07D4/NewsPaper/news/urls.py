from django.urls import path
from .views import NewsList, NewDetail, NewsSearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView
urlpatterns = [
    path('', NewsList.as_view()),
    #path('<int:pk>', NewDetail.as_view()),
    path('search', NewsSearch.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
]
