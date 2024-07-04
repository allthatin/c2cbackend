# Generated by Django 4.2.5 on 2024-04-11 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('article', '0021_alter_article_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='view',
            name='article',
        ),
        migrations.AddField(
            model_name='view',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='view',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]