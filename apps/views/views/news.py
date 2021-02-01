from django.db.models import Q
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, ListCreateAPIView
from apps.keyverification import models
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.forms import model_to_dict
from ShoppingMallBE.settings import MEDIA_URL, server_URL


class NewsModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format="%Y-%m-%d")  # 自定义创建时间

    class Meta:
        model = models.News
        # fields = ['id', 'cover', 'content', 'topic', 'user', 'favor_count', ]
        fields = ['id', 'cover', 'title', 'content', 'topic', 'user', 'favor_count', 'create_date', 'state']
        # fields ='__all__'

    def get_user(self, obj):
        avatar = server_URL + MEDIA_URL + str(obj.user.avatar)  # 拼接头像URL
        return {'id': obj.user_id, 'nickname': obj.user.nickname, 'avatar': avatar}
        # return model_to_dict(obj.user, fields=['id', 'nickname', 'str(avatar)'])

    def get_topic(self, obj):
        if not obj.topic:
            return
        # return {'id': obj.topic_id, 'title': obj.topic.title}
        return model_to_dict(obj.topic, fields=['id', 'title'])


# 方法一 APIView
"""
class NewsViews(APIView):
    def get(self, request, *args, **kwargs):
        minId = request.query_params.get('minId')
        maxId = request.query_params.get('maxId')
        if minId:
            queryset = models.News.objects.filter(id__lt=minId).order_by('-id')[0:10]  # 获得比minId更小的id
        elif maxId:
            queryset = models.News.objects.filter(id__gt=maxId).order_by('id')[0:10]  # 获得比minId更大的id
        else:
            queryset = models.News.objects.all().order_by('-id')[0:10]

        ser = NewsModelSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)
"""

# 方法二：ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import BaseFilterBackend


# 动态切片 http://127.0.0.1:8000/api/nuew/?limit=2&offset=8
class OldNewsListPagination(LimitOffsetPagination):
    """
    分页器
    """
    default_limit = 5  # 默认切多少条
    max_limit = 50  # 最大切多少
    limit_query_param = 'limit'  # 取多少条的参数
    offset_query_param = 'offset'  # 取哪条开始取

    def get_offset(self, request):  # 重写offset_query_param
        return 0

    def get_paginated_response(self, data):  # 重写,可定制页面展示的格式
        return Response(data)


class MinFilterBackend(BaseFilterBackend):  # 处理分页
    def filter_queryset(self, request, queryset, view):
        minId = request.query_params.get('minId')
        if minId:
            queryset = queryset.filter(id__lt=minId).order_by('-id')
            return queryset
        return queryset


class MaxFilterBackend(BaseFilterBackend):  # 处理刷新
    def filter_queryset(self, request, queryset, view):
        maxId = request.query_params.get('maxId', )
        if maxId:
            queryset = queryset.filter(id__gt=maxId).order_by('id')
            return queryset
        return queryset


class NewsViews(ListAPIView):
    queryset = models.News.objects.all().order_by('-id')
    serializer_class = NewsModelSerializer  # serializer_class是固定的
    pagination_class = OldNewsListPagination
    filter_backends = [MinFilterBackend,  # 处理最小的ID做法
                       MaxFilterBackend,  # 处理最大的ID做法
                       ]  # filter_backends根据条件


class TopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        # fields = ['id', 'cover', 'content', 'topic', 'user', 'favor_count', ]
        fields = '__all__'


class TopicViews(ListAPIView):
    """
    话题
    """
    queryset = models.Topic.objects.all().order_by('id')
    serializer_class = TopicModelSerializer


class NewsDetailsModelSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format="%Y-%m-%d")  # 自定义创建时间

    class Meta:
        model = models.News
        # fields = '__all__'
        exclude = ['cover', ]

    def get_images(self, obj):
        detail_queryset = models.NewsDetail.objects.filter(news=obj)  # 自定义所有图片
        # return [row.cos_path for row in detail_queryset]   # 方法一
        # return [{'id': row.id, 'path': row.cos_path} for row in detail_queryset]  # 方法二和方法三显示是一样的
        return [model_to_dict(row, fields=['id', 'cos_path']) for row in detail_queryset]  # 方法三 model_to_dict

    # def create_date(self,obj):    # 自定义创建时间和上面方法一样
    #     obj_create_date = obj.create_date.strftime("%Y-%m-%d") import datetime
    #     return obj_create_date

    def get_user(self, obj):  # 自定义用户
        return {'id': obj.user_id, 'nickname': obj.user.nickname, 'avatar': obj.user.get_avatar_url()}
        # return model_to_dict(obj.user, fields=['id', 'nickname', 'str(avatar)'])

    def get_topic(self, obj):  # 自定义话题
        if not obj.topic:
            return
        # return {'id': obj.topic_id, 'title': obj.topic.title}
        return model_to_dict(obj.topic, fields=['id', 'title'])

    def get_viewer(self, obj):
        # viewer_queryset = models.ViewerRecord.objects.filter(news=obj).order_by('-id')[:5]
        queryset = models.ViewerRecord.objects.filter(news=obj)
        viewer_queryset = queryset.order_by('-id')[:5]
        context = {
            'count': queryset.count(),
            'result': [{'user_id': row.user.nickname, 'avatar': row.user.get_avatar_url()} for row in viewer_queryset],
        }
        return context
        # return [model_to_dict(row.user, fields=['nickname',row.user.avatar]) for row in viewer_queryset]

    def get_comment(self, obj):
        # 获取一级评论
        first_queryset = models.CommentRecord.objects.filter(news=obj, depth=1).order_by('-id').values(
            'id', 'content', 'depth', 'user__nickname', 'user__avatar', 'create_date')
        # 获取二级评论(取一级评论下的二级评论,id最大的)
        first_id_list = [item['id'] for item in first_queryset]
        from django.db.models import Max
        result = models.CommentRecord.objects.filter(
            news=obj, depth=2, reply__id__in=first_id_list).values('reply_id').annotate(max_id=Max('id'))
        secon_id_list = [item['max_id'] for item in result]
        second_queryset = models.CommentRecord.objects.filter(id__in=secon_id_list).values(
            'id', 'content', 'user__nickname', 'user__avatar', 'create_date', 'reply_id', 'reply__user__nickname')
        # 做返回列表
        import collections
        first_dict = collections.OrderedDict()  # 生成有序列表
        for item in first_queryset:  # 加入一级评论
            item['create_date'] = item['create_date'].strftime('%Y-%m-%d')  # 修改返回的时间格式
            item['user__avatar'] = server_URL + MEDIA_URL + item['user__avatar']  # 拼接返回带域名URL
            first_dict[item['id']] = item  # 增加到有序的列表中

        for node in second_queryset:  # 加入二级评论
            node['create_date'] = node['create_date'].strftime('%Y-%m-%d')  # 修改返回的时间格式
            node['user__avatar'] = server_URL + MEDIA_URL + node['user__avatar']  # 拼接返回带域名URL
            first_dict[node['reply_id']]['child'] = [node, ]

        return first_dict.values()


class NewDetailsViews(RetrieveAPIView):  # RetrieveAPIView适合取一条数据
    """
    动态详细
    """
    queryset = models.News.objects
    serializer_class = NewsDetailsModelSerializer


##################获取所有子评论#####################
class CommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d')
    user__nickname = serializers.CharField(source='user.nickname')  # 重新返回的字典的名称
    user__avatar = serializers.CharField(source='user.get_avatar_url')  # 重新返回的字典的名称
    reply_id = serializers.CharField(source='reply.id')
    reply__user__nickname = serializers.CharField(source='reply.user.nickname')

    class Meta:
        model = models.CommentRecord
        # fields = '__all__'
        exclude = ['news', 'user', 'reply', 'root']
    # def get_user(self, obj):  # 自定义用户
    #     return {'id': obj.user_id, 'nickname': obj.user.nickname, 'avatar': obj.user.get_avatar_url()}
    # return model_to_dict(obj.user, fields=['id', 'nickname', 'str(avatar)'])
    # def get_reply_user(self,obj):
    #     return model_to_dict(obj.reply.user, fields=['id', 'nickname'])


class CreateCommentModelSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    # read_only=True的意思是不用提交数据,但是序列化返回数据库中的值

    user__nickname = serializers.CharField(source='user.nickname', read_only=True)  # 重新返回的字典的名称
    user__avatar = serializers.CharField(source='user.get_avatar_url', read_only=True)  # 重新返回的字典的名称

    reply_id = serializers.CharField(source='reply.id', read_only=True)
    reply__user__nickname = serializers.CharField(source='reply.user.nickname', read_only=True)

    class Meta:
        model = models.CommentRecord
        # fields = '__all__'
        exclude = ['user', 'favor_count']


from rest_framework import status
from django.db.models import F


class CommentViews(APIView):
    def get(self, request, *args, **kwargs):
        root_id = request.query_params.get('root')
        # 1. 获得这个根评论的所有子孙评论
        node_queryset = models.CommentRecord.objects.filter(root_id=root_id).order_by('id')
        # 2.序列化
        ser = CommentModelSerializer(instance=node_queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        1. 进行数据校验
            1.1 校验格式要跟返回值一样
        2. 校验通过,保存数据库
        3. 将保存到数据库的数据返回小程序页面
        """

        ser = CreateCommentModelSerializer(data=request.data)
        if ser.is_valid():
            ser.save(user_id=1)
            # print(ser.data)
            # 评论+1
            news_id = ser.data.get('news')
            models.News.objects.filter(id=news_id).update(comment_count=F('comment_count') + 1)
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


##########################测试################################
"""

class CreateNewsDetailModelSerializer(serializers.ModelSerializer):
    # 轮播图序列化
    # news_id = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsDetail
        # fields = '__all__'
        exclude = ['news_id']

    # def create(self, validated_data):
    #     print(validated_data)
    #     images = models.NewsDetail(
    #         key=validated_data['key'],
    #         cos_path=validated_data['cos_path'],
    #         # news_id=validated_data['']
    #     )
    #     images.save()
    #     return images

class CreateViewModelSerializer(serializers.ModelSerializer):
    # newsList = models.News.objects.get(id=1).news.all()
    # images = serializers.CharField(source=newsList,many=True)
    # user = serializers.SerializerMethodField()
    # topic = serializers.SerializerMethodField()
    images = CreateNewsDetailModelSerializer(many=True)

    # images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    create_date = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)  # 自定义创建时间

    class Meta:
        model = models.News
        fields = ['id', 'cover', 'title', 'content', 'topic',
                  'user', 'favor_count', 'state', 'create_date', 'images']
        # exclude = ['comment_count', 'viewer_count']
"""


class CreateNewsDetailModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    cos_path = serializers.CharField()


class CreateNewsModelSerializer(serializers.ModelSerializer):
    imageList = CreateNewsDetailModelSerializer(many=True)

    class Meta:
        model = models.News
        exclude = ['user', 'viewer_count', 'comment_count', 'favor_count']
        # fields = '__all__'

    def create(self, validated_data):
        image_list = validated_data.pop('imageList')  # 增加imageList对象
        news_object = models.News.objects.create(**validated_data)   # 创建外键
        data_list = models.NewsDetail.objects.bulk_create(  # bulk_create批量创建
            [models.NewsDetail(**info, news=news_object) for info in image_list] #循环创建追主键
        )
        news_object.imageList = data_list
        return news_object


# class ReleaseViews(APIView):
#     def post(self, request, *args, **kwargs):
#         ser = CreateNewsModelSerializer(data=request.data)
#         print('post请求',request.data)
#         print('CreateNewsModelSerializer',CreateNewsModelSerializer)
#         if ser.is_valid():
#             ser.save()
#             print(ser.data)
#             return Response(ser.data, status=status.HTTP_201_CREATED)
#         return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ReleaseViews(ListCreateAPIView):
    """
    简单的情况下 和ReleaseViews(APIView):效果是一样的
    path('users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
    header: { 一个大坑，微信小程序必须用json 格式
        "Content-Type": "application/json"  //指定请求格式是json
      },
    """
    serializer_class = CreateNewsModelSerializer
    # print(repr(serializer_class)) 打印