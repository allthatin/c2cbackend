# Generated by Django 4.2.5 on 2024-04-09 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0056_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['date_joined'], 'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
    ]
