from .forms import (
    AccessoriesForm,
    ParentCategoryForm,
    CategoryForm,
    CustomerForm,
    CustomerUpdateForm,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from WebApp.models import Accessories, Categories, ParentCategories
from WebApp.models import Orders, OrderDetails
import json, csv, codecs,os
from django.conf import settings
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDay, TruncWeek
from django.db.models import Sum, Count, F, Q
from django.http import HttpResponse
from django.utils.timezone import make_aware
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


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
                "Address": order.Address,
                "PhoneNumber": order.PhoneNumber,
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
            phoneNumber = data.get("phoneNumber")
            address = data.get("address")

            order = Orders.objects.get(pk=order_id)
            order.IsPaid = 1 if is_paid == "true" else 0
            order.IsCancelled = 1 if is_cancelled == "true" else 0
            order.PhoneNumber = phoneNumber
            order.Address = address
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
    if Orders.objects.filter(UserID=user).exists():
        messages.error(request, "Không thể xóa khách hàng này vì họ đã có đơn hàng.")
    else:
        user.delete()
        messages.success(request, "Khách hàng đã được xóa thành công.")
    return redirect("admin_customer")


def edit_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("admin_customer")
    else:
        form = CustomerUpdateForm(instance=user)
    return render(request, "pages/edit_customer.html", {"form": form})


def generate_statistics(period="day"):
    if period == "day":
        start_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start_date = timezone.now() - timedelta(days=6)
    elif period == "month":
        start_date = timezone.now() - timedelta(days=29)
    else:
        raise ValueError("Period must be 'day', 'week', or 'month'.")

    orders_query = Orders.objects.filter(OrderDate__gte=start_date)

    total_orders = orders_query.count()

    total_revenue = orders_query.aggregate(total_revenue=Sum("TotalAmount"))[
        "total_revenue"
    ]

    grouped_statistics = {}
    if period in ["day", "week", "month"]:
        for i in range(30 if period == "month" else 7):
            current_date = start_date + timedelta(days=i)
            orders_of_day = orders_query.filter(OrderDate__date=current_date.date())
            total_orders_of_day = orders_of_day.count()
            total_revenue_of_day = orders_of_day.aggregate(
                total_revenue=Sum("TotalAmount")
            )["total_revenue"]
            grouped_statistics[current_date.date()] = {
                "total_orders": total_orders_of_day,
                "total_revenue": total_revenue_of_day,
            }

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "grouped_statistics": grouped_statistics,
    }


def statistical(request, period):
    stats = generate_statistics(period)
    json_array = []

    for date, statistics in stats["grouped_statistics"].items():
        formatted_date = date.strftime("%d/%m/%Y")

        total_orders = statistics["total_orders"]
        total_revenue = statistics["total_revenue"]

        json_array.append(
            {
                "date": formatted_date,
                "total_orders": total_orders,
                "total_revenue": total_revenue,
            }
        )

    return JsonResponse({"statistics_list": json_array})

def custom_sales_report(request):
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        if start_date and end_date:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            # Convert start_date and end_date to aware datetime objects
            start_date = make_aware(datetime.combine(start_date, time.min))
            end_date = make_aware(datetime.combine(end_date, time.max))

            sales = OrderDetails.objects.filter(
                OrderID__OrderDate__range=(start_date, end_date)
            )

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                'attachment; filename="'
                + str(start_date.strftime("%d%m%Y"))
                + "-"
                + str(end_date.strftime("%d%m%Y"))
                + '.pdf"'
            )

            # Create PDF canvas
            p = canvas.Canvas(response, pagesize=letter)
            width, height = letter

            # Path to custom font
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'OpenSans-Regular.ttf')
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            # Thiết lập font in đậm
            p.setFont('Helvetica-Bold', 12)

            # Vẽ tiêu đề của báo cáo với font in đậm
            p.drawString(175, height - 50, f"Sales Report from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}")

            # Đặt lại font về font mặc định

            # Draw table headers
            p.drawString(50, height - 100, "Product ID")
            p.drawString(125, height - 100, "Product Name")
            p.drawString(270, height - 100, "Quantity")
            p.drawString(325, height - 100, "Unit Price")
            p.drawString(425, height - 100, "Total Price")
            p.drawString(500, height - 100, "Order Date")

            y = height - 120  # Initial y position for data rows
            p.setFont('CustomFont', 12)

            for sale in sales:
                p.drawString(50, y, str(sale.AccessoryID.id))
                product_name = sale.AccessoryID.Name
                if len(product_name) > 20:
                    product_name = product_name[:20] + "..."
                p.drawString(125, y, product_name)
                p.drawString(270, y, str(sale.Quantity))
                p.drawString(325, y, f"{sale.UnitPrice:}đ")
                p.drawString(425, y, f"{sale.Quantity * sale.UnitPrice:}đ")
                p.drawString(500, y, sale.OrderID.OrderDate.strftime("%d/%m/%Y"))
                y -= 20  # Move to the next row

                # Check for page overflow and create a new page if needed
                if y < 50:
                    p.showPage()
                    p.setFont('CustomFont', 12)
                    y = height - 50

            p.showPage()
            p.save()

            return response

    # Handle GET request or invalid POST data here
    return HttpResponse("Invalid request method or missing start/end date.")
