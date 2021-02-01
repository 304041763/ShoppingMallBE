from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import ListAPIView
from apps.keyverification import models


# Create your views here.

class OssCredentialView(APIView):
    """
    获得秘钥
    """
    def get(self, request, *args, **kwargs):
        from utils.oss import get_credential
        return Response(get_credential())


class TopicSerializer(ModelSerializer):
    """
    话题的序列化
    """
    class Meta:
        model = models.Topic
        fields = "__all__"


class TopicView(ListAPIView):
    """
    所有话题
    """
    serializer_class = TopicSerializer
    queryset = models.Topic.objects.all().order_by('-count')
