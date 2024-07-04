# Generated by Django 4.2.5 on 2024-05-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_alter_usersession_session_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='event_type',
            field=models.CharField(choices=[('prepandready', '페이지 로드'), ('exterminate', '페이지 닫기'), ('fiwjfwu9', '페이지 이탈'), ('wolfwolf', '클릭'), ('fufu', '폼 제출'), ('grr', '스크롤')], max_length=50, verbose_name='이벤트 분류'),
        ),
    ]
