from unicodedata import name
from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from pipestore_project.decorators import user_created_order

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('admin/orders/order/<int:order_id>/pdf', staff_member_required( views.invoice_pdf ), name='invoice_pdf'),
    path('order/<int:order_id>/pdf', user_created_order( views.invoice_pdf ), name="customer_invoice_pdf"),
    path('order/<int:order_id>/', user_created_order( views.order_detail ), name="order_detail"),
]
