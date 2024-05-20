from pyexpat import model
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import AuthenticationForm
from django.shortcuts import redirect
from .forms import IdentifyForm
from .forms import RegistrationForm
from .forms import RecoveryForm
from .models import Accessories, Categories, ParentCategories
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str


# Create your views here.
def index(request):
    data = {
        "accessories": Accessories.objects.all()[:12],
        "parent_categories": ParentCategories.objects.prefetch_related(
            "categories"
        ).all(),
    }
    return render(request, "pages/index.html", data)


def product_detail(request, accessory_id):
    accessory = Accessories.objects.filter(id=accessory_id).first()
    if accessory:
        data = {
            "accessory": accessory,
            "parent_categories": ParentCategories.objects.prefetch_related(
                "categories"
            ).all(),
        }
        return render(request, "pages/product_detail.html", data)
    else:
        return redirect("login")


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


def login(request):
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
