# Generated by Django 4.2.5 on 2024-03-21 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_alter_article_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.CharField(default='c221d7d3', max_length=255, verbose_name='UUID'),
        ),
    ]
