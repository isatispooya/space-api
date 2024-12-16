from django.db import models

class Announcement (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.FileField(upload_to='media/announcements/' , null=True , blank=True)
    link = models.CharField(max_length=500 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title


class ShortCut (models.Model):
    title = models.CharField(max_length=255)
    picture = models.FileField(upload_to='media/shortcuts/' , null=True , blank=True)
    link = models.CharField(max_length=500 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title
