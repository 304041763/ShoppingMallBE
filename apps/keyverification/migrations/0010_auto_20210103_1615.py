# Generated by Django 2.2 on 2021-01-03 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keyverification', '0009_auto_20210102_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentrecord',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roots', to='keyverification.CommentRecord', verbose_name='根评论'),
        ),
        migrations.AlterField(
            model_name='commentrecord',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replys', to='keyverification.CommentRecord', verbose_name='回复'),
        ),
    ]