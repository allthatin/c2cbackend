# Generated by Django 4.2.5 on 2024-03-15 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_rename_is_staff_user_is_phoneverified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='연락처'),
        ),
    ]