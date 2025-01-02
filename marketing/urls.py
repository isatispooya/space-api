from django.urls import path, include
from .views import InvitationCodeView, InvitationView

urlpatterns = [
    path('invitation-code/', InvitationCodeView.as_view(), name='invitation-code'),
    path('invitation/', InvitationView.as_view(), name='invitation'),
]