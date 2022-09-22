from django.shortcuts import render, redirect

from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

from ..users.models import User
from ..examplePurchases.models import InventoryPurchase, Purchase
from ..exampleInventario.models import Inventario
# Create your views here.


class IndexView(PermissionRequiredMixin, TemplateView):
    permission_required = 'history.view_history'
    template_name = "history/logs.html"
    

# App 'Users'
class UserLogsView(PermissionRequiredMixin, ListView):
    permission_required = 'history.view_history'
    model = User
    template_name = "history/users.html"
    context_object_name = 'history'
    paginate_by = 20
    queryset = User.history.all()
    
    
class UserRollbackView(PermissionRequiredMixin, View):
    permission_required = 'history.change_history'
    model = User
    success_url = reverse_lazy('history:users')
    
    def post(self, request, pk, *args, **kwargs):
        history = self.model.history.get(pk=pk)
        history.save()
        return redirect(self.success_url)


# App 'Purchases'
class PurchasesLogsView(PermissionRequiredMixin, ListView):
    permission_required = 'history.view_history'
    model = Purchase
    template_name = "history/purchases.html"
    context_object_name = 'history'
    paginate_by = 20
    queryset = Purchase.history.all()
    
    
class PurchasesRollbackView(PermissionRequiredMixin, View):
    permission_required = 'history.change_history'
    model = Purchase
    success_url = reverse_lazy('history:purchases')
    
    def post(self, request, pk, *args, **kwargs):
        history = self.model.history.get(pk=pk)
        history.save()
        return redirect(self.success_url)


# App 'Inventario'
class InventoriesLogsView(PermissionRequiredMixin, ListView):
    permission_required = 'history.view_history'
    model = Inventario
    template_name = "history/inventories.html"
    context_object_name = 'history'
    paginate_by = 20
    queryset = Purchase.history.all()
    
    
class InventoriesRollbackView(PermissionRequiredMixin, View):
    permission_required = 'history.change_history'
    model = Inventario
    success_url = reverse_lazy('history:inventories')
    
    def post(self, request, pk, *args, **kwargs):
        history = self.model.history.get(pk=pk)
        history.save()
        return redirect(self.success_url)
