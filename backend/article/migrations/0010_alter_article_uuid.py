# Generated by Django 4.2.5 on 2024-03-21 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_alter_article_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.CharField(default='070d4ca3', max_length=255, verbose_name='UUID'),
        ),
    ]