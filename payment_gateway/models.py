from django.db import models

class PaymentGateway(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    base_url = models.CharField(max_length=500)
    username  = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    terminal_number = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "درگاه پرداخت"
        verbose_name_plural = "درگاه پرداخت"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name}"


