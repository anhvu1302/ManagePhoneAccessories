from django import forms
from WebApp.models import Accessories, Categories, ParentCategories
from django.contrib.auth.models import User

class ParentCategoryForm(forms.ModelForm):
    class Meta:
        model = ParentCategories
        fields = ["ParentCategoryName"]


class CategoryForm(forms.ModelForm):

    Parent_categories = ParentCategories.objects.all()
    ParentCategoryID = forms.ModelChoiceField(
        queryset=Parent_categories,
        label="Parent Category",
        empty_label="Select Parent Category",
    )

    class Meta:
        model = Categories
        fields = ["CategoryName", "ParentCategoryID"]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields["ParentCategoryID"].label_from_instance = (
            lambda obj: obj.ParentCategoryName
        )
        self.fields["ParentCategoryID"].widget.attrs.update(
            {"class": "formbold-form-input formbold-form-textarea"}
        )


class AccessoriesForm(forms.ModelForm):
    categories = Categories.objects.all()

    CategoryID = forms.ModelChoiceField(
        queryset=categories, label="Category", empty_label="Select Category"
    )

    class Meta:
        model = Accessories
        fields = ["Name", "Price", "Discount", "Image", "Description", "CategoryID"]

    def __init__(self, *args, **kwargs):
        super(AccessoriesForm, self).__init__(*args, **kwargs)
        self.fields["CategoryID"].label_from_instance = lambda obj: obj.CategoryName
        self.fields["CategoryID"].widget.attrs.update(
            {"class": "formbold-form-input formbold-form-textarea"}
        )
class CustomerForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_active",
        ]

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if self.instance.pk:  # Nếu đang chỉnh sửa
            if (
                User.objects.filter(username=username)
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise forms.ValidationError(
                    "Tên tài khoản này đã tồn tại. Vui lòng chọn tên khác."
                )
        else:  # Nếu đang thêm mới
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    "Tên tài khoản này đã tồn tại. Vui lòng chọn tên khác."
                )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if self.instance.pk:  # Nếu đang chỉnh sửa
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    "Email này đã được sử dụng. Vui lòng chọn email khác."
                )
        else:  # Nếu đang thêm mới
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "Email này đã được sử dụng. Vui lòng chọn email khác."
                )
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:  # Kiểm tra nếu mật khẩu trống
            raise forms.ValidationError("Mật khẩu không được để trống.")
        return password

    def save(self, commit=True):
        user = super(CustomerForm, self).save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user