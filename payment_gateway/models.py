from django.db import models
from companies.models import Company

class PaymentGateway(models.Model):
    name = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True ,
        verbose_name="نام درگاه"
    )
    description = models.TextField(
        null=True , 
        blank=True ,
        verbose_name="توضیحات"
    )
    base_url = models.CharField(max_length=500 , null=True , blank=True)
    redirect_url = models.CharField(
        max_length=500 , 
        null=True , 
        blank=True ,
        verbose_name="آدرس هدایت"
    )
    username  = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True ,
        verbose_name="نام کاربری"
    )
    password = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True ,
        verbose_name="رمز عبور"
    )
    terminal_number = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True ,
        verbose_name="شماره ترمینال"
    )
    company = models.ForeignKey(
        Company , 
        on_delete=models.CASCADE , 
        null=True , 
        blank=True ,
        verbose_name="شرکت"
    )
    card_number = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True ,
        verbose_name="شماره کارت"
    )
    is_active = models.BooleanField(
        default=True ,
        verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(
        auto_now_add=True ,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True ,
        verbose_name="تاریخ بروزرسانی"
    )
    
    class Meta:
        verbose_name = "درگاه پرداخت"
        verbose_name_plural = "درگاه پرداخت"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name}"


