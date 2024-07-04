# Generated by Django 4.2.5 on 2024-06-29 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bids', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('card_type', models.CharField(blank=True, choices=[('마스터카드', '마스터카드'), ('비자', '비자')], max_length=255, null=True, verbose_name='카드종류')),
                ('card_company', models.CharField(blank=True, max_length=255, null=True, verbose_name='카드회사')),
                ('card_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='카드번호')),
                ('card_holder', models.CharField(blank=True, max_length=255, null=True, verbose_name='카드소유자')),
                ('card_expiration', models.CharField(blank=True, max_length=255, null=True, verbose_name='카드만료일')),
                ('card_cvc', models.CharField(blank=True, max_length=255, null=True, verbose_name='카드CVC')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_cards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '카드정보',
                'verbose_name_plural': '카드정보',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Logistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(blank=True, default=orders.models.generate_uuid, max_length=36, null=True, verbose_name='UUID')),
                ('delivery_price', models.IntegerField(default=0, verbose_name='배송비')),
                ('delivery_status', models.CharField(blank=True, max_length=255, null=True, verbose_name='배송상태')),
                ('delivery_company', models.CharField(blank=True, max_length=255, null=True, verbose_name='배송회사')),
                ('delivery_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='송장번호')),
            ],
            options={
                'verbose_name': '배송',
                'verbose_name_plural': '배송',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(blank=True, default=orders.models.generate_uuid, max_length=36, null=True, verbose_name='UUID')),
                ('orderno', models.CharField(blank=True, null=True, verbose_name='주문번호')),
                ('buy_fee', models.IntegerField(default=4, verbose_name='구매수수료')),
                ('buy_fee_discount', models.IntegerField(default=0, verbose_name='구매수수료할인')),
                ('sell_fee', models.IntegerField(default=4, verbose_name='판매수수료')),
                ('sell_fee_discount', models.IntegerField(default=0, verbose_name='판매수수료할인')),
                ('logisticno_input_due_date', models.DateTimeField(blank=True, null=True, verbose_name='송장번호 입력기한')),
                ('isfullfilled', models.BooleanField(default=False, verbose_name='거래 완료여부')),
                ('bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bid_orders', to='bids.bids')),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
                ('logistic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logistic_orders', to='orders.logistics')),
            ],
            options={
                'verbose_name': '주문',
                'verbose_name_plural': '주문',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('결제완료', '결제완료'), ('픽업중', '픽업중'), ('배송준비', '배송준비'), ('배송중', '배송중'), ('배송완료', '배송완료'), ('정산완료', '정산완료'), ('판매취소', '판매취소')], default='결제완료', max_length=255, verbose_name='주문상태')),
            ],
            options={
                'verbose_name': '주문 상태',
                'verbose_name_plural': '주문 상태',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='VirtualWireAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='은행명')),
                ('account_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='계좌번호')),
                ('account_holder', models.CharField(blank=True, max_length=255, null=True, verbose_name='예금주')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wire_transfers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '계좌이체',
                'verbose_name_plural': '계좌이체',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(blank=True, default=orders.models.generate_uuid, max_length=36, null=True, verbose_name='UUID')),
                ('score', models.IntegerField(default=0, verbose_name='별점')),
                ('content', models.TextField(blank=True, null=True, verbose_name='내용')),
                ('image', models.ImageField(blank=True, null=True, upload_to='review_images', verbose_name='이미지')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_reviews', to='orders.orders')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '리뷰',
                'verbose_name_plural': '리뷰',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(blank=True, default=orders.models.generate_uuid, max_length=36, null=True, verbose_name='UUID')),
                ('payment_method', models.CharField(choices=[('카드', '카드'), ('계좌이체', '계좌이체')], default='카드', max_length=255, verbose_name='결제수단')),
                ('payment_price', models.IntegerField(default=0, verbose_name='결제금액')),
                ('installment', models.CharField(blank=True, choices=[('일시불', '일시불'), ('무이자할부', '무이자할부'), ('일반할부', '일반할부')], max_length=255, null=True, verbose_name='할부')),
                ('installment_months', models.CharField(blank=True, choices=[('3개월', '3개월'), ('6개월', '6개월'), ('9개월', '9개월'), ('12개월', '12개월')], max_length=255, null=True, verbose_name='할부개월')),
                ('payment_3rd_party', models.CharField(blank=True, choices=[('토스', '토스'), ('카카오페이', '카카오페이'), ('네이버페이', '네이버페이'), ('페이코', '페이코'), ('이니시스', '이니시스')], max_length=255, null=True, verbose_name='결제사')),
                ('cardinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cardinfo_payments', to='orders.cardinfo')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_payments', to='orders.orders')),
                ('virtualwireinfo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wireinfo_payments', to='orders.virtualwireaccount')),
            ],
            options={
                'verbose_name': '결제',
                'verbose_name_plural': '결제',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_orders', to='orders.payments'),
        ),
        migrations.AddField(
            model_name='orders',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_orders', to='orders.reviews'),
        ),
        migrations.AddField(
            model_name='orders',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status_orders', to='orders.status'),
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('changes', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_history', to='orders.orders')),
            ],
            options={
                'verbose_name': '주문 히스토리',
                'verbose_name_plural': '주문 히스토리',
                'ordering': ['-created_on'],
            },
        ),
        migrations.AddField(
            model_name='logistics',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_logistics', to='orders.orders'),
        ),
    ]
