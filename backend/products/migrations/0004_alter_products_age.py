# Generated by Django 4.2.5 on 2024-06-29 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_unique_together_alter_products_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='세대'),
        ),
    ]
