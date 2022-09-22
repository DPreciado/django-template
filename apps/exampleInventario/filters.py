import django_filters
from django.db.models import Q
from .models import Inventario


inventario_fields = {
    'nombre': {'label': 'Nombre'},
    'sku':{'label': 'SKU'},
}

class InventarioFilter(django_filters.FilterSet):

    class Meta:
        model = Inventario
        fields = list(inventario_fields.keys())
    
    def __init__(self, *args, **kwargs):
        super(InventarioFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            self.filters[field_name].label = inventario_fields[field_name]['label']
            self.filters[field_name].field.widget.attrs.update({
                'class': 'form-control', 'placeholder': inventario_fields[field_name]['label']
            })

            # If it's an input field, change it so that it uses contains
            if self.filters[field_name].__class__.__name__ == 'CharFilter':
                self.filters[field_name].lookup_expr = 'icontains'
