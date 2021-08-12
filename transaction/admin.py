from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from transaction.models import *

# Register your models here.

admin.site.register(BranchMaster)
admin.site.register(DepartmentMaster)
admin.site.register(CompanyLedgerMaster)
admin.site.register(ArticleMaster)
admin.site.register(ColorMaster)
admin.site.register(InventoryItem)



class TransactionLineItemInline(admin.TabularInline):
    model = TransactionLineItem

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    inlines = [TransactionLineItemInline]


class InventoryItemInline(admin.TabularInline):
    model = InventoryItem

@admin.register(TransactionLineItem)
class TransactionLineItemAdmin(admin.ModelAdmin):
    inlines = [InventoryItemInline]