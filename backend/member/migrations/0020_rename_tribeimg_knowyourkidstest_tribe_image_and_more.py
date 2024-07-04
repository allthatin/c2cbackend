# Generated by Django 4.2.5 on 2024-03-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0019_remove_user_tribe_remove_user_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knowyourkidstest',
            old_name='tribeimg',
            new_name='tribe_image',
        ),
        migrations.RemoveField(
            model_name='user',
            name='personalitychips',
        ),
        migrations.AlterField(
            model_name='knowyourkidstest',
            name='uuid',
            field=models.CharField(default='2248c0af-8233-44ee-90aa-76ab6a5420d2', max_length=255, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uservid',
            field=models.CharField(default='e0411657-6e8f-4af0-a265-0da25af1db50', max_length=36, verbose_name='USERVID'),
        ),
    ]