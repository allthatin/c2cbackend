# Generated by Django 4.2.5 on 2024-03-20 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_comment_article_alter_article_uuid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.CharField(default='c772864c', max_length=255, verbose_name='UUID'),
        ),
    ]
