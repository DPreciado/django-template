from .models import Inventario
from django import forms


#crear formulario
class InventarioForm(forms.ModelForm):

    def clean_sku(self):
        # if the sku is already in the database, raise an error
        sku = self.cleaned_data['sku']
        if Inventario.objects.filter(sku=sku).exists() or Inventario.deleted_objects.filter(sku=sku).exists():
            raise forms.ValidationError("One SKU already exits. Please enter a different SKU")
        return sku

    class Meta:
        model = Inventario
        fields = '__all__' # You can change this for the field's name
        exclude = ['is_deleted' , 'deleted_at']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder':'Nombre de producto'}),
            'sku': forms.TextInput(attrs={'placeholder':'Identificador del producto'}),
        }