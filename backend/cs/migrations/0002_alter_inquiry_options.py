# Generated by Django 4.2.5 on 2024-04-09 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inquiry',
            options={'ordering': ['-created_on'], 'verbose_name': '문의&제휴 신청', 'verbose_name_plural': '문의&제휴 신청 목록'},
        ),
    ]
