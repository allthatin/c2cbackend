# Generated by Django 4.2.5 on 2024-04-12 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0059_alter_user_hash_phone_alter_user_raw_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='invitecode',
        ),
        migrations.AddField(
            model_name='user',
            name='invitationcode',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='초대코드'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='회원가입 완료여부'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='어드민'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_privacyconsent',
            field=models.BooleanField(default=False, verbose_name='개인정보 수집 및 이용 동의'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_smsverified',
            field=models.BooleanField(default=False, verbose_name='휴대폰 인증'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='스태프'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_thirdpartyconsent',
            field=models.BooleanField(default=False, verbose_name='마케팅 목적의 개인정보 수집 및 이용 동의'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_thirdpartyconsent2',
            field=models.BooleanField(default=False, verbose_name='광고성 정보 수집 동의'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='이름'),
        ),
    ]
