import os, sys, django

# 调用项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
# 往DJANGO_SETTINGS_MODULE环境变量中
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ShoppingMallBE.settings")
django.setup()

from apps.keyverification import models
# res = models.News.objects.all().order_by('-id')
#
# print(res.query)
for i in range(37, 40):
    news_object = models.News.objects.create(
        title="微信小程序版博客-用户中心",
        cover="https://htyper-1255622648.cos.ap-nanjing.myqcloud.com/UploadPictures/1608262777db84i8gctk.png",
        content="截至目前，北京市共有中风险地区3个，为朝阳区汉庭酒店大山子店(包括底商)、顺义区南法信镇西杜兰村、\
            顺义区高丽营镇张喜庄村。北京市其它地区均为低风险地区。还有{0}天放假".format(i),
        topic_id=1,
        user_id=1
    )

    models.NewsDetail.objects.create(
        key="1608262777vru520756i.png",
        cos_path="https://htyper-1255622648.cos.ap-nanjing.myqcloud.com/UploadPictures/1608262777vru520756i.png",
        news=news_object
    )

    models.NewsDetail.objects.create(
        key="1608262898zf9kis2245.png",
        cos_path="https://htyper-1255622648.cos.ap-nanjing.myqcloud.com/UploadPictures/1608262898zf9kis2245.png",
        news=news_object
    )
