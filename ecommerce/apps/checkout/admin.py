from django.contrib import admin
from .models import PaymentSelections,DeliveryOptions

# Register your models here.
admin.site.register(PaymentSelections)
admin.site.register(DeliveryOptions)
