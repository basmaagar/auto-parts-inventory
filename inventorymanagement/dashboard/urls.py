from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/', views.staff, name='staff'),
    path('staff/<int:pk>/', views.staff_detail, name='staff_detail'),
    path('product/', views.product, name='product'),
    path('admin_part_add/', views.admin_part_add, name='admin_part_add'),
    path('product_edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product_delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('order/', views.order, name='order'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('receipt_order/<int:order_id>/', views.receipt_order, name='receipt_order'),
    path('invoice_detail/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice_pdf/<int:invoice_id>/', views.invoice_pdf, name='invoice_pdf'),
    path('parts_data/', api_views.parts_data, name='parts_data'),
    path('orders_data/', api_views.orders_data, name='orders_data'),

    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:part_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:part_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:part_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),

    # About Us page
    path('about_us/', views.about_us, name='about_us'),
]
