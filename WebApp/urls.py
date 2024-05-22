from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact", views.contact, name="contact"),
    path("policy", views.policy, name="policy"),
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
    # vnpay url
    path("create-payment", views.create_payment, name="create_payment"),
    path("payment", views.payment, name="payment"),
    path("payment_return", views.payment_return, name="payment_return"),

    # cart
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_cartItem,
        name="decrease_cartItem",
    ),
    path(
        "cart/increase/<int:product_id>/",
        views.increase_cartItem,
        name="increase_cartItem",
    ),
    path(
        "cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"
    ),
    path("cart/order/", views.add_order, name="order"),
]
