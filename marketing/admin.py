from django.contrib import admin
from .models import Invitation, InvitationCode

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ['invitation_code', 'invited_user']
    readonly_fields = ['created_at']

@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'introducer_user', 'description']
    
