# Generated by Django 4.2.5 on 2024-04-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0024_view_visit_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='view',
            name='referrer_url',
        ),
        migrations.AddField(
            model_name='view',
            name='referer_url',
            field=models.URLField(blank=True, null=True, verbose_name='참조 URL'),
        ),
        migrations.AddField(
            model_name='view',
            name='ua_platform',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='플랫폼'),
        ),
    ]
