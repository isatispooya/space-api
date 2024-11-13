from django.db import models
from companies.models import Company
from user.models import User
class Position(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_positions')
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True)
    type_of_employment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {str(self.user)}"