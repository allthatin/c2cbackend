# Generated by Django 4.2.5 on 2024-03-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0030_alter_knowyourkidstest_uuid_alter_user_uservid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='knowyourkidstest',
            name='tribe_image',
        ),
        migrations.AlterField(
            model_name='knowyourkidstest',
            name='uuid',
            field=models.CharField(default='5fc7417e-6718-4f8a-9e35-7e565f040106', max_length=255, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uservid',
            field=models.CharField(default='f00848e1-99ae-4afa-903f-0d0aa6af7071', max_length=36, verbose_name='USERVID'),
        ),
    ]