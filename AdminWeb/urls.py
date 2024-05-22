from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login, name="admin_index"),
    path("logout/", logout_admin, name="admin_logout"),
    path("dashboard/", admin_required(dashboard), name="admin_dashboard"),
    path("order/", orderDashboard, name="admin_order"),
    path('order/details/<int:order_id>', orderDetails, name='admin_order_details'),
    path("order/cancel_order/<int:order_id>/", cancelOrder, name="cancel_order"),
    path("order/confirm-payment/<int:order_id>/", confirmPayment, name="confirm_payment"),
    path("order/update/<int:order_id>/", updateOrder, name="updated_order"),
    path('list/', accessory_list, name='accessory_list'),
    path('create/', accessory_create, name='accessory_create'),
    path('update/<int:id>/', accessory_update, name='accessory_update'),
    path('delete/<int:id>/', accessory_delete, name='accessory_delete'),
    path('manage-categories/', manage_categories, name='manage_categories'),
    path('delete_parent/<int:id>/', delete_parent_category, name='delete_parent_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),
]

