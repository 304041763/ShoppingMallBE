from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from apps.keyverification import models
from django.forms import model_to_dict
from rest_framework.views import APIView


class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = ['cover','title','content', 'topic', 'user', 'favor_count', 'create_date']
        # fields = '__all__'


class NewsViews(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.News.objects.all().order_by('-id')[0:5]
        ser = NewsModelSerializer(instance=queryset, many=True)
        return Response(ser.data,status=200)



class CreateNewsTopicModelSerializer(serializers.Serializer):
    key = serializers.CharField()
    cos_path = serializers.CharField()


class CreateNewsModelSerializer(serializers.ModelSerializer):
    imageList = CreateNewsTopicModelSerializer(many=True)

    class Meta:
        model = models.News
        exclude = ['user', 'viewer_count', 'comment_count', 'favor_count']

    def create(self, validated_data):
        image_list = validated_data.pop('imageList')
        news_object = models.News.objects.create(**validated_data)
        data_list = models.NewsDetail.objects.bulk_create(  # bulk_create批量创建
            [models.NewsDetail(**info, news=news_object) for info in image_list]
        )
        news_object.imageList = data_list
        if news_object.topic:
            news_object.topic.count += 1
            news_object.save()
        return news_object


class ListNewsModelSerializer(serializers.ModelSerializer):
    topis = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        models = models.News
        exclude = ['address', ]

    def get_topic(self, obj):
        if not obj.topic:
            return
        return model_to_dict(obj.topic, ['id', 'title'])

    def get_user(self, obj):
        return model_to_dict(obj.user, ['id', 'nickname', 'avatar'])


class ReachBottomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get('minID')
        if not min_id:
            return queryset
        return queryset.filter(id__gt=min_id)


class PullDownRedfreshFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        mix_id = request.query_params.get('mixID')
        if not mix_id:
            return queryset
        return queryset.filter(id__gt=mix_id).reverse()


class NewsView(CreateAPIView, ListAPIView):
    """
    获取动态
    """
    queryset = models.News.objects.prefetch_related('user', 'topic').order_by("-id")

    filter_backends = [ReachBottomFilter, PullDownRedfreshFilter]

    def perform_create(self, serializer):  # 替换默认调用的perform_create
        new_object = serializer.save(user_id=1)
        # 默认就保存News表中的，user_id=1，就是自增长user，调用serializer对象save（但是先调用上面自己create方法把另外两个表数据创建）
        return new_object

    def get_serializer_class(self):
        if self.request.method == 'POST':
            pass
            return CreateNewsModelSerializer
        if self.request.method == 'GET':
            return ListNewsModelSerializer
