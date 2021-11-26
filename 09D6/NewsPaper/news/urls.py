from django.urls import path
#from django.contrib.auth.views import LoginView, LogoutView
from .views import NewsList, NewDetail, NewsSearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, upgrade_me, SubscribeUpdateView



urlpatterns = [
    path('', NewsList.as_view()),
    #path('<int:pk>', NewDetail.as_view()),
    path('search', NewsSearch.as_view()),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('create/<int:pk>', NewsUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', NewsDeleteView.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('subscribe', SubscribeUpdateView.as_view(), name='news_subscribe'),
    #path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    #path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    #path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
]
