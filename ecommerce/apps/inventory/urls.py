from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'inventory'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('<slug:slug>/', views.product_detail, name="product_details"),
    path('shop/<slug:slug>/', views.category_list, name="category_list"),
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
