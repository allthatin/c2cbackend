# Generated by Django 4.2.5 on 2024-04-12 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0058_remove_knowyourkidstest_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash_phone',
            field=models.TextField(blank=True, null=True, verbose_name='b연락처'),
        ),
        migrations.AlterField(
            model_name='user',
            name='raw_phone',
            field=models.TextField(blank=True, null=True, verbose_name='연락처'),
        ),
    ]
