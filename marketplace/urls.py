from django.urls import path
from . import views

urlpatterns = [

    path('', views.index_view, name='index'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('order/create/<int:product_id>/', views.create_order_view, name='create_order'),
    path('order/status/<str:order_id>/', views.order_status_view, name='order_status'),
    path('dashboard/login/', views.dashboard_login_view, name='dashboard_login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/verify/<str:order_id>/', views.verify_order_admin, name='verify_order_admin'),
    path('viral-promo/', views.viral_promo_view, name='viral_promo'),
    path('create-affiliate/', views.create_affiliate_view, name='create_affiliate'),
    path('buyer-requests/', views.buyer_requests_view, name='buyer_requests'),
    path('buyer-requests/post/', views.post_buyer_request_view, name='post_buyer_request'),
    path('buyer-requests/offer/<int:request_id>/', views.submit_seller_offer_view, name='submit_seller_offer'),
    path('rent-store/', views.rent_store_view, name='rent_store'),
    path('download-master-pdf/', views.download_master_pdf_view, name='download_master_pdf'),
]
