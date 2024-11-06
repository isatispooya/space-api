from django.db import models



class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    logo = models.FileField(upload_to='company_logos/', null=True, blank=True)
    national_id = models.CharField(max_length=20)
    type_of_activity = models.CharField(max_length=255)
    year_of_establishment = models.IntegerField()

    def __str__(self):
        return self.name

