from re import template
from django.shortcuts import redirect, render
from django.db import models
from .models import Inventario
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django_filters.views import FilterView
from django.urls import reverse_lazy
from .forms import InventarioForm
from .filters import InventarioFilter
from django.db import transaction


class Index(FilterView):
    model = Inventario
    template_name = "exampleInventario/index.html"
    context_object_name = 'inventario'
    paginate_by = 20
    filterset_class = InventarioFilter

    
class Create(CreateView):
    model = Inventario
    template_name = "exampleInventario/create.html"
    form_class = InventarioForm
    success_url = reverse_lazy('exampleInventario:index')

class Edit(UpdateView):
    model = Inventario
    template_name = "exampleInventario/edit.html"
    form_class = InventarioForm
    success_url = reverse_lazy('exampleInventario:index') 

class Delete(DeleteView):
    model = Inventario
    success_url = reverse_lazy('exampleInventario:index')