# Generated by Django 4.2.5 on 2024-05-06 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0064_remove_team_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assets/team', verbose_name='팀 이미지'),
        ),
    ]
