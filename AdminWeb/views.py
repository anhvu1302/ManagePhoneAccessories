from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from WebApp.models import Orders, OrderDetails
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from WebApp.models import Accessories


from .forms import AccessoriesForm


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("/admin")
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
