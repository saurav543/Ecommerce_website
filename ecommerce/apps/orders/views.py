from django.shortcuts import render
from django.http.response import JsonResponse
from ecommerce.apps.basket.basket import Basket
# from ecommerce.apps.inventory import Product
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem


# Create your views here.
app_name = 'orders'


def add(request):
    basket = Basket(request)
    if request.method == "POST":
        user_id = request.user.id
        order_key = request.POST['order_key']
        obj = basket.get_total_price()
        baskettotal = obj
        # check order is exist
        # print(baskettotal)
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id = user_id, full_name='name', address1='add1', address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(order_id = order_id, product=item['product'], price=item['price'], quantity=item['quantity'])
        response = JsonResponse({'success': 'success'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders

@login_required
def orders(request):
    user_id = request.user.id
    order = Order.objects.filter(user=user_id, billing_status=True)
    # print(order)
    order_list = []
    for od in order:
        order_item = OrderItem.objects.filter(order=od)
        order_list.append(order_item)
        
    print(order,order_list)
    return render(request,'account/dashboard/order_list.html',{'order_item':order_list})
    
