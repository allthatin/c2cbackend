# Generated by Django 4.2.5 on 2024-04-28 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0030_likedislike_remove_like_content_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_on'], 'verbose_name': '댓글', 'verbose_name_plural': '댓글 목록'},
        ),
        migrations.AlterUniqueTogether(
            name='likedislike',
            unique_together=set(),
        ),
    ]