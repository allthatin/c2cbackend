# Generated by Django 4.2.5 on 2024-05-08 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_alter_userevent_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='event_type',
            field=models.CharField(choices=[('prepandready', 'Page Load'), ('exterminate', 'Page Close'), ('fiwjfwu9', 'Page OutFocus'), ('wolfwolf', 'Button Click'), ('fufu', 'Form Submit'), ('grr', 'Scroll')], max_length=50, verbose_name='이벤트 분류'),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='session_key',
            field=models.CharField(max_length=40),
        ),
    ]