# WebApp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def format_currency(value):
    try:
        numeric_value = int(value)
        return f"{numeric_value:,.0f}đ".replace(",", ".")
    except ValueError:
        return value


@register.filter
def format_discounted_price(price, discount):
    try:
        discounted_price = price * (100 - discount) / 100
        return f"{discounted_price:,.0f}đ".replace(",", ".")
    except (ValueError, TypeError):
        return price
