from django.contrib import admin
from .models import Announcement , ShortCut 

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title' , 'link' , 'is_active']
    list_filter = ['created_at' , 'is_active', 'title']
    search_fields = ['title']   
    fieldsets = [
        ('اطلاعات اصلی', {
            'fields': ['title' , 'description' , 'picture' , 'link' , 'is_active']
        }),
        ('تاریخ‌ها', {
            'fields': ['created_at' , 'updated_at']
        })
    ]


@admin.register(ShortCut)
class ShortCutAdmin(admin.ModelAdmin):
    list_display = ['title' , 'link' , 'is_active']
    list_filter = ['created_at' , 'is_active', 'title']
    search_fields = ['title']
    fieldsets = [
        ('اطلاعات اصلی', {
            'fields': ['title' , 'link' , 'is_active']
        }),
        ('تاریخ‌ها', {
            'fields': ['created_at' , 'updated_at']
        })
    ]