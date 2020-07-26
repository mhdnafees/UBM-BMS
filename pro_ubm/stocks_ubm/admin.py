from django.contrib import admin
from .models import Stock,SalesRegistry,PurchaseRegistry,ProfitGen,InvoiceGen

# Register your models here.
admin.site.register(Stock)
admin.site.register(SalesRegistry)
admin.site.register(PurchaseRegistry)
admin.site.register(ProfitGen)
admin.site.register(InvoiceGen)
