from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Inventario
# Register your models here.

admin.site.register(Inventario, SimpleHistoryAdmin)