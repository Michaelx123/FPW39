from django.urls import path
#from django.contrib.auth.views import LoginView, LogoutView
from .views import NewsList, NewDetail, NewsSearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, upgrade_me, SubscribeView
from django.views.decorators.cache import cache_page


urlpatterns = [
    #path('', cache_page(60)(NewsList.as_view())), плохой способ кэшировани при удалении
    path('', NewsList.as_view()),
    #path('<int:pk>', NewDetail.as_view()),
    path('search', NewsSearch.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]
