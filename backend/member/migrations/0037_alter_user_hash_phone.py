# Generated by Django 4.2.5 on 2024-03-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0036_alter_user_unique_together_user_hash_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='hash_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='b연락처'),
        ),
    ]
