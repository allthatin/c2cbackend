# Generated by Django 4.2.5 on 2024-03-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0026_alter_knowyourkidstest_uuid_alter_user_uservid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knowyourkidstest',
            name='uuid',
            field=models.CharField(default='2f27c001-83ff-4c12-af01-ece2fdd48134', max_length=255, verbose_name='UUID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uservid',
            field=models.CharField(default='da8e9b27-de8e-4a2e-894a-8c91f8504e5f', max_length=36, verbose_name='USERVID'),
        ),
    ]