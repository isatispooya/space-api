from django.db import models
from user.models import User
from positions.models import Position
import uuid
from django.contrib.auth import get_user_model


class Attache(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="attaches/")
    
    def __str__(self):
        return self.name

class Correspondence (models.Model):
    sender = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='sent_correspondence')
    receiver = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='received_correspondence')
    subject = models.TextField(blank = True , null= True)
    date = models.DateTimeField(auto_now = True)
    number = models.IntegerField(null=True , blank= True)
    attache = models.ForeignKey(Attache, on_delete=models.CASCADE, null=True, blank = True)
    text = models.TextField(blank = True , null = True)
    foreigner = models.BooleanField(default=False)
    internal = models.BooleanField(default=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return f"{self.subject} - {self.date}"
    


    


    