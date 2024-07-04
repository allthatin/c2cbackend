# Generated by Django 4.2.5 on 2024-07-01 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_manufacturer_delete_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='manufacturerfk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufacturer_products', to='products.manufacturer'),
        ),
    ]
