from django.urls import path
from customer.views import CustomerViewSet

urlpatterns = [
    path('customer/<id>/', CustomerViewSet.as_view(), name='customer_service'),
    path('customer/', CustomerViewSet.as_view(), name='customer_service'),
]
