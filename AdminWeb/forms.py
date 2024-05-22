from django import forms
from WebApp.models import Accessories, Categories, ParentCategories

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
