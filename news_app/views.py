from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model

from news_app.custom_permission import OnlyLoggedSuperUser
from hitcount.views import  HitCountMixin


from .models import Category, News
from .forms import ContactForm, CommentForm


# Create your views here.

def news_list(request):
    news_list = News.objects.all()

    context = {
        'news_list':news_list
    }

    return render(request, 'news/news_list.html', context=context)



# @require_POST
def news_detail(request, news):

    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits +1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        #yangi commnet obyektini yaratamiz lekin MB ga yozmaymiz
        new_comment = comment_form.save(commit=False)
        new_comment.news = news
        #izoh egasini so'rov yuborayotgan userga bog'laymiz
        new_comment.user = request.user
        #MB da saqlaymiz
        new_comment.save()
        comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news':news,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form
}

    return render(request, 'news/detail.html', context )


# @require_POST
# def news_detail(request, news):
#     # get the article by article_id
#     news = get_object_or_404(News, status=News.Status.Published)
#     comment = None
#
#     # A comment form
#     form = CommentForm(data=request.POST)
#
#     if form.is_valid():
#         # Create a Comment object before saving it to the database
#         comment = form.save(commit=False)
#
#         # Assign the article to the comment
#         comment.news = news
#         # Save the comment to the database
#         comment.save()
#         pass
#
#     return render(request, 'news/detail.html', {'news': news, 'form': form, 'comment': comment})
#
#     pass


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


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'body', 'category', 'status', 'image']
    template_name = 'crud/detail_update.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/create.html'
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    success_url = reverse_lazy('home_page')

# @login_required
# @user_passes_test(lambda u: u.is_superuser)
# def admin_page_View(request):
#     admin_user = User.objects.filter(is_superuser=True)
#     context = {
#         'admin_user': admin_user
#     }
#     return render(request, 'pages/admin_page.html', context)


def admin_page_View(request):
    # Filter superusers
    admin_users = User.objects.filter(is_superuser=True)
    # Check if there are any superusers
    if admin_users.exists():
        context = {
            'admin_users': admin_users
        }
    else:
        context = {
            'admin_users': None  # Provide an empty list or None if no superusers exist
        }

    return render(request, 'admin_page.html', context)

class SearchResultView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        barcha_yangiliklar = News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return barcha_yangiliklar