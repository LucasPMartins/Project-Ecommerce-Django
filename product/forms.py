from django import forms
from .models import Product, ProductVariation

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller_id'] 

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = ('price', 'discount_price', 'attributes', 'stock')

ProductVariationFormSet = forms.inlineformset_factory(
    Product,
    ProductVariation,
    form=ProductVariationForm,
    extra=1,  # Número de variações extras exibidas por padrão
    can_delete=True  # Permite remover variações
)