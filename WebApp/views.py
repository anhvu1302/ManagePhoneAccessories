import hashlib
import hmac
import json
import random
import requests
from .forms import (
    AuthenticationForm,
    IdentifyForm,
    RecoveryForm,
    RegistrationForm,
    PaymentForm,
    OrderForm,
)
from .models import (
    Accessories,
    Categories,
    ParentCategories,
    Orders,
    OrderDetails,
    Cart,
)
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from WebApp.settings import *
from WebApp.vnpay import vnpay


# Create your views here.
def index(request):

    data = {
        "accessories": Accessories.objects.all()[:12],
    }
    return render(request, "pages/index.html", data)


def contact(request):
    return render(request, "pages/contact.html")


def policy(request):
    return render(request, "pages/policy.html")


def productDetail(request, accessory_id):
    accessory = Accessories.objects.filter(id=accessory_id).first()
    data = {
        "accessory": accessory,
    }
    return render(request, "pages/product_detail.html", data)


def productByCategory(request, categories_id=None):
    category = Categories.objects.filter(id=categories_id).first()
    accessories_list = Accessories.objects.filter(CategoryID__id=categories_id)

    paginator = Paginator(accessories_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {
        "accessories": page_obj,
        "category": category,
    }

    return render(request, "pages/productByCategory.html", data)


def productByParentCategory(request, parent_categories_id=None):
    parCategory = ParentCategories.objects.filter(id=parent_categories_id).first()
    accessories_list = Accessories.objects.filter(
        CategoryID__ParentCategoryID__id=parent_categories_id
    )

    paginator = Paginator(accessories_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {
        "accessories": page_obj,
        "parCategory": parCategory,
    }

    return render(request, "pages/productByParentCategory.html", data)


def search_accessories(request):
    query = request.GET.get("name", "")
    accessories_list = []

    if query:
        accessories_list = Accessories.objects.filter(Name__contains=query)

    paginator = Paginator(accessories_list, 4)
    page = request.GET.get("page")
    try:
        accessories = paginator.page(page)
    except PageNotAnInteger:
        accessories = paginator.page(1)
    except EmptyPage:
        accessories = paginator.page(paginator.num_pages)

    data = {
        "accessories": accessories,
        "query": query,
    }

    return render(request, "pages/search_results.html", data)


def userLogout(request):
    logout(request)
    return redirect("/")


def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            return redirect("index")
        else:
            return render(request, "pages/login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "pages/login.html", {"form": form})


def register(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/login")
    return render(request, "pages/register.html", {"form": form})


def identify(request):
    if request.method == "POST":
        form = IdentifyForm(request.POST)
        if form.is_valid():
            try:
                form.send_password_reset_email(request)
                return render(request, "pages/success.html")
            except ValidationError as e:
                form.add_error("email", e)
    else:
        form = IdentifyForm()
    return render(request, "pages/identify.html", {"form": form})


def recovery(request, uidb64, token):
    if request.method == "POST":
        form = RecoveryForm(data=request.POST, uidb64=uidb64, token=token)
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            form.save(new_password)

        return redirect("login")
    else:
        form = RecoveryForm(uidb64=uidb64, token=token)
    return render(request, "pages/recovery.html", {"form": form})


def send_payment_confirmation_email(order, order_details):
    subject = "Xác nhận thanh toán thành công"
    context = {"order": order, "order_details": order_details}
    html_message = render_to_string("emails/payment_success.html", context)
    plain_message = strip_tags(html_message)
    from_email = EMAIL_HOST_USER
    to = order.UserID.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def create_payment(request):
    return render(request, "pages/create_payment.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode("utf-8")
    byteData = data.encode("utf-8")
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(orderId, amount, ipaddr):
    vnp = vnpay()
    vnp.requestData["vnp_Version"] = "2.1.0"
    vnp.requestData["vnp_Command"] = "pay"
    vnp.requestData["vnp_TmnCode"] = VNPAY_TMN_CODE
    vnp.requestData["vnp_Amount"] = amount * 100
    vnp.requestData["vnp_CurrCode"] = "VND"
    vnp.requestData["vnp_TxnRef"] = datetime.now().strftime("%Y%m%d%H%M%S")
    vnp.requestData["vnp_OrderInfo"] = "VNPAY " + str(orderId)
    vnp.requestData["vnp_OrderType"] = "billpayment"
    vnp.requestData["vnp_Locale"] = "vn"

    vnp.requestData["vnp_CreateDate"] = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # 20150410063022
    vnp.requestData["vnp_IpAddr"] = ipaddr
    vnp.requestData["vnp_ReturnUrl"] = VNPAY_RETURN_URL
    vnpay_payment_url = vnp.get_payment_url(VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY)
    return vnpay_payment_url


def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData["vnp_TxnRef"]
        amount = int(inputData["vnp_Amount"]) / 100
        order_desc = inputData["vnp_OrderInfo"]
        vnp_TransactionNo = inputData["vnp_TransactionNo"]
        vnp_ResponseCode = inputData["vnp_ResponseCode"]
        vnp_TmnCode = inputData["vnp_TmnCode"]
        vnp_PayDate = inputData["vnp_PayDate"]
        vnp_BankCode = inputData["vnp_BankCode"]
        vnp_CardType = inputData["vnp_CardType"]
        order = Orders.objects.get(id=int(order_desc.split()[1]))

        if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":

                if not order.IsPaid:
                    orders_list = Orders.objects.filter(id=int(order_desc.split()[1]))
                    order_details = OrderDetails.objects.filter(OrderID=orders_list[0])
                    send_payment_confirmation_email(orders_list[0], order_details)
                    order.IsPaid = 1
                    order.save()
                return render(
                    request,
                    "pages/payment_return.html",
                    {
                        "title": "Kết quả thanh toán",
                        "result": "Thành công",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode,
                    },
                )
            else:
                return render(
                    request,
                    "pages/payment_return.html",
                    {
                        "title": "Kết quả thanh toán",
                        "result": "Lỗi",
                        "order_id": order_id,
                        "amount": amount,
                        "order_desc": order_desc,
                        "vnp_TransactionNo": vnp_TransactionNo,
                        "vnp_ResponseCode": vnp_ResponseCode,
                    },
                )
        else:
            return render(
                request,
                "pages/payment_return.html",
                {
                    "title": "Kết quả thanh toán",
                    "result": "Lỗi",
                    "order_id": order_id,
                    "amount": amount,
                    "order_desc": order_desc,
                    "vnp_TransactionNo": vnp_TransactionNo,
                    "vnp_ResponseCode": vnp_ResponseCode,
                    "msg": "Sai checksum",
                },
            )
    else:
        return render(
            request,
            "pages/payment_return.html",
            {"title": "Kết quả thanh toán", "result": ""},
        )


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


n = random.randint(10**11, 10**12 - 1)
n_str = str(n)
while len(n_str) < 12:
    n_str = "0" + n_str


def get_data_from_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(UserID=request.user)
    else:
        session_cart = request.session.get("cart_items", {})
        cart_items = []
        for accessory_id, quantity_dict in session_cart.items():
            # Extract accessory ID and quantity
            accessory = Accessories.objects.get(id=accessory_id)
            quantity = quantity_dict["quantity"]
            cart_item = Cart(UserID=None, AccessoryID=accessory, Quantity=quantity)
            cart_items.append(cart_item)
    total_num = sum(item.Quantity for item in cart_items)
    if total_num == 0:
        has_item = False
    else:
        has_item = True

    return total_num, has_item


def viewOrder(request):
    all_orders = Orders.objects.all()

    for order in all_orders:
        order_details = OrderDetails.objects.filter(OrderID=order)
        order.order_details.set(order_details)

    paginator = Paginator(all_orders, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data = {
        "orders": page_obj,
    }
    return render(request, "pages/user_order.html", data)


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(UserID=request.user)
        user = request.user
        user_id = user.id

    else:
        user = None
        user_id = 2
        session_cart = request.session.get("cart_items", {})
        cart_items = []
        for accessory_id, quantity_dict in session_cart.items():
            # Extract accessory ID and quantity
            accessory = Accessories.objects.get(id=accessory_id)
            quantity = quantity_dict["quantity"]
            cart_item = Cart(UserID=None, AccessoryID=accessory, Quantity=quantity)
            cart_items.append(cart_item)

    if cart_items is None or len(cart_items) == 0:
        items_recommend = {
            "accessories": Accessories.objects.all()[:12],
            "parent_categories": ParentCategories.objects.prefetch_related(
                "categories"
            ).all(),
            "has_items": False,
        }
        return render(request, "pages/cart.html", items_recommend)

    total_num = sum(item.Quantity for item in cart_items)
    TotalAmount = sum(item.AccessoryID.Price * item.Quantity for item in cart_items)
    total_discount_price = sum(
        item.Quantity * item.AccessoryID.Price * (item.AccessoryID.Discount / 100)
        for item in cart_items
    )
    have_to_pay = TotalAmount - total_discount_price

    context = {
        "user": user,
        "has_items": True,
        "cart_items": cart_items,
        "TotalAmount": TotalAmount,
        "total_discount_price": total_discount_price,
        "total_num": total_num,
        "have_to_pay": int(have_to_pay),
        "form": OrderForm(
            initial={
                "user_id": user_id,
                "total_amount": int(have_to_pay),
            }
        ),
        # Data send to view
    }
    return render(request, "pages/cart.html", context)


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        session_cart = request.session.get("cart_items", {})
        if product_id in session_cart:
            quantity_dict = session_cart[product_id]
            current_quantity = quantity_dict["quantity"]
            current_quantity += 1
            session_cart[product_id] = {"quantity": current_quantity}
        else:
            session_cart[product_id] = {"quantity": 1}

        request.session["cart_items"] = session_cart
    else:
        product = Accessories.objects.get(id=product_id)
        cart_item, created = Cart.objects.get_or_create(
            AccessoryID=product, UserID=request.user, defaults={"Quantity": 1}
        )
        if not created:
            cart_item.Quantity += 1
        cart_item.save()

    return redirect("/cart/")


def increase_cartItem(request, product_id):
    if not request.user.is_authenticated:
        session_cart = request.session.get("cart_items", {})
        if product_id not in session_cart:
            session_cart[product_id] = {"quantity": 1}
        else:
            quantity_dict = session_cart[product_id]
            current_quantity = quantity_dict["quantity"]
            current_quantity += 1
            session_cart[product_id] = quantity_dict
            request.session["cart_items"] = session_cart
    else:
        product = Accessories.objects.get(id=product_id)
        cart_item = Cart.objects.get(AccessoryID=product, UserID=request.user)
        cart_item.Quantity += 1
        cart_item.save()

    return HttpResponseRedirect("/cart/")


def decrease_cartItem(request, product_id):
    if not request.user.is_authenticated:
        session_cart = request.session.get("cart_items", {})
        if product_id not in session_cart:
            session_cart[product_id] = {"quantity": 1}
        else:
            quantity_dict = session_cart[product_id]
            current_quantity = quantity_dict["quantity"]
            current_quantity -= 1
            session_cart[product_id] = quantity_dict
            request.session["cart_items"] = session_cart
    else:
        product = Accessories.objects.get(id=product_id)
        cart_item = Cart.objects.get(AccessoryID=product, UserID=request.user)
        cart_item.Quantity -= 1
        cart_item.save()
        if cart_item.Quantity == 0:
            cart_item.delete()
    return HttpResponseRedirect("/cart/")


def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        product = Accessories.objects.get(id=product_id)
        cart_item = Cart.objects.get(AccessoryID=product, UserID=request.user)
        cart_item.delete()

    return HttpResponseRedirect("/cart/")


def view_orders_list(request):
    pass


def view_order_detail(request):
    pass


def add_order(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        total_amount = request.POST["total_amount"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        paymentMethod = request.POST["PaymentMethod"]

        try:
            with transaction.atomic():
                # Save to Orders
                user = User.objects.get(id=user_id)
                newOrder = Orders(
                    UserID=user,
                    TotalAmount=int(total_amount),
                    PhoneNumber=phone_number,
                    Address=address,
                )
                newOrder.save()

                # Get items in Cart and add each of them to OrderDetails
                cart_items = Cart.objects.filter(UserID=user)
                for item in cart_items:
                    newOrderDetails = OrderDetails(
                        OrderID=newOrder,
                        AccessoryID=item.AccessoryID,
                        Quantity=item.Quantity,
                        UnitPrice=item.AccessoryID.Price,
                    )
                    newOrderDetails.save()

                # After payment, delete items in cart of user
                Cart.objects.filter(UserID=user).delete()

                if paymentMethod == "VNPAY":
                    paymentUrl = payment(
                        newOrder.id, newOrder.TotalAmount, get_client_ip(request)
                    )
                    return redirect(paymentUrl)
                else:
                    return HttpResponse("Thanh toán thành công!")
        except Exception as e:
            return HttpResponse(f"Thanh toán thất bại! Lỗi: {str(e)}")

    else:
        return HttpResponseRedirect("/cart")
