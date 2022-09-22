from django.db import models
from simple_history.models import HistoricalRecords
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Inventario(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    nombre = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ['-id']      # Orders by Id ("-" means descending)



