from .forms import AccessoriesForm, ParentCategoryForm, CategoryForm, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from WebApp.models import Accessories, Categories, ParentCategories
from WebApp.models import Orders, OrderDetails
import json


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin/")
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect("./dashboard/")

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj = User.objects.filter(username=username).first()

            if not user_obj:
                messages.info(request, "Account not found")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            user_obj = authenticate(username=username, password=password)

            if user_obj:
                if user_obj.is_staff:
                    login(request, user_obj)
                    return redirect("./dashboard/")
                else:
                    messages.info(
                        request,
                        "Bạn không có quyền quản trị. Vui lòng liên hệ với admin",
                    )
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            else:
                messages.info(request, "Tên tài khoản hoặc mật khẩu không đúng")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        return render(request, "pages/adminLogin.html")

    except Exception as e:
        print(e)
        messages.error(request, "An unexpected error occurred. Please try again later.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def logout_admin(request):
    logout(request)
    return redirect("/admin")


def dashboard(request):
    return render(request, "pages/dashboard.html")


def orderDashboard(request):
    search_type = request.GET.get("searchType")
    search_input = request.GET.get("searchInput")
    orders_list = None

    if search_type == "id":
        try:
            search_input = int(search_input)
            orders_list = Orders.objects.filter(id=search_input)
        except ValueError:
            pass
    elif search_type == "customerName":
        if search_input:
            orders_list = Orders.objects.filter(
                UserID__username__icontains=search_input
            )
    else:
        orders_list = Orders.objects.select_related("UserID").all()

    if not orders_list:
        orders_list = Orders.objects.none()

    paginator = Paginator(orders_list, 1)

    page = request.GET.get("page")
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    return render(request, "pages/order.html", {"orders": orders})


def orderDetails(request, order_id):
    if request.method == "GET":
        try:
            order = get_object_or_404(Orders, id=order_id)
            order_details = order.order_details.all()

            order_data = {
                "id": order.id,
                "UserID": order.UserID.username,
                "TotalAmount": order.TotalAmount,
                "IsCancelled": order.IsCancelled,
                "IsPaid": order.IsPaid,
                "OrderDate": order.OrderDate.strftime("%Y-%m-%d %H:%M:%S"),
                "order_details": [],
            }

            for detail in order_details:
                order_data["order_details"].append(
                    {
                        "id": detail.id,
                        "AccessoryID": {
                            "id": detail.AccessoryID.id,
                            "Name": detail.AccessoryID.Name,
                            "Price": detail.AccessoryID.Price,
                            "Discount": detail.AccessoryID.Discount,
                            "Image": detail.AccessoryID.Image.url,
                            "Description": detail.AccessoryID.Description,
                        },
                        "Quantity": detail.Quantity,
                        "UnitPrice": detail.UnitPrice,
                    }
                )

            return JsonResponse(order_data, safe=False)
        except Orders.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def updateOrder(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            is_paid = data.get("isPaid")
            is_cancelled = data.get("isCancelled")

            order = Orders.objects.get(pk=order_id)
            order.IsPaid = 1 if is_paid == "true" else 0
            order.IsCancelled = 1 if is_cancelled == "true" else 0
            order.save()

            return JsonResponse(
                {
                    "success": True,
                }
            )
        except Orders.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})


def confirmPayment(request, order_id):
    if request.method == "POST":
        try:
            order = Orders.objects.get(pk=order_id)
            order.IsPaid = 1
            order.save()
            return JsonResponse({"success": True})
        except Orders.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def cancelOrder(request, order_id):
    if request.method == "POST":
        try:
            order = Orders.objects.get(pk=order_id)
            order.IsCancelled = 1
            order.save()
            return JsonResponse({"success": True})
        except Orders.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
    return JsonResponse({"success": False, "error": "Invalid request method"})


def accessory_list(request):
    accessories = Accessories.objects.all()
    return render(request, "pages/accessory_list.html", {"accessories": accessories})


def accessory_create(request):
    if request.method == "POST":
        form = AccessoriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("accessory_list")
    else:
        form = AccessoriesForm()
    return render(request, "pages/accessory_form.html", {"form": form})


def accessory_update(request, id):
    accessory = get_object_or_404(Accessories, id=id)
    if request.method == "POST":
        form = AccessoriesForm(request.POST, request.FILES, instance=accessory)
        if form.is_valid():
            form.save()
            return redirect("accessory_list")
    else:
        form = AccessoriesForm(instance=accessory)
    return render(request, "pages/accessory_form.html", {"form": form})


def accessory_delete(request, id):
    accessory = get_object_or_404(Accessories, id=id)
    if request.method == "POST":
        accessory.delete()
        return redirect("accessory_list")
    return render(
        request, "pages/accessory_confirm_delete.html", {"accessory": accessory}
    )


def manage_categories(request):
    parent_form = ParentCategoryForm(request.POST or None)
    category_form = CategoryForm(request.POST or None)

    if request.method == "POST":
        if "add_parent_category" in request.POST and parent_form.is_valid():
            parent_form.save()
        elif "add_category" in request.POST and category_form.is_valid():
            category_form.save()
        elif "save_changes" in request.POST:
            for key, value in request.POST.items():
                if key.startswith("parent_category_"):
                    parent_category_id = int(key.split("_")[-1])
                    parent_category = ParentCategories.objects.get(
                        id=parent_category_id
                    )
                    parent_category.ParentCategoryName = value
                    parent_category.save()
                elif key.startswith("category_"):
                    category_id = int(key.split("_")[-1])
                    category = Categories.objects.get(id=category_id)
                    category.CategoryName = value
                    category.save()

    parent_categories = ParentCategories.objects.all()
    categories = Categories.objects.all()

    return render(
        request,
        "pages/manage_categories.html",
        {
            "parent_form": parent_form,
            "category_form": category_form,
            "parent_categories": parent_categories,
            "categories": categories,
        },
    )


def delete_parent_category(request, id):
    parent_category = get_object_or_404(ParentCategories, id=id)
    parent_category.delete()
    return redirect("manage_categories")


def delete_category(request, id):
    category = get_object_or_404(Categories, id=id)
    category.delete()
    return redirect("manage_categories")


def customerDashboard(request):
    search_type = request.GET.get("searchType")
    search_input = request.GET.get("searchInput")
    customers_list = User.objects.filter(is_superuser=False).order_by("id")

    if search_type == "first_name":
        try:
            if search_input:
                customers_list = User.objects.filter(
                    first_name__icontains=search_input, is_superuser=False
                )
        except ValueError:
            pass
    elif search_type == "username":
        if search_input:
            customers_list = User.objects.filter(
                username__icontains=search_input, is_superuser=False
            )

    paginator = Paginator(customers_list, 3)  # Số lượng khách hàng mỗi trang
    page_number = request.GET.get("page")

    try:
        customers = paginator.page(page_number)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    return render(request, "pages/customer.html", {"customers": customers})


def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_customer")
    else:
        form = CustomerForm()
    return render(request, "pages/add_customer.html", {"form": form})


def delete_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "Khách hàng đã được xóa thành công.")
    return redirect("admin_customer")


def edit_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin_customer")
    else:
        form = CustomerForm(instance=user)
    return render(request, "pages/edit_customer.html", {"form": form})
