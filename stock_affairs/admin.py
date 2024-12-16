from django.contrib import admin
from .models import Shareholders, StockTransfer, DisplacementPrecedence, CapitalIncreasePayment , Precedence , UnusedPrecedencePurchase , UnusedPrecedenceProcess


admin.site.register(Shareholders)
admin.site.register(StockTransfer)
admin.site.register(DisplacementPrecedence)
admin.site.register(CapitalIncreasePayment)
admin.site.register(Precedence)
@admin.register(UnusedPrecedencePurchase)
class UnusedPrecedencePurchaseAdmin(admin.ModelAdmin):
    list_display = ['user'  , 'created_at' , 'status' , 'requested_amount' , 'price' , 'transaction_id' , 'amount']
    list_filter = ['created_at' , 'user'  , 'status']
    search_fields = ['user'  , 'status']
    list_per_page = 100
    ordering = ['-created_at']
    list_editable = ['status']
    list_display_links = ['user' ]
    list_select_related = ['user' ]
    fieldsets = [
        ('اطلاعات اصلی', {
            'fields': ['user'  , 'status']
        }),
        ('تاریخ‌ها', {
            'fields': ['created_at' , 'updated_at']
        }) , 
        ('مبالغ', {
            'fields': ['amount' , 'price' , 'requested_amount']
        }), 
        ('شناسه تراکنش', {
            'fields': ['transaction_id' , 'transaction_url']
        }) , 
        ('فیش خرید', {
            'fields': ['document']
        })
    ]

@admin.register(UnusedPrecedenceProcess)
class UnusedPrecedenceProcessAdmin(admin.ModelAdmin):
    list_display = ['company' , 'total_amount' , 'used_amount' , 'price' , 'end_date']
    list_filter = ['company' , 'end_date' , 'created_at']
    search_fields = ['company']
    list_per_page = 100
    ordering = ['-end_date']
    list_display_links = ['company']
    list_select_related = ['company']
    fieldsets = [
        ('اطلاعات اصلی', {
            'fields': ['company' , 'total_amount' , 'used_amount' , 'price']
        }),
        ('تاریخ‌ها', {
            'fields': ['end_date']
        })
    ]
