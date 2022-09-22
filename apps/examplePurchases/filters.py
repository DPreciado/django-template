import django_filters
from django import forms
from django_filters.widgets import RangeWidget
from django.db.models import Q
from .models import Purchase


purchase_fields = {
    'date': {'label': 'Fecha'},
    'total_price':{'label': 'Gasto'},
    'description':{'label': 'Descripción'},
}

class PurchaseFilter(django_filters.FilterSet):
    # override the default behaviour
    date = django_filters.DateFromToRangeFilter(label="Fecha", widget=RangeWidget(attrs={'type': 'date'}))
    total_price = django_filters.NumericRangeFilter(label="Gasto", lookup_expr='range', widget=RangeWidget(attrs={'type': 'number'}))

    class Meta:
        model = Purchase
        fields = list(purchase_fields.keys())
    
    def __init__(self, *args, **kwargs):
        super(PurchaseFilter, self).__init__(*args, **kwargs)
        for field_name in self.get_fields():
            self.filters[field_name].label = purchase_fields[field_name]['label']
            self.filters[field_name].field.widget.attrs.update({
                'class': 'form-control', 'placeholder': purchase_fields[field_name]['label']
            })

            # If it's an input field, change it so that it uses contains
            #if self.filters[field_name].__class__.__name__ == 'CharFilter':
            #    self.filters[field_name].lookup_expr = 'icontains'
