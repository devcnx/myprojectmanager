from django.http import JsonResponse
from work_orders.models import WorkOrder


def get_next_trip_number(request, work_order_id):
    work_order = WorkOrder.objects.get(pk=work_order_id)
    next_trip_number = work_order.get_next_trip_number()
    return JsonResponse({'next_trip_number': next_trip_number})
