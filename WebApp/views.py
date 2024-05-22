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
)
from .models import Accessories, Categories, ParentCategories
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from WebApp.models import Accessories
from WebApp.vnpay import vnpay
from WebApp.settings import *

# Create your views here.
def index(request):
    data = {
        "accessories": Accessories.objects.all()[:12],
        "parent_categories": ParentCategories.objects.prefetch_related(
            "categories"
        ).all(),
        "user": request.user,
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
        "parent_categories": ParentCategories.objects.prefetch_related(
            "categories"
        ).all(),
    }
    return render(request, "pages/product_detail.html", data)


def productByCategory(request, categories_id=None):
    category = Categories.objects.filter(id=categories_id).first()
    accessories_list = Accessories.objects.filter(CategoryID__id=categories_id)

    paginator = Paginator(accessories_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    parent_categories = ParentCategories.objects.prefetch_related("categories").all()

    data = {
        "accessories": page_obj,
        "parent_categories": parent_categories,
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

    parent_categories = ParentCategories.objects.prefetch_related("categories").all()

    data = {
        "accessories": page_obj,
        "parent_categories": parent_categories,
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

    parent_categories = ParentCategories.objects.prefetch_related("categories").all()

    data = {
        "accessories": accessories,
        "parent_categories": parent_categories,
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


def create_payment(request):
    return render(request, "pages/create_payment.html", {"title": "Danh sách demo"})


def hmacsha512(key, data):
    byteKey = key.encode("utf-8")
    byteData = data.encode("utf-8")
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


def payment(request):

    if request.method == "POST":
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data["order_type"]
            order_id = form.cleaned_data["order_id"]
            amount = form.cleaned_data["amount"]
            order_desc = form.cleaned_data["order_desc"]
            # bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data["language"]
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData["vnp_Version"] = "2.1.0"
            vnp.requestData["vnp_Command"] = "pay"
            vnp.requestData["vnp_TmnCode"] = VNPAY_TMN_CODE
            vnp.requestData["vnp_Amount"] = amount * 100
            vnp.requestData["vnp_CurrCode"] = "VND"
            vnp.requestData["vnp_TxnRef"] = order_id
            vnp.requestData["vnp_OrderInfo"] = order_desc
            vnp.requestData["vnp_OrderType"] = order_type
            # Check language, default: vn
            if language and language != "":
                vnp.requestData["vnp_Locale"] = language
            else:
                vnp.requestData["vnp_Locale"] = "vn"


            vnp.requestData["vnp_CreateDate"] = datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )  # 20150410063022
            vnp.requestData["vnp_IpAddr"] = ipaddr
            vnp.requestData["vnp_ReturnUrl"] = VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(
                VNPAY_PAYMENT_URL, VNPAY_HASH_SECRET_KEY
            )
            print(vnpay_payment_url)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "pages/payment.html", {"title": "Thanh toán"})

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
        if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
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
