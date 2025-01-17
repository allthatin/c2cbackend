# Generated by Django 4.2.5 on 2024-03-23 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0037_alter_user_hash_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='태그명')),
            ],
            options={
                'verbose_name': '태그',
                'verbose_name_plural': '태그 목록',
                'ordering': ['created_on'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='introduction',
            field=models.TextField(blank=True, null=True, verbose_name='소개글'),
        ),
        migrations.AddField(
            model_name='user',
            name='keywords',
            field=models.ManyToManyField(blank=True, related_name='keyword_user', to='member.keyword'),
        ),
    ]
