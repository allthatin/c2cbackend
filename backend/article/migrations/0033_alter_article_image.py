# Generated by Django 4.2.5 on 2024-04-29 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0032_remove_articleimage_article_remove_article_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ManyToManyField(blank=True, related_name='image_article', to='article.articleimage'),
        ),
    ]
