# Generated by Django 4.2.5 on 2024-05-21 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0009_alter_userevent_event_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userevent',
            options={'ordering': ['-timestamp']},
        ),
    ]
