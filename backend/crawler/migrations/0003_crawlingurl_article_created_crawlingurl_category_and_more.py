# Generated by Django 4.2.5 on 2024-06-20 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_alter_crawlingurl_stockdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawlingurl',
            name='article_created',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='sites',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='crawlingurl',
            name='viewno',
            field=models.IntegerField(default=0),
        ),
    ]
