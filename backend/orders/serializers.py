from rest_framework import serializers
from . import models


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'

class CardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CardInfo
        fields = ['card_type', 'card_company', 'card_number', 'card_holder']

class PaymentSerializer(serializers.ModelSerializer):
    virtualwireinfo = serializers.SerializerMethodField()
    cardinfo = serializers.SerializerMethodField()
    class Meta:
        model = models.Payments
        fields = ['payment_method', 'payment_price', 'payment_3rd_party', 'installment'
                  , 'installment_months', 'virtualwireinfo', 'cardinfo']

class OrderListSerializer(serializers.ModelSerializer):
    
    productimage = serializers.SerializerMethodField()
    # buy_total_price = serializers.SerializerMethodField()
    transaction_date = serializers.SerializerMethodField()
    updated_on_date = serializers.SerializerMethodField()
    # delivery_number = serializers.SerializerMethodField()
    status = serializers.StringRelatedField()
    productprice = serializers.SerializerMethodField()
    designer = serializers.SerializerMethodField()

    class Meta:
        model = models.Orders
        fields = ['orderno', 'productimage', 'transaction_date',\
                   'status', 'updated_on_date','productprice', 'designer']
    
    def get_transaction_date(self, obj):
        return obj.transaction_date
    
    def get_productimage(self, obj):
        images = obj.bid.product.thumbnail.url
        return images
    
    def get_updated_on_date(self, obj):
        return obj.updated_on_date
    
    def get_productprice(self, obj):
        return f'₩{obj.bid.price:,}'
    
    def get_designer(self, obj):
        return obj.get_designer

class OrderListSellerSerializer(OrderListSerializer):
    bid_total_price = serializers.SerializerMethodField()
    logistic = serializers.StringRelatedField()

    class Meta(OrderListSerializer.Meta):
        # ['orderno', 'productimage', 
        #  'transaction_date', 'status', 'updated_on_date']
        fields = OrderListSerializer.Meta.fields + \
        ['bid_total_price', 'logistic', 'bid']

    def get_bid_total_price(self, obj):
        return f'₩{obj.bid.price:,}'

class OrderListBuyerSerializer(OrderListSerializer):
    buy_total_price = serializers.SerializerMethodField()
    total_delivery_info = serializers.SerializerMethodField()
    delivery_price = serializers.SerializerMethodField()
    logistic = serializers.StringRelatedField()
    
    class Meta(OrderListSerializer.Meta):
        # ['orderno', 'productimage', 
        #  'transaction_date', 'status', 'updated_on_date']
        fields = OrderListSerializer.Meta.fields + \
        ['buy_total_price', 'delivery_price',
         'total_delivery_info', 'logistic']
        
    
    
    def get_buy_total_price(self, obj):
        return f'₩{obj.buy_total_price:,}'
    
    def get_delivery_price(self, obj):
        return f'₩{obj.logistic.delivery_price:,}'
    
    def get_total_delivery_info(self, obj):
        return f'{obj.delivery_company} {obj.delivery_number}'
    
class OrderDetailSerializer(OrderListSerializer):
    productName = serializers.SerializerMethodField()
    class Meta(OrderListSerializer.Meta):
        # ['orderno', 'delivery_number',  'productimage', 
        #  'buy_total_price', 'transaction_date', 'status', 'updated_on_date']
        fields = OrderListSerializer.Meta.fields + \
        ['productName']

    def get_productName(self, obj):
        return obj.bid.product.name
    
class OrderDetailSellerSerializer(OrderDetailSerializer):
    fee_total = serializers.SerializerMethodField()
    fee = serializers.SerializerMethodField()
    fee_discount = serializers.SerializerMethodField()
    logisticno_input_due_date = serializers.SerializerMethodField()
    sell_total_price = serializers.SerializerMethodField()

    class Meta(OrderDetailSerializer.Meta):
        # ['orderno', 'productimage', 
        #  'transaction_date', 'status', 'updated_on_date']
        # ['productName']
        fields = OrderDetailSerializer.Meta.fields + \
        ['fee', 'fee_discount', 'fee_total',
         'sell_total_price', 'logisticno_input_due_date']
    
    def get_fee_total(self, obj):
        total = obj.sell_fee - obj.sell_fee_discount
        return f'{total:,}%'
    
    def get_fee(self, obj):
        return f'{obj.sell_fee:,}%'
    
    def get_fee_discount(self, obj):
        return f'{obj.sell_fee_discount:,}%'
    
    def get_logisticno_input_due_date(self, obj):
        return obj.get_logisticno_input_due_date
    
    def get_sell_total_price(self, obj):
        return f'₩{obj.sell_total_price:,}'
    
class OrderDetailBuyerSerializer(OrderDetailSerializer):
    
    buyer = serializers.StringRelatedField()
    payment = serializers.StringRelatedField()
    delivery_number = serializers.StringRelatedField()
    delivery_price = serializers.SerializerMethodField()
    buy_total_price = serializers.SerializerMethodField()
    fee_discount = serializers.SerializerMethodField()
    fee = serializers.SerializerMethodField()
    fee_total = serializers.SerializerMethodField()

    class Meta(OrderDetailSerializer.Meta):
        # ['orderno', 'productimage', 
        #  'transaction_date', 'status', 'updated_on_date']
        # ['productName']
        fields = OrderDetailSerializer.Meta.fields + \
        ['buyer', 'fee', 'fee_discount', 'fee_total', 'delivery_price',
         'buy_total_price', 'payment', 
         'delivery_number']

    def get_buy_total_price(self, obj):
        return f'₩{obj.buy_total_price:,}'
    
    def get_fee_discount(self, obj):
        return f'{obj.buy_fee_discount:,}%'
    
    def get_fee(self, obj):
        return f'{obj.buy_fee:,}%'
    
    def get_fee_total(self, obj):
        total = obj.buy_fee - obj.buy_fee_discount
        return f'{total:,}%'

    def get_delivery_price(self, obj):
        return f'₩{obj.logistic.delivery_price:,}' if obj.logistic else ''
    
class LogisticsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Logistics
        fields = '__all__'

class LogisticsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Logistics
        fields = '__all__'

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reviews
        fields = '__all__'