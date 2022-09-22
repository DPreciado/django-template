from django.views.generic.list import ListView
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django_filters.views import FilterView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.db import transaction
from django.core.exceptions import ValidationError

from ..exampleInventario.models import Inventario
from .forms import PurchaseForm, Purchase
from .models import InventoryPurchase
from .filters import PurchaseFilter


# Index
class Index(FilterView):
    model = Purchase
    template_name = "examplePurchases/index.html"
    context_object_name = 'purchases'
    paginate_by = 20
    filterset_class = PurchaseFilter


# Create
class Create(CreateView):
    model = Purchase
    template_name = "examplePurchases/create.html"
    form_class = PurchaseForm
    success_url = reverse_lazy('examplePurchases:index')
    
    # Override the context that is passed to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventario'] = Inventario.objects.all()
        return context
    
    def form_invalid(self, form):
        return super(CreateView, self).form_invalid(form)

    # Override the save method that Django uses to store the form's POST data.
    @transaction.atomic
    def post(self, request):

        # Get the Purchase's Form data sent through the POST
        form = PurchaseForm(request.POST)


        # Check if the data in our form is valid before saving the data
        if form.is_valid():
        
            # save current point of database
            sid = transaction.savepoint()

            # Create the purchase and save it in a variable for later use as a ForeignKey
            purchase = form.save()



            # Loop through the POST data to get the id of each N item in a dict of our own
            product_keys = {}
            product_count = 0
            for key in request.POST :
                # If input name matches, we store the id as a value in our dict
                if key.find("product_name_") != -1:
                    product_keys[product_count] = key.split("_")[2]
                    product_count += 1

            # Now we iterate our dictionary with the ID values to get each form field sent
            for id in product_keys.values():

                if request.POST.get('product_name_' + str(id)) is None:
                    break

                product = request.POST.__getitem__('product_name_' + str(id))
                quantity = request.POST.__getitem__('quantity_' + str(id))
                price = request.POST.__getitem__('price_' + str(id))

                # CHECK IF THE PRODUCT NAME IS A NUMBER IF IT IS A NUMBER, THEN IT IS A PRODUCT ID
                if product.isdigit():
                    # Link the product to the current Purchase
                    InventoryPurchase.objects.create(
                        inventory = Inventario.objects.get(id=product),
                        purchase = purchase,
                        price = price,
                        supplier = "",
                        quantity = quantity,
                        transaction_type = "storage",
                    )
                # IF IT IS NOT A NUMBER, THEN IT IS A PRODUCT NAME AND WE NEED TO CREATE A NEW PRODUCT
                else:
                    inventory_name = product

                    # Try to get the product with the same SKU
                    if Inventario.objects.filter(sku=request.POST.__getitem__('sku_' + str(id))).exists():
                    # If the product exists it return a error
                        msg = "One SKU already exits. Please enter a different SKU"
                        form.add_error(None, msg)

                        # send error messages in context
                        context = {'form': form}
                        context['inventario'] = Inventario.objects.all()

                        # Rollback the database to the previous state
                        transaction.savepoint_rollback(sid)

                        # Return the form with the error message
                        return render(request, self.template_name, context)


                    #If not exist continue with the creation of the product
                    inventory = Inventario.objects.create(
                        nombre = inventory_name,
                        sku = request.POST.__getitem__('sku_' + str(id))
                    )

                    # Link the product to the current Purchase
                    InventoryPurchase.objects.create(
                        inventory = inventory,
                        purchase = purchase,
                        price = price,
                        supplier = "",
                        quantity = quantity,
                        transaction_type = "storage",
                    )
            # If everything is ok, commit the changes to the database
            transaction.savepoint_commit(sid)
            
            return redirect(self.success_url)
        
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


# Show
class Show(DetailView):
    model = Purchase
    template_name = "examplePurchases/showPurchase.html"
    context_object_name = 'purchase'

    # Override the context that is passed to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current id of the puchase
        id_purchase = self.kwargs['pk']

        # With filter we will get the products related to our current purchase 
        # NOTE: to acces the inventory fields we must first access the model's foreign key (in the template)
        context['inventario'] = InventoryPurchase.objects.filter(purchase_id = id_purchase)
        return context


