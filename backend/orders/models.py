from django.db import models
from utils.datetime_model import TimeStampModel
import math

def generate_uuid():
    import uuid
    return str(uuid.uuid4())

class Status(TimeStampModel):
    """주문 히스토리"""
    STATUS_PROCESS = (
        ("결제완료", "결제완료"),
        ("픽업중", "픽업중"),
        ("배송준비", "배송준비"),
        ("배송중", "배송중"),
        ("배송완료", "배송완료"),
        ("정산완료", "정산완료"),
        ("판매취소", "판매취소"),
    )
    status = models.CharField("주문상태", max_length=255, choices=STATUS_PROCESS, default="결제완료")
    
    class Meta:
        verbose_name = "주문 상태"
        verbose_name_plural = "주문 상태"
        ordering = ["-created_on"]
    
    def __str__(self):
        return f'{str(self.status)}'

# Create your models here.
class Orders(TimeStampModel):
    """주문"""
    uuid = models.CharField("UUID", max_length=36, null=True, blank=True, default=generate_uuid)
    orderno = models.CharField("주문번호", null=True, blank=True)
    # orderno는 Signal로 생성
 
    buyer = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="user_orders", null=True, blank=True)
    bid = models.ForeignKey("bids.Bids", on_delete=models.CASCADE, related_name="bid_orders", null=True, blank=True)

    buy_fee = models.IntegerField("구매수수료", default=4)
    buy_fee_discount = models.IntegerField("구매수수료할인", default=0)
    sell_fee = models.IntegerField("판매수수료", default=4)
    sell_fee_discount = models.IntegerField("판매수수료할인", default=0)

    logistic = models.ForeignKey("Logistics", on_delete=models.CASCADE, related_name="logistic_orders", null=True, blank=True)
    logisticno_input_due_date = models.DateTimeField("송장번호 입력기한", null=True, blank=True)
    isfullfilled = models.BooleanField("거래 완료여부", default=False)
    # 판매자가 2일 이내에 송장 번호를 입력하면 True

    status = models.ForeignKey("Status", on_delete=models.CASCADE, related_name="status_orders", null=True, blank=True)
    review = models.ForeignKey("Reviews", on_delete=models.CASCADE, related_name="review_orders", null=True, blank=True)
    payment = models.ForeignKey("Payments", on_delete=models.CASCADE, related_name="payment_orders", null=True, blank=True)


    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문"
        ordering = ["-created_on"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.__original_state = self.__dict__.copy()
        self.__original_state = self._get_current_state()
    
    def _get_current_state(self):
        return {f.name: f.value_from_object(self) for f in self._meta.fields}

    def has_changed(self):
        return any(self.__original_state[field] != value and field != 'updated_on'
                    for field, value in self._get_current_state().items())

    def changed(self):
        current_state = self._get_current_state()
        return [(field, self.__original_state[field], current_state[field]) 
                for field in self.__original_state 
                if self.__original_state[field] != current_state[field] and field != 'updated_on']
    
    @property
    def is_newly_created(self):
        return self.__original_state['id'] is None

    def save(self, *args, **kwargs):
        if self.bid.user == self.buyer and self.is_newly_created:
            response = ValueError("구매자와 판매자가 같습니다.")
            try:
                # order bid status 정합성 안맞을 경우 rollback
                self.delete()
            except:
                pass
            return response
        if self.bid.is_sold == True and self.is_newly_created:
            response = ValueError("이미 판매된 상품입니다.")
            try:
                # order bid status 정합성 안맞을 경우 rollback
                self.delete()
            except:
                pass
            return response
        super(Orders, self).save(*args, **kwargs)

    def __str__(self):
        return f'#주문-{str(self.uuid)}'    
    
    @property
    def buy_total_price(self):
        bidPrice = self.bid.price
        final_fee = (100 + self.buy_fee - self.buy_fee_discount) / 100
        delivery_price = self.logistic.delivery_price if self.logistic else 0
        totalprice = bidPrice * final_fee + delivery_price
        return int(math.floor(totalprice / 1000) * 1000)
    
    @property
    def sell_total_price(self):
        bidPrice = self.bid.price
        totalprice = bidPrice * (100 - self.sell_fee + self.sell_fee_discount) / 100
        return int(math.floor(totalprice / 1000) * 1000)
    
    @property
    def transaction_date(self):
        return self.created_on.strftime("%m월 %d일 %H:%M")
    
    @property
    def updated_on_date(self):
        return self.updated_on.strftime("%m월 %d ")
    
    def get_korean_format_price(self):
        return f"₩{(self.price):,}"
    
    @property
    def get_logisticno_input_due_date(self):
        return self.logisticno_input_due_date.strftime("%m월 %d일 %H:%M")
    
    @property
    def get_productprice(self):
        return self.bid.price
    
    @property
    def get_designer(self):
        return self.bid.product.designer.name
    
  
class OrderHistory(TimeStampModel):
    """주문 히스토리"""
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, related_name="order_history", null=True, blank=True)
    changes = models.TextField(null=True, blank=True)
    

    class Meta:
        verbose_name = "주문 히스토리"
        verbose_name_plural = "주문 히스토리"
        ordering = ["-created_on"]

    def __str__(self):
        return f'#{str(self.order)}-{str(self.changes)}'
    
