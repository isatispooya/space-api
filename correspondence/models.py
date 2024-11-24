from django.db import models
from user.models import User
from positions.models import Position


class Correspondence (models.Model):
    sender = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="correspondences_sent")
    internal_receiver= models.ForeignKey(Position, on_delete=models.CASCADE, related_name="correspondences_received_internal")
    foreigner_receiver= models.ForeignKey(User, on_delete=models.CASCADE, related_name="correspondences_received_foreigner")
    subject = models.TextField(blank = True , null= True)
    date = models.DateTimeField(auto_now = True)
    number = models.IntegerField(null=True , blank= True)
    attache = models.IntegerField(null=True, blank = True)
    text = models.TextField(blank = True , null = True)
    foreigner = models.BooleanField(default=False)
    internal = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.subject} - {self.date}"