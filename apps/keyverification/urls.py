from django.contrib import admin
from django.urls import path
from apps.views.views import news
from apps.keyverification.views import topics

urlpatterns = [
    # path('userprofile/', include('apps.userprofile.urls'))
    # path(r'news/', news.NewsViews.as_view()),
    path(r'credential/', topics.OssCredentialView.as_view()),  # 密钥端口
]
