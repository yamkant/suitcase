from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_results.models import TaskResult
import requests

# NOTE: Signal after celery work -> to wsgi server 
@receiver(post_save, sender=TaskResult)
def process_celery_task_result(sender, instance, **kwargs):
    if instance.status == 'SUCCESS':
        requests.get(f'http://my_app:8000/alarms/tasks/{instance.id}/')

# NOTE: KEEP CODE
# @receiver(pre_save, sender=Product)
# def on_change(sender, instance: Product, **kwargs):
#     if instance.id is None: # new object will be created
#         pass # write your code here
#     else:
#         previous = Product.objects.get(id=instance.id)
#         if previous.is_active != instance.is_active: # field will be updated
#             send_event('testchannel', 'message', {"msg": "AFTER REQUEST!!!!!!!!!!"})
#             print("Status Changed!!!!!!!")
#             pass  # write your code here