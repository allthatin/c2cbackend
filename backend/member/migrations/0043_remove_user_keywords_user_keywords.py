# Generated by Django 4.2.5 on 2024-04-05 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0042_user_raw_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='keywords',
        ),
        migrations.AddField(
            model_name='user',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
