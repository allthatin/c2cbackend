# Generated by Django 4.2.5 on 2024-06-18 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0003_inquiry_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inquiry',
            name='name',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='phone',
        ),
    ]
