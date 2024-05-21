from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect


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
                if user_obj.is_superuser:
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
