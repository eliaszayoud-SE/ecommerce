from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('category', views.CategoryViewSet)
router.register('item', views.ItemsViewSet)
# router.register('favorite', views.FavoriteViewSet)

urlpatterns = [
    path('home_data/', views.home_data),
    path('add_favorite/', views.add_favorite),
    path('delete_favorite/', views.delete_favorite),
    path('list_favorite/', views.list_favorite),
    path('add_to_cart/', views.add_to_cart),
    path('delete_from_cart/', views.delete_from_cart),
    path('get_count_cart/', views.get_count_cart),
    path('view_cart/', views.view_cart),
    path('search/', views.search),
    path('add_address/', views.add_address),
    path('delete_address/', views.delete_address),
    path('view_address/', views.view_address),
    path('check_coupon/', views.check_coupon),
    path('checkout/', views.checkout),
    path('view_order/', views.view_pending_order),
    path('view_archive_order/', views.view_archive_order),
    path('notification_test/', views.notification_test),
    path('approved_order/', views.approved_order),
    path('view_notification/', views.view_notification),
    path('order_details/', views.order_details),
    path('delete_order/', views.delete_order),
    path('offers_item/', views.offers_item),
    path('order_prepared/', views.order_prepared),
    path('order_approved_by_delivery/', views.order_approved_by_delivery),
    path('order_delivery/', views.order_delivery),
    path('view_archive_order_for_delivery/', views.view_archive_order_for_delivery),
    path('view_bending_order_for_delivery/', views.view_bending_order_for_delivery),
    path('view_accepted_order_for_delivery/', views.view_accepted_order_for_delivery),
    path('view_order_for_admin/', views.view_order_for_admin),
    path('view_archive_order_for_admin/', views.view_archive_order_for_admin),
    path('add_categories/', views.add_categories),
    path('view_categories/', views.view_categories),
    path('delete_categories/', views.delete_categories),
    path('edit_categories/', views.edit_categories),
]

urlpatterns += router.urls
