# Generated by Django 4.2.5 on 2024-03-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(blank=True, choices=[('water', '물'), ('gold', '금속'), ('fire', '불'), ('wood', '나무'), ('earth', '흙'), ('cloud', '구름'), ('star', '별')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='tribe',
            field=models.CharField(blank=True, choices=[('fish', '물고기'), ('butterfly', '나비'), ('beetle', '풍뎅이'), ('owl', '부엉이'), ('tiger', '호랑이'), ('dolphin', '돌고래'), ('horse', '말'), ('wolf', '늑대')], max_length=10, null=True),
        ),
    ]