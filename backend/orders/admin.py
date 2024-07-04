from django.contrib import admin

from .models import Orders, Logistics, Reviews,\
    OrderHistory, Status, Payments, CardInfo, VirtualWireAccount

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)
    list_per_page = 20

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'buyer', 'status')
    list_filter = ('status',)
    search_fields = ('uuid', 'buyer__username')
    list_per_page = 20

@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'order', 'delivery_price', 'delivery_status', 'delivery_company', 'delivery_number')
    list_filter = ('delivery_status',)
    search_fields = ('uuid', 'order__uuid')
    list_per_page = 20

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'order', 'score', 'content')
    list_filter = ('score',)
    search_fields = ('uuid', 'order__uuid')
    list_per_page = 20

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'changes')
    search_fields = ('order__uuid', 'changes')
    list_per_page = 20


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('order','payment_price','payment_3rd_party')
    search_fields = ('payment_price',)
    list_per_page = 20

@admin.register(CardInfo)
class CardInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'card_holder')
    search_fields = ('card_holder',)
    list_per_page = 20

@admin.register(VirtualWireAccount)
class VirtualWireAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'account_holder', 'bank_name')
    search_fields = ('account_number',)
    list_per_page = 20
