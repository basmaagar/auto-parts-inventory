from django import forms
from .models import Category, Part, Compatibility, Order

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'reference', 'brand', 'model', 'price', 'technical_specs', 'category', 'quantityinstock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].label = "Price"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CompatibilityForm(forms.ModelForm):
    class Meta:
        model = Compatibility
        fields = ['part', 'vehicle_brand', 'vehicle_model', 'year_start', 'year_end']

from django.core.exceptions import ValidationError

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['part', 'order_quantity']

    def clean(self):
        cleaned_data = super().clean()
        part = cleaned_data.get('part')
        order_quantity = cleaned_data.get('order_quantity')

        if part and order_quantity:
            if order_quantity > part.quantityinstock:
                raise ValidationError(f"Cannot order more than {part.quantityinstock} items in stock for {part.name}.")
        return cleaned_data
