from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView

from .models import Category, News
from .forms import ContactForm
# Create your views here.

def news_list(request):
    news_list = News.objects.all()

    context = {
        'news_list':news_list
    }

    return render(request, 'news/news_list.html', context=context)

def news_detail(request, news):

    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    return render(request, 'news/detail.html', {'news':news})

# def HomePage(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:4]
#     local_one = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]
#     sossial_one = News.published.filter(category__name = 'Jamiyat').order_by('-publish_time')[:1]
#     sossial_news = News.published.all().filter(category__name="Jamiyat").order_by('-publish_time')[1:6]
#     tex_one = News.published.all().filter(category__name='Fan-texnika').order_by('-publish_time')[:1]
#     tex_news = News.published.all().filter(category__name='Fan-texnika').order_by('-publish_time')[1:6]
#
#     context = {
#         'news_list':news_list,
#         'categories':categories,
#         'local_one':local_one,
#         'local_news':local_news,
#         'sossial_one':sossial_one,
#         'sossial_news':sossial_news,
#         'tex_one':tex_one,
#         'tex_news':tex_news,
#     }
#     return render(request, 'news/index.html', context)

class HopmePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:4]
        # context['local_one'] = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:1]
        context['local_news'] = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:5]
        # context['sossial_one'] = News.published.all().filter(category__name="Jamiyat").order_by('-publish_time')[1:6]
        context['sossial_news'] = News.published.all().filter(category__name="Jamiyat").order_by('-publish_time')[:5]
        # context['tex_one'] = News.published.all().filter(category__name='Fan-texnika').order_by('-publish_time')[:1]
        context['tex_news'] = News.published.all().filter(category__name='Fan-texnika').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]
        return context


# def ContactPage(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('<h2> Thank you for Contact us! </h2>')
#
#     context = {
#     'form':form
#     }
#
#     return render(request, 'news/contact.html', context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form':form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2> Thank you for Contact us! </h2>")
        context = {
            'form':form
        }

        return render(request, 'news/contact.html', context)

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local.html'
    context_object_name = 'mahalliy'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeingNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'texnologiya'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Fan-texnika')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news