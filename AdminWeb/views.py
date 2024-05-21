from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
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




def accessory_list(request):
    accessories = Accessories.objects.all()
    return render(request, 'pages/accessory_list.html', {'accessories': accessories})


def accessory_create(request):
    if request.method == 'POST':
        form = AccessoriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accessory_list')
    else:
        form = AccessoriesForm()
    return render(request, 'pages/accessory_form.html', {'form': form})


def accessory_update(request, id):
    accessory = get_object_or_404(Accessories, id=id)
    if request.method == 'POST':
        form = AccessoriesForm(request.POST, request.FILES, instance=accessory)
        if form.is_valid():
            form.save()
            return redirect('accessory_list')
    else:
        form = AccessoriesForm(instance=accessory)
    return render(request, 'pages/accessory_form.html', {'form': form})

def accessory_delete(request, id):
    accessory = get_object_or_404(Accessories, id=id)
    if request.method == 'POST':
        accessory.delete()
        return redirect('accessory_list')
    return render(request, 'pages/accessory_confirm_delete.html', {'accessory': accessory})