from django.contrib import admin
from .models import Shareholders, StockTransfer, DisplacementPrecedence, CapitalIncreasePayment , Precedence , Underwriting , UnusedPrecedenceProcess


admin.site.register(Shareholders)
admin.site.register(StockTransfer)
admin.site.register(DisplacementPrecedence)
admin.site.register(CapitalIncreasePayment)
admin.site.register(Precedence)
admin.site.register(Underwriting)
admin.site.register(UnusedPrecedenceProcess)

