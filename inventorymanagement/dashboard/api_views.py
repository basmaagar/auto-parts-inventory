from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Part, Order
from django.db.models import Sum

@login_required
def parts_data(request):
    parts = Part.objects.all()
    data = {
        'part_name_refs': [f"{part.name} ({part.reference})" for part in parts],
        'part_quantities': [part.quantityinstock for part in parts],
    }
    return JsonResponse(data)

@login_required
def orders_data(request):
    if request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    order_aggregates = orders.values('part__name').annotate(total_quantity=Sum('order_quantity')).order_by('part__name')
    data = {
        'order_product_names': [item['part__name'] for item in order_aggregates],
        'order_quantities': [item['total_quantity'] for item in order_aggregates],
    }
    return JsonResponse(data)
