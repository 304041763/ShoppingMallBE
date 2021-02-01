import os,sys,django
# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ShoppingMallBE.settings")
django.setup()


from apps.keyverification import models

for i in range(10,13):
    models.ViewerRecord.objects.create(user_id='{0}'.format(i),news_id=36)
    # 用户1-10看过文章ID 36