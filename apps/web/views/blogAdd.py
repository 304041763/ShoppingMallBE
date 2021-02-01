from apps.keyverification import models
from django.shortcuts import render
from django.forms import ModelForm
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage
from rest_framework import serializers
from ShoppingMallBE.settings import MEDIA_URL, server_URL
from django.forms import model_to_dict


def blog_item_list(request):
    blog_list = models.News.objects.prefetch_related().all().order_by('id')  # 获取所有数据
    # blog_list = models.News.objects.all().select_related("topic","user")  # 获取所有数据
    # blog_list = NewsModelSerializer()
    # queryset = models.News.objects.select_related("topic","user") # 查询News表的'topic'值
    # for book in queryset:
    #     # print(book.topic)
    #     # print({'id': book.topic_id, 'title': book.topic})
    #     topic_li ={'id': book.topic_id, 'title': book.topic}
    #     user_li={'id': book.user_id, 'title': book.user}
    # queryset = models.News.objects.all().select_related("topic_id","user_id")

    paginator = Paginator(blog_list, 5)  # 分页功能，每页分7个
    if request.method == 'GET':
        blog_object = paginator.page(1)  # 默认返回一页数据
        context = {
            'blog_object': blog_object,
        }
        return render(request, 'homepage.html', context)

    if request.is_ajax():
        page = request.POST.get('page')  # 获取点击的页数
        # print(request.POST.get('page'))
        try:
            blogs = paginator.page(page)  # 根据页数获取数据
        except PageNotAnInteger:
            blogs = paginator.page(1)  # 如果不是整数返回也第一页
        except InvalidPage:
            blogs = paginator.page(paginator.num_pages)  # 页数不合法返回最后一个页

        # 指定返回值topic__title，user__nickname是跨表
        blog_li = list(blogs.object_list.values('id','cover', 'title', 'content',
                                                'address', 'favor_count', 'viewer_count',
                                                'comment_count', 'create_date', 'state',
                                                'topic__title', 'user__nickname', ))

        # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
        result = {'has_previous': blogs.has_previous(),
                  'has_next': blogs.has_next(),
                  'num_pages': blogs.paginator.num_pages,
                  'blog_li': blog_li,
                  }
        # print('222222',result)
        return JsonResponse(result)


class BlogAddModelForm(ModelForm):
    class Meta:
        model = models.News
        exclude = ['comment_count', 'create_date', 'viewer_count', 'favor_count']

    def __init__(self, *args, **kwargs):
        super(BlogAddModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


def blog_item_add(request):
    if request.method == "POST":
        # print(request.POST)
        form = BlogAddModelForm(request.POST)
        if form.is_valid():
            form.save()
            blog_list = models.News.objects.prefetch_related().all().order_by('id')  # 获取所有数据
            paginator = Paginator(blog_list, 5)  # 分页功能，每页分7个
            blog_object = paginator.page(1)  # 默认返回一页数据
            context = {
                'blog_object': blog_object,
                'form': form,
            }
            return render(request, 'homepage.html', context)
    form = BlogAddModelForm()
    context = {
        'form': form,
    }
    return render(request, 'content/blog_item_add.html', context)



def blog_item_del(request):
    # print(request.GET.get('pk'))
    news_id = request.GET.get('pk')
    models.News.objects.filter(id=news_id).delete()
    return JsonResponse({'status':True})
