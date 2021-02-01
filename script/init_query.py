import os, sys, django

# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShoppingMallBE.settings")
django.setup()

from apps.keyverification import models

# News表 一对多 NewsDetail表 反向查询
# 反向查询
a = models.News.objects.get(id=1).news.all().order_by('-id')  # news是models related_name设置名字
print(a)
# 正向查询
# b = models.NewsDetail.objects.filter(id=1).values('news_id__title')  # 从本表news_id跨到表找到title返回
# print(b)

