# Generated by Django 2.2 on 2020-12-28 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyverification', '0003_auto_20201228_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='/static/portrait/', null=True, upload_to='user_directory_path', verbose_name='头像'),
        ),
    ]
