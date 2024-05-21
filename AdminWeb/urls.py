from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login, name="admin_index"),
    path('logout/', logout_admin, name='admin_logout'),  
    path("dashboard/", admin_required(dashboard), name="admin_dashboard"),
    path('list/', accessory_list, name='accessory_list'),
    path('create/', accessory_create, name='accessory_create'),
    path('update/<int:id>/', accessory_update, name='accessory_update'),
    path('delete/<int:id>/', accessory_delete, name='accessory_delete'),
]

