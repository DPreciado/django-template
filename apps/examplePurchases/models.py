from datetime import datetime
from django.db import models
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Purchase(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    total_price = models.CharField(max_length=255)
    description = models.CharField(max_length=65535)
    date = models.DateField(default=datetime.now)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Purchase"    
        verbose_name_plural = "Purchases"
        db_table = "purchase"
        ordering = ['-id']      # Orders by Id ("-" means descending)



class InventoryPurchase(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    inventory = models.ForeignKey('exampleInventario.Inventario', on_delete = models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete = models.CASCADE)
    price = models.CharField(max_length=10)
    supplier = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=255, default='entry')
    history = HistoricalRecords()

    class Meta:
        verbose_name = "InventoryPurchase"    
        verbose_name_plural = "InventoryPurchases"
        db_table = "inventory_purchases"
        ordering = ['-id']      # Orders by Id ("-" means descending)