class Logistics(TimeStampModel):
    """배송"""
    uuid = models.CharField("UUID", default=generate_uuid, max_length=36, null=True, blank=True)
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, related_name="order_logistics", null=True, blank=True)
    
    delivery_price = models.IntegerField("배송비", default=0)
    delivery_status = models.CharField("배송상태", max_length=255, null=True, blank=True)
    delivery_company = models.CharField("배송회사", max_length=255, null=True, blank=True)
    delivery_number = models.CharField("송장번호", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "배송"
        verbose_name_plural = "배송"
        ordering = ["-created_on"]

    def __str__(self):
        return f'{self.delivery_company} {str(self.delivery_number)}'
    
class Reviews(TimeStampModel):
    """리뷰"""
    uuid = models.CharField("UUID", default=generate_uuid, max_length=36, null=True, blank=True)
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, related_name="order_reviews", null=True, blank=True)
    user = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="user_reviews", null=True, blank=True)
    
    score = models.IntegerField("별점", default=0)
    content = models.TextField("내용", null=True, blank=True)
    image = models.ImageField("이미지", upload_to="review_images", null=True, blank=True)
    
    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰"
        ordering = ["-created_on"]

    def __str__(self):
        return f'#{str(self.uuid)}'
    

class Payments(TimeStampModel):
    """결제"""
    uuid = models.CharField("UUID", default=generate_uuid, max_length=36, null=True, blank=True)
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, related_name="order_payments", null=True, blank=True)
    
    PAYMENT_METHODS = (
        ("카드", "카드"),
        ("계좌이체", "계좌이체"),
    )
    payment_method = models.CharField("결제수단", max_length=255, choices=PAYMENT_METHODS, default="카드")
    payment_price = models.IntegerField("결제금액", default=0)
    
    INSTALLMENT_CHOICES = (
        ("일시불", "일시불"),
        ("무이자할부", "무이자할부"),
        ("일반할부", "일반할부"),
    )
    installment = models.CharField("할부", max_length=255, choices=INSTALLMENT_CHOICES, null=True, blank=True)

    INSTALLMENT_MONTHS = (
        ("3개월", "3개월"),
        ("6개월", "6개월"),
        ("9개월", "9개월"),
        ("12개월", "12개월"),
    )
    installment_months = models.CharField("할부개월", max_length=255, choices=INSTALLMENT_MONTHS, null=True, blank=True)


    PAYMENT_3RD_PARTY = (
        ("토스", "토스"),
        ("카카오페이", "카카오페이"),
        ("네이버페이", "네이버페이"),
        ("페이코", "페이코"),
        ("이니시스", "이니시스"),
    )

    payment_3rd_party = models.CharField("결제사", max_length=255, choices=PAYMENT_3RD_PARTY, null=True, blank=True)
    virtualwireinfo = models.ForeignKey("VirtualWireAccount", on_delete=models.CASCADE, related_name="wireinfo_payments", null=True, blank=True)
    cardinfo = models.ForeignKey("CardInfo", on_delete=models.CASCADE, related_name="cardinfo_payments", null=True, blank=True)

    class Meta:
        verbose_name = "결제"
        verbose_name_plural = "결제"
        ordering = ["-created_on"]

    def __str__(self):
        return f'{self.payment_3rd_party} / {str(self.installment)}'
    
class CardInfo(TimeStampModel):
    """카드정보"""
    user = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="user_cards", null=True, blank=True)
    CARD_TYPE_CHOICE = (
        ("마스터카드", "마스터카드"),
        ("비자", "비자")
    )

    card_type = models.CharField("카드종류", max_length=255, choices=CARD_TYPE_CHOICE, null=True, blank=True)
    card_company = models.CharField("카드회사", max_length=255, null=True, blank=True)
    card_number = models.CharField("카드번호", max_length=255, null=True, blank=True)
    card_holder = models.CharField("카드소유자", max_length=255, null=True, blank=True)
    card_expiration = models.CharField("카드만료일", max_length=255, null=True, blank=True)
    card_cvc = models.CharField("카드CVC", max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = "카드정보"
        verbose_name_plural = "카드정보"
        ordering = ["-created_on"]
    
    def __str__(self):
        return f'#{str(self.card_company)}'
    
class VirtualWireAccount(TimeStampModel):
    """가상계좌"""
    user = models.ForeignKey("member.User", on_delete=models.CASCADE, related_name="user_wire_transfers", null=True, blank=True)
    bank_name = models.CharField("은행명", max_length=255, null=True, blank=True)
    account_number = models.CharField("계좌번호", max_length=255, null=True, blank=True)
    account_holder = models.CharField("예금주", max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name = "계좌이체"
        verbose_name_plural = "계좌이체"
        ordering = ["-created_on"]

    def __str__(self):
        return f'#{str(self.user)}'