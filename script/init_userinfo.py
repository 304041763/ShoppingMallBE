import os,sys,django
# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ShoppingMallBE.settings")
django.setup()


from apps.keyverification import models

for i in range(1,20):
    models.UserInfo.objects.create(phone='13722222222',
                                   nickname='还好{0}'.format(i),
                                   token='{0}'.format(i),
                                   avatar='user_directory_path/sg.png')

