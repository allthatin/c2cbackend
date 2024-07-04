from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Orders
from datetime import timedelta
from .tasks import cancel_unfulfilled_order, \
async_save_order_history, SaveOrdernoDueDate_updateBidStatus

CANCELLATION_DELAY = timedelta(hours=1).total_seconds()  

@receiver(post_save, sender=Orders)
def when_order_updated(sender, instance, created, **kwargs):

    if created:
        # 연결된 테이블 상태 변경
        # 주문번호 생성, 주문번호 입력기한 설정, 주문 상태 변경
        SaveOrdernoDueDate_updateBidStatus.apply_async(
            (instance.id,)
            )
        # 2일후 판매 취소 작업 예약
        cancel_unfulfilled_order.apply_async(
            (instance.id,), countdown=CANCELLATION_DELAY)

    elif not created and instance.changed():
        # 주문 히스토리 저장
        print("instance.changed()", instance.changed(), created)
        changes = mapping_changes(instance)
        changes_str = ", ".join(changes)
        async_save_order_history.apply_async(
            (instance.id, changes_str)
            )
        
def mapping_changes(instance):
    changes = []
    for field, old_value, new_value in instance.changed():
        if not field.startswith('_'):
            field_verbose_name = next((f.verbose_name for f in instance._meta.get_fields() if f.name == field), field)
            changes.append(f"{field_verbose_name}: {old_value} -> {new_value}")
    return changes