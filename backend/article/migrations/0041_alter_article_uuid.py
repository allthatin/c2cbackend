# Generated by Django 4.2.5 on 2024-05-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0040_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='uuid',
            field=models.TextField(blank=True, null=True, verbose_name='UUID'),
        ),
    ]
