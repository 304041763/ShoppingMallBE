import os,sys,django
# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ShoppingMallBE.settings")
django.setup()


from apps.keyverification import models

models.Topic.objects.create(title='Django')
models.Topic.objects.create(title='server 2012')
models.Topic.objects.create(title='PHP')
models.Topic.objects.create(title='CentOS 6.X')
models.Topic.objects.create(title='微信小程序')













