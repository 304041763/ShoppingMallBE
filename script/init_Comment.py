import os,sys,django
# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE","ShoppingMallBE.settings")
django.setup()


from apps.keyverification import models


first1 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-1',
        user_id=1,
        depth=1,)

first1_1 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-1-1',
        user_id=6,
        reply=first1,
        depth=2,
        root=first1)

first1_1_1 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-1-1-1',
        user_id=10,
        reply=first1_1,
        depth=3,root=first1)

first1_1_2 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-1-1-2',
        user_id=12,
        reply=first1_1,
        depth=3,root=first1)




first2 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-2',
        user_id=3,
        depth=1,)




first3 = models.CommentRecord.objects.create(
        news_id=36,
        content='好-3',
        user_id=5,
        depth=1,)
