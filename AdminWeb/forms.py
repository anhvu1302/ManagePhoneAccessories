from django import forms
from WebApp.models import Accessories, Categories, ParentCategories

class AccessoriesForm(forms.ModelForm):
    categories = Categories.objects.all()

    CategoryID = forms.ModelChoiceField(
        queryset=categories,
        label="Category",
        empty_label="Select Category"
    )

    class Meta:
        model = Accessories
        fields = ['Name', 'Price', 'Discount', 'Image', 'Description', 'CategoryID']

    def __init__(self, *args, **kwargs):
        super(AccessoriesForm, self).__init__(*args, **kwargs)
        self.fields['CategoryID'].label_from_instance = lambda obj: obj.CategoryName
        self.fields['CategoryID'].widget.attrs.update({'class': 'formbold-form-input formbold-form-textarea'})
