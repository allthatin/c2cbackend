# Generated by Django 4.2.5 on 2024-03-20 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.CharField(default='bb58d7ec', max_length=255, verbose_name='UUID'),
        ),
    ]
