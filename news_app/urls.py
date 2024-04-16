from django.urls import path
from news_app.views import news_list, news_detail, HopmePageView, ContactPageView, LocalNewsView, ForeingNewsView, \
    TechnologyNewsView, SportNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_View, SearchResultView
from accounts.views import user_login
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', HopmePageView.as_view(), name='home_page'),
    path('create', NewsCreateView.as_view(), name='create-page'),
    path('all', news_list, name='news_list'),
    path('<slug:news>/', news_detail, name='news_detail'),
    path('<slug>/update', NewsUpdateView.as_view(),name='news-update'),
    path('<slug>/delete', NewsDeleteView.as_view(), name='news-delete'),
    path('contact', ContactPageView.as_view(), name='contact_page'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),
    path('local', LocalNewsView.as_view(), name='local_page'),
    path('foreing', ForeingNewsView.as_view(), name='foreing_page'),
    path('technology', TechnologyNewsView.as_view(), name='technology_page'),
    path('sport', SportNewsView.as_view(), name='sport_page'),
    path('adminpage/', admin_page_View, name='admin_page'),
    path('news/search_result/', SearchResultView.as_view(), name='search_result'),

]
