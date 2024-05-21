from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login, name="admin_index"),
    path("logout/", logout_admin, name="admin_logout"),
    path("dashboard/", admin_required(dashboard), name="admin_dashboard"),
    path("order/", admin_required(orderDashboard), name="admin_order"),
    path('order/details/<int:order_id>/', orderDetails, name='admin_order_details'),
    path("order/cancel_order/<int:order_id>/", cancelOrder, name="cancel_order"),
    path("order/confirm-payment/<int:order_id>/", confirmPayment, name="confirm_payment"),
    path("order/update/<int:order_id>/", updateOrder, name="updated_order"),
]
