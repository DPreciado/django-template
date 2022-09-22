from .models import Purchase
from django import forms

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__' # You can change this for the field's name
        exclude = ['is_deleted' , 'deleted_at']
        
        labels = {
            'description': ('Descripción'),
            'product_count': ('Número de productos'),
            'total_price': (''),
            'date': ('Fecha'),
        }
        widgets = {
            'description': forms.TextInput(attrs={'placeholder':'Descripción de la compra'}),
            'product_count': forms.NumberInput(attrs={'placeholder':'0', 'value':'0', 'id':'product_count', 'min':'0'}),
            'total_price': forms.NumberInput(attrs={'placeholder':'0', 'value':'0'}),
            'date': forms.DateInput(attrs={'type':'date'}),
        }
