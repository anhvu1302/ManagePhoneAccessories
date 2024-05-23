from django import template
from WebApp.models import ParentCategories, Cart

register = template.Library()


@register.inclusion_tag("partials/navbar.html")
def load_navbar():
    parent_categories = ParentCategories.objects.prefetch_related("categories").all()
    return {"parent_categories": parent_categories}


@register.inclusion_tag("partials/userBox.html", takes_context=True)
def loadUserBox(context):
    request = context["request"]
    return {"user": request.user}


@register.inclusion_tag("partials/cartQuantity.html", takes_context=True)
def loadCartQuantity(context):
    request = context["request"]
    cart_items = Cart.objects.filter(UserID=request.user)
    total_num = sum(item.Quantity for item in cart_items)
    return {"total_num": total_num}


@register.inclusion_tag("partials/heartQuantity.html", takes_context=True)
def loadHeartQuantity(context):
    # request = context['request']
    # cart_items = Cart.objects.filter(UserID=request.user)
    # total_num = sum(item.Quantity for item in cart_items)
    # print(cart_items)
    # for cart in cart_items:
    #     print(cart.Quantity)
    return {"total_num": 0}