# Edit
class Edit(UpdateView):
    model = Purchase
    template_name = "examplePurchases/edit.html"
    form_class = PurchaseForm
    success_url = reverse_lazy('examplePurchases:index')

    # Override the context that is passed to the template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the current id of the puchase
        id_purchase = self.kwargs['pk']

        # With filter we will get the products related to our current purchase 
        # NOTE: to access the inventory fields we must first access the model's foreign key (in the template)
        context['inventario'] = InventoryPurchase.objects.filter(purchase_id = id_purchase)
        context['all_products'] = Inventario.objects.all()
        return context
        

    # Override the save method that Django uses to store the form's POST data.
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        # Get the Purchase's Form data sent through the POST
        form = PurchaseForm(request.POST, instance = self.get_object())

        # Check if the data in our form is valid before saving the data
        if form.is_valid():

            # save current point of database
            sid = transaction.savepoint()

            # We edit the purchase entity and save it in a variable for later use as a ForeignKey
            purchase = form.save()
            
            # Now we erase all products from the current purchase to then add the new ones.
            InventoryPurchase.objects.filter(purchase_id = purchase.id).delete()

            # Loop through the POST data to get the id of each N item in a dict of our own
            product_keys = {}
            product_count = 0
            for key in request.POST :
                # If input name matches, we store the id as a value in our dict
                if key.find("product_name_") != -1:
                    product_keys[product_count] = key.split("_")[2]
                    product_count += 1

            # Now we iterate our dictionary with the ID values to get each form field sent
            for id in product_keys.values():

                if request.POST.get('product_name_' + str(id)) is None:
                    break

                product = request.POST.__getitem__('product_name_' + str(id))
                quantity = request.POST.__getitem__('quantity_' + str(id))
                price = request.POST.__getitem__('price_' + str(id))

                # CHECK IF THE PRODUCT NAME IS A NUMBER IF IT IS A NUMBER, THEN IT IS A PRODUCT ID
                if product.isdigit():
                    # Link the product to the current Purchase
                    InventoryPurchase.objects.create(
                        inventory = Inventario.objects.get(id=product),
                        purchase = purchase,
                        price = price,
                        supplier = "",
                        quantity = quantity,
                        transaction_type = "storage",
                    )
                # IF IT IS NOT A NUMBER, THEN IT IS A PRODUCT NAME AND WE NEED TO CREATE A NEW PRODUCT
                else:
                    inventory_name = product

                    # Try to get the product with the same SKU
                    if Inventario.objects.filter(sku=request.POST.__getitem__('sku_' + str(id))).exists():
                    # If the product exists it return a error
                        msg = "One SKU already exits. Please enter a different SKU"
                        form.add_error(None, msg)

                        # send error messages in context
                        context = {'form': form}
                        
                        # Get the current id of the puchase
                        id_purchase = self.kwargs['pk']

                        context['inventario'] = InventoryPurchase.objects.filter(purchase_id = id_purchase)
                        context['all_products'] = Inventario.objects.all()

                        # Rollback the database to the previous state
                        transaction.savepoint_rollback(sid)

                        # Return the form with the error message
                        return render(request, self.template_name, context)

                    # Create inventory product
                    inventory = Inventario.objects.create(
                        nombre = inventory_name,
                        sku = request.POST.__getitem__('sku_' + str(id))
                    )

                    # Link the product to the current Purchase
                    InventoryPurchase.objects.create(
                        inventory = inventory,
                        purchase = purchase,
                        price = price,
                        supplier = "",
                        quantity = quantity,
                        transaction_type = "storage",
                    )
                    
            # If everything is ok, commit the changes to the database
            transaction.savepoint_commit(sid)

            return redirect(self.success_url)
        else:
            # If the form is not valid, return the form with the errors.
            context = {'form': form}
            context['inventario'] = InventoryPurchase.objects.filter(purchase_id = self.get_object().id)
            context['all_products'] = Inventario.objects.all()

            return render(request, self.template_name, context)


# Delete the entity
class Delete(DeleteView):
    model = Purchase
    success_url = reverse_lazy('examplePurchases:index')


# Delete the N to N relationship between 2 entities (in a show view)
class DeleteRelation(DeleteView):
    model = InventoryPurchase

    def get_success_url(self):
        purchase_id = self.request.POST.get('purchase_id')
        return reverse('examplePurchases:show', kwargs={ 'pk': purchase_id })