# Generated by Django 4.2.5 on 2024-05-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0042_alter_article_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.TextField(blank=True, null=True, verbose_name='UUID'),
        ),
    ]
