# Generated by Django 4.2.5 on 2024-03-17 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_alter_user_options_alter_user_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_phoneverified',
            new_name='is_smsverified',
        ),
        migrations.AddField(
            model_name='user',
            name='is_thirdpartyconscent',
            field=models.BooleanField(default=False),
        ),
    ]