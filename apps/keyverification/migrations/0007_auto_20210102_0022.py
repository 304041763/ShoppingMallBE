# Generated by Django 2.2 on 2021-01-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyverification', '0006_auto_20210102_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(null=True, upload_to='user_directory_path/%Y/%m/%d/', verbose_name='头像'),
        ),
    ]