from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static
app_name = 'basket'

urlpatterns = [
    path('', views.basket_summery, name='basket_summary'),
    path('add/', views.basket_add, name="basket_add"),
    path('delete/', views.basket_delete, name="basket_delete"),
    path('update/', views.basket_update, name="basket_update"),
]
