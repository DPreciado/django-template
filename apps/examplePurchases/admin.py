from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Purchase, InventoryPurchase
# Register your models here.

admin.site.register(Purchase, SimpleHistoryAdmin)
admin.site.register(InventoryPurchase, SimpleHistoryAdmin)