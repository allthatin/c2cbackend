# Generated by Django 4.2.5 on 2024-04-11 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('article', '0022_remove_view_article_view_content_type_view_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='활성화 여부'),
        ),
        migrations.AddField(
            model_name='view',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP 주소'),
        ),
        migrations.AddField(
            model_name='view',
            name='referrer_url',
            field=models.URLField(blank=True, null=True, verbose_name='참조 URL'),
        ),
        migrations.AddField(
            model_name='view',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='세션 키'),
        ),
        migrations.AddField(
            model_name='view',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='사용자 에이전트'),
        ),
        migrations.AlterField(
            model_name='view',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='view',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
