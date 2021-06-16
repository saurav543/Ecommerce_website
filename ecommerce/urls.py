from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('basket/', include('ecommerce.apps.basket.urls', namespace='basket')),
    path('account/', include('ecommerce.apps.account.urls', namespace='account')),
    path('orders/', include('ecommerce.apps.orders.urls', namespace='orders')),
    # # path("__debug__/", include(debug_toolbar.urls)),
    # # stripe payment
    # path('payment/', include('payment.urls', namespace='payment')),
    path('checkout/', include('ecommerce.apps.checkout.urls', namespace='checkout')),
     path('', include('ecommerce.apps.inventory.urls',namespace='inventory')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
