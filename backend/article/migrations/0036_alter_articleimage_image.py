# Generated by Django 4.2.5 on 2024-04-29 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0035_alter_articleimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='assets', verbose_name='이미지'),
        ),
    ]