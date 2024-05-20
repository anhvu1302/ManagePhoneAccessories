from django.urls import path
from .views import *

urlpatterns = [
    path("", admin_login, name="admin_index"),
    path('logout/', logout_admin, name='admin_logout'),  
    path("dashboard/", admin_required(dashboard), name="admin_dashboard"),
]
