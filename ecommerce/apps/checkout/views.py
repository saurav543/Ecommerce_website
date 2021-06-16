from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DeliveryOptions
from django.http import HttpResponseRedirect , JsonResponse
from ecommerce.apps.basket.basket import Basket
from ecommerce.apps.account.models import Address
from django.http.response import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from ecommerce.apps.orders.views import payment_confirmation
import stripe
import json
import os
# Create your views here.

@login_required
def deliverychoices(request):
   deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
   return render(request,"checkout/delivery_choices.html",{'deliveryoptions':deliveryoptions})

@login_required
def basket_update_delivery(request):
   basket = Basket(request)
   if request.POST.get('action') == 'post':
      delivery_option = int(request.POST.get("deliveryoption")) 
      delivery_type = DeliveryOptions.objects.get(id=delivery_option)
      update_total_price = basket.basket_update_delivery(delivery_type.delivery_price)
      session = request.session
      if "purchase" not in request.session:
         session['purchase']={ 
                              "delivery_id":delivery_type.id }
      else:
         session['purchase']['delivery_id']=delivery_type.id
         session.modified = True   
      response = JsonResponse({"total": update_total_price,"delivery_price":delivery_type.delivery_price})
      return response
   return render(request,'checkout/delivery_choices.html')
   

@login_required
def delivery_address(request):
   session = request.session
   if 'purchase' not in request.session:
      messages.success(request,'Select delivery one of the delivery option.')
      return HttpResponseRedirect(request.META['HTTP_REFERER'])
   address = Address.objects.filter(customer=request.user).order_by("-default")
   if "address" not in request.session:
       session['address']={'address_id':str(address[0].id)}
   else:
      session['address']['address_id']=str(address[0].id)
      session.modified = True
   return render(request,'checkout/delivery_address.html',{'addresses':address})







 
@login_required
def payment_selection(request):
   if 'address' not in request.session:
      messages.success(request,'Please select address option')
      return HttpResponseRedirect(request.META['HTTP_REFERER'])
   basket = Basket(request)
   total = basket.get_total_price()
   price = int(total)
   print(total)
   stripe.api_key = settings.STRIPE_SECRET_KEY
   intent = stripe.PaymentIntent.create(
      description='Software development services',
      shipping={
         'name': 'Jenny Rosen',
         'address': {
               'line1': '510 Townsend St',
               'postal_code': '98140',
               'city': 'San Francisco',
               'state': 'CA',
               'country': 'US',
         },
      },
      amount=price,
      currency='gbp',
      metadata={'userid': request.user.id}
   )
    
   return render(request, 'checkout/payment_selection.html', {'client_secret': intent.client_secret, 'STRIPE_PUBLISHABLE_KEY': os.environ.get('STRIPE_PUBLISHABLE_KEY')})

@csrf_exempt
def stripe_webhook(request):
   payload = request.body
   event = None
   try:
      event = stripe.Event.construct_from(
         json.loads(payload), stripe.api_key
      )
      print(event.type)
   except ValueError as e:
      return HttpResponse(status=400)
   if event.type == 'payment_intent.succeeded':
      # print(event.data.object.client_secret)
      payment_confirmation(event.data.object.client_secret)
   else:
      print('Unhandled event type {}'.format(event.type))
   return HttpResponse(status=200)


@login_required
def order_place(request):
   basket = Basket(request)
   basket.clear()
   return render(request, 'checkout/orderplaced.html')
