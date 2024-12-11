from django.urls import path , include 
from rest_framework.routers import DefaultRouter
from .views import ShareholdersViewset , StockTransferViewset , PrecedenceViewset , CapitalIncreasePaymentViewset , DisplacementPrecedenceViewset

router = DefaultRouter()
router.register('shareholders', ShareholdersViewset)
router.register('stock_transfer', StockTransferViewset)
router.register('precedence', PrecedenceViewset)
router.register('capital_increase_payment', CapitalIncreasePaymentViewset)
router.register('displacement_precedence', DisplacementPrecedenceViewset)
urlpatterns = router.urls



