from django.contrib import admin
from django.urls import path, re_path
from apps.web.views import blogAdd

urlpatterns = [
    # path('userprofile/', include('apps.userprofile.urls'))
    # path(r'news/', news.NewsViews.as_view()),
    # re_path(r'news/(?P<pk>\d+)/', news.NewDetailsViews.as_view()),  # 使用正则
    # # path(r'news/<int:pk>/', news.NewDetailsViews.as_view()),    #使用int类型
    # path(r'commnet/', news.CommentViews.as_view()),    #使用int类型
    # #详细详解在 https://www.cnblogs.com/feixuelove1009/p/8399338.html
    # path(r'news/', news.NewsViews.as_view()),   # 文章列表
    # path(r'topic/', news.TopicViews.as_view()),   # 话题列表
    # path(r'release/', news.ReleaseViews.as_view()),   # 发布页面
    path(r'blog/item/list/', blogAdd.blog_item_list, name='blog_list'),
    re_path(r'blog/item/add/', blogAdd.blog_item_add, name='blog_add'),
    re_path(r'blog/item/del/', blogAdd.blog_item_del, name='blog_del'),
    # re_path(r'blog/item/del/<int:pk>', blogAdd.blog_item_del, name='blog_del'),
]
