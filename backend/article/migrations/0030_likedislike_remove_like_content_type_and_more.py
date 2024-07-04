# Generated by Django 4.2.5 on 2024-04-27 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('article', '0029_comment_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('action', models.CharField(choices=[('like', '좋아요'), ('dislike', '싫어요')], max_length=10, verbose_name='좋아요 여부')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '게시글 싫어요/좋아요',
                'verbose_name_plural': '게시글 싫어요/좋아요 목록',
                'ordering': ['created_on'],
                'unique_together': {('user', 'content_type', 'object_id')},
            },
        ),
        migrations.RemoveField(
            model_name='like',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='like',
            name='user',
        ),
        migrations.DeleteModel(
            name='DisLike',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]