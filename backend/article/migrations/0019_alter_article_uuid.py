# Generated by Django 4.2.5 on 2024-03-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_alter_article_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='UUID'),
        ),
    ]