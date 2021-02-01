from django.db import models
import uuid, os
from ShoppingMallBE.settings import MEDIA_URL, server_URL


def user_directory_path(filename):
    """修改路径名字"""
    # ext = filename.split('.')[-1]
    ext = 'png'
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return os.path.join(instance.user.id, "portrait", filename)
    return str(filename)


class UserInfo(models.Model):
    """
    用户
    """
    phone = models.CharField(verbose_name='手机号', max_length=32, )
    nickname = models.CharField(verbose_name="昵称", max_length=32, )
    # user_id = models.CharField(verbose_name="用户ID", max_length=32)
    avatar = models.ImageField(verbose_name="头像", upload_to="user_directory_path/%Y%m%d/", null=True)

    token = models.CharField(verbose_name="用户Token", max_length=64, )

    def get_avatar_url(self):  # 拼接返回路径
        return server_URL + MEDIA_URL + str(self.avatar)

    class Meta:
        db_table = 'UserInfo'

    def __str__(self):
        return self.nickname


class Topic(models.Model):
    """
    话题
    """
    title = models.CharField(verbose_name="话题", max_length=32)
    count = models.PositiveIntegerField(verbose_name="关注度", default=0)

    def __str__(self):
        return self.title


class News(models.Model):
    """
    动态
    """
    cover = models.CharField(verbose_name="封面", max_length=128)
    title = models.CharField(verbose_name="标题", max_length=64, null=True, blank=True)
    content = models.CharField(verbose_name="内容", max_length=255)
    topic = models.ForeignKey(to='Topic', verbose_name="话题", null=True, blank=True, related_name='topic',on_delete=models.CASCADE)
    address = models.CharField(verbose_name="位置", max_length=128, null=True, blank=True)
    user = models.ForeignKey(verbose_name="发布者", to='UserInfo', related_name='user', on_delete=models.CASCADE,
                             null=True, blank=True)
    favor_count = models.PositiveIntegerField(verbose_name="赞数", default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览数", default=0)
    comment_count = models.PositiveIntegerField(verbose_name="评论数", default=0)
    create_date = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    # activation_state = (('true', 'false'),('true', 'false'))
    state = models.BooleanField(verbose_name="激活状态", default=False, null=True, blank=True)


class NewsDetail(models.Model):
    """
    动态详细
    """
    # key = models.CharField(verbose_name="腾讯对象中的文件名", max_length=128, help_text="用于以后再腾讯对象存储中删除")
    key = models.CharField(verbose_name="腾讯对象中的文件名", max_length=128)
    cos_path = models.CharField(verbose_name="腾讯对象存储中图片路径", max_length=128)
    news = models.ForeignKey(verbose_name="动态", to="News", on_delete=models.CASCADE, related_name="news")
    # related_name反向查询使用


class ViewerRecord(models.Model):
    """浏览记录"""
    news = models.ForeignKey(verbose_name="动态", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to='UserInfo', on_delete=models.CASCADE, null=True, blank=True)


class NewsFavorRecord(models.Model):
    """动态记录"""
    news = models.ForeignKey(verbose_name="动态", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="点赞用户", to='UserInfo', on_delete=models.CASCADE, null=True, blank=True)


class CommentRecord(models.Model):
    news = models.ForeignKey(verbose_name="动态", to="News", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=255)
    user = models.ForeignKey(verbose_name="评论者", to="UserInfo", on_delete=models.CASCADE, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)

    reply = models.ForeignKey(verbose_name="回复", to="self", null=True, blank=True, on_delete=models.CASCADE,
                              related_name='replys')
    depth = models.PositiveIntegerField(verbose_name="评论层级", default=1)
    root = models.ForeignKey(verbose_name="根评论", to="self", null=True, blank=True, on_delete=models.CASCADE,
                             related_name='roots')

    favor_count = models.PositiveIntegerField(verbose_name="赞数", default=0)


class CommentFavorRecord(models.Model):
    comment = models.ForeignKey(verbose_name="动态", to="CommentRecord", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='点赞用户', to='UserInfo', on_delete=models.CASCADE, null=True, blank=True)
