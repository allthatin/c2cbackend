# Generated by Django 4.2.5 on 2024-03-20 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0028_alter_knowyourkidstest_uuid_alter_user_uservid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowyourkidstest',
            name='uuid',
            field=models.CharField(default='c7bb79c3-5666-4bbc-9924-fba500b5bd2b', max_length=255, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uservid',
            field=models.CharField(default='387aad2b-7aee-4216-8a2a-416479459c3b', max_length=36, verbose_name='USERVID'),
        ),
    ]
