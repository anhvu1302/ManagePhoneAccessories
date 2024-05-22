from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("policy", views.policy, name="policy"),
    path("home", views.index, name="home"),
    path(
        "product/parent-category/<int:parent_categories_id>",
        views.productByParentCategory,
        name="product_by_parent_category",
    ),
    path(
        "product/category/<int:categories_id>",
        views.productByCategory,
        name="product_by_category",
    ),
    path("search/", views.search_accessories, name="search_accessories"),
    path(
        "product_detail/<int:accessory_id>",
        views.productDetail,
        name="productDetail",
    ),
    path("logout", views.userLogout, name="logout"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("identify", views.identify, name="identify"),
    path("recovery/<uidb64>/<token>/", views.recovery, name="recovery"),
]
