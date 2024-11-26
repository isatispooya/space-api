from django.db import models
from user.models import User
from positions.models import Position
import uuid
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

class Attache(models.Model):
    name = models.CharField(max_length=255, verbose_name="نام فایل")
    file = models.FileField(
        upload_to="attachments/%Y/%m/",  
        verbose_name="فایل",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="تاریخ ایجاد")
    class Meta:
        verbose_name = "پیوست"
        verbose_name_plural = "پیوست‌ها"
        indexes = [
            models.Index(fields=['created_at']),
        ]
        
    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class Correspondence (models.Model):
    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('sent', 'ارسال شده'),
        ('received', 'دریافت شده'),
        ('archived', 'بایگانی شده'),]
    
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT, 
        related_name='sent_correspondence',
        verbose_name="فرستنده",)
    
    receiver = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='received_correspondence',
        verbose_name="گیرنده",)
    
    subject = models.CharField(  
        max_length=255,
        blank = True,
        null= True,
        db_index=True,
        verbose_name="موضوع",)
    
    number = models.BigIntegerField(
        null=True,
        blank= True,
        db_index=True,
        verbose_name="شماره",)
    
    attachments = models.ForeignKey(
        Attache,
        null=True,
        blank = True,
        on_delete=models.CASCADE,
        verbose_name="پیوست",)
    
    text = models.TextField(
        blank = True,
        null = True,
        verbose_name="متن",)
    
    status = models.CharField( 
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True,
        verbose_name="وضعیت",)
    
    is_foreign = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="خارجی",)
    
    is_internal = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="داخلی",)
    
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
        verbose_name="شناسه یکتا",) 
       
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="تاریخ ایجاد",)
    
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="تاریخ به‌روزرسانی",)
    
    priority = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'عادی'),
            ('immediate', 'فوری'),
            ('very_immediate', 'خیلی فوری'),],
        default='normal',
        verbose_name="اولویت",)
    
    confidentiality_level = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'عادی'),
            ('confidential', 'محرمانه'),
            ('secret', 'سری'),
            ('top_secret', 'به کلی سری'),],
        default='normal',
        verbose_name="سطح محرمانگی",)
    
    class Meta:
        verbose_name = "مکاتبه"
        verbose_name_plural = "مکاتبات"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at', 'status']),
            models.Index(fields=['sender', 'receiver']),
        ]
    def __str__(self):
        return f"{self.number} - {self.subject} ({self.created_at:%Y-%m-%d})"
    


    


    