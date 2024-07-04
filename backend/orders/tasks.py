from .models import Orders, OrderHistory, Status
from bids.models import Bids
from config import celery_app
from datetime import timedelta
import re

@celery_app.task(bind=True)
def cancel_unfulfilled_order(_, order_id):
    try:
        order = Orders.objects.get(id=order_id)
        if order.status == '결제완료':
            order.status = '구매취소'
            order.save()
    except Orders.DoesNotExist:
        print("Order does not exist", order_id)

@celery_app.task(bind=True)
def async_save_order_history(_, order_id, changes):
    orderinstance = Orders.objects.get(id=order_id)
    OrderHistory.objects.create(order=orderinstance, changes=changes)
    

@celery_app.task(bind=True)
def SaveOrdernoDueDate_updateBidStatus(_, order_id):
    CANCELLATION_DELAY = timedelta(hours=1).total_seconds()  
    
    try:
        instance = Orders.objects.get(id=order_id)
        integercreatedon = re.sub('\D', '', str(instance.created_on))
        instance.orderno = int(str(integercreatedon) + str(instance.bid.id) + str(instance.buyer.id))

        format_duedate = (instance.created_on + timedelta(seconds=CANCELLATION_DELAY)).strftime("%Y-%m-%d %H:%M:%S")
        instance.logisticno_input_due_date = format_duedate
        instance.status = Status.objects.get(status="결제완료")
        instance.save()
        
    except Orders.DoesNotExist:
        print("Order does not exist")

    except Exception as e:
        if 'can only join an iterable' in e:
            # order내역 첫번째 생성시 오류 발생합니다 ( None이 있으므로)
            pass
        else:
            print(e)
            print("Error occurred")

    try:
        bidinstance = Bids.objects.get(id=instance.bid.id)
        bidinstance.is_sold = True
        bidinstance.save()
    except Bids.DoesNotExist:
        print("Bid does not exist")