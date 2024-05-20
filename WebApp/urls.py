from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.index, name="home"),
    path(
        "product/parent-category/<int:parent_categories_id>/",
        views.productByParentCategory,
        name="product_by_parent_category",
    ),
    path(
        "product/category/<int:categories_id>/",
        views.productByCategory,
        name="product_by_category",
    ),
    path(
        "product_detail/<int:accessory_id>/",
        views.product_detail,
        name="product_detail",
    ),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("identify", views.identify, name="identify"),
    path("recovery/<uidb64>/<token>/", views.recovery, name="recovery"),
]
