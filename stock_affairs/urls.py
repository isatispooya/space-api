from django.urls import path , include 
from rest_framework.routers import DefaultRouter
from .views import ShareholdersViewset , StockTransferViewset ,PrecedenceViewset , CapitalIncreasePaymentViewset , DisplacementPrecedenceViewset , CreateUnusedPurchase , UnusedPrecedenceProcessViewset

router = DefaultRouter()
router.register('shareholders', ShareholdersViewset)
router.register('stock_transfer', StockTransferViewset)
router.register('precedence', PrecedenceViewset)
router.register('capital_increase_payment', CapitalIncreasePaymentViewset)
router.register('displacement_precedence', DisplacementPrecedenceViewset)
router.register('unused_precedence_process', UnusedPrecedenceProcessViewset)

urlpatterns = router.urls

urlpatterns += [
    path('create_unused_purchase/', CreateUnusedPurchase.as_view(), name='create-unused-purchase'),
    path('create_unused_purchase/<int:pk>/', CreateUnusedPurchase.as_view(), name='create-unused-purchase-detail'),
]



