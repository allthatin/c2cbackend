# Generated by Django 4.2.5 on 2024-03-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0014_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='7e8abf38-f005-4a55-9c32-ad40f9752e57', max_length=36, verbose_name='UUID'),
        ),
    ]
