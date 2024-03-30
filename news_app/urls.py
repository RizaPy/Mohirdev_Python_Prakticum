from django.urls import path
from news_app.views import news_list, news_detail, HopmePageView, ContactPageView, LocalNewsView, ForeingNewsView, TechnologyNewsView, \
    SportNewsView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', HopmePageView.as_view(), name='home_page'),
    path('all', news_list, name='news_list'),
    path('<slug:news>/', news_detail, name='news_detail'),
    path('contact', ContactPageView.as_view(), name='contact_page'),
    # path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('local/', LocalNewsView.as_view(), name='local_page'),
    path('foreing/', ForeingNewsView.as_view(), name='foreing_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_page'),
    path('sport/', SportNewsView.as_view(), name='sport_page'),
]
