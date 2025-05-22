from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='index'),
    path('staff/', views.staff, name='staff'),
    path('product/', views.product, name='product'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('product/add/', views.admin_part_add, name='admin_part_add'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/', views.order, name='order'),
    path('order/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('order/receipt/<int:order_id>/', views.receipt_order, name='receipt_order'),
    path('staff/detail/<int:pk>', views.staff_detail, name='staff_detail'),
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.invoice_pdf, name='invoice_pdf'),
]
