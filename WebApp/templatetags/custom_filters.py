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

@register.filter
def obfuscate_email(email):
    if '@' not in email:
        return email 

    local_part, domain = email.split('@')
    if len(local_part) < 2:
        return email 

    return f'{local_part[0]}********{local_part[-1]}@{domain}'