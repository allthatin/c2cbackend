# Generated by Django 4.2.5 on 2024-06-26 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0070_remove_team_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='led_team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='user_team', to='member.team'),
        ),
    ]
