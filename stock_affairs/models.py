from django.db import models
from companies.models import Company
from django.utils import timezone
from user.models import User
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from payment_gateway.models import PaymentGateway


class Shareholders(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="نام سهامدار"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    number_of_shares = models.PositiveBigIntegerField(verbose_name="تعداد سهام")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "سهامدار"
        verbose_name_plural = "سهامداران"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.company}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if Shareholders.objects.filter(user=self.user, company=self.company).exists():
            raise ValidationError({
                "error": "این کاربر قبلاً در این شرکت به عنوان سهامدار ثبت شده است"
            })


class StockTransfer(models.Model):
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='stock_sales',
        verbose_name="فروشنده"
    )
    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='stock_purchases',
        verbose_name="خریدار"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    number_of_shares = models.BigIntegerField(verbose_name="تعداد سهام")
    document = models.FileField(
        upload_to='stock_affairs/documents/',
        null=True, 
        blank=True,
        verbose_name="سند"
    )
    price = models.BigIntegerField(verbose_name="قیمت")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "انتقال سهام"
        verbose_name_plural = "انتقال‌های سهام"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]
    def __str__(self):
        return f"{self.seller} - {self.buyer} - {self.company}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.seller == self.buyer:
            raise ValidationError({
                "error": "فروشنده و خریدار نمی‌توانند یک شخص باشند"
            })


class Precedence(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    precedence = models.BigIntegerField(verbose_name="حق تقدم")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "حق تقدم"
        verbose_name_plural = "حق تقدم‌ها"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.company}"
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if Precedence.objects.filter(user=self.user, company=self.company).exists():
            raise ValidationError({
                "error": "شما قبلا حق تقدم در این شرکت ثبت کرده اید"
            })
    


class CapitalIncreasePayment(models.Model):
    document = models.FileField(
        upload_to='stock_affairs/documents/',
        verbose_name="سند"
    )
    precedence = models.ForeignKey(
        Precedence, 
        on_delete=models.CASCADE,
        verbose_name="حق تقدم"
    )
    amount = models.BigIntegerField(verbose_name="مقدار")
    value = models.BigIntegerField(verbose_name="قیمت")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )
    class Meta:
        verbose_name = "پرداخت حق تقدم"
        verbose_name_plural = "پرداخت‌های حق تقدم"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.precedence}"


class DisplacementPrecedence(models.Model):
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='precedence_sales',
        verbose_name="فروشنده"
    )
    buyer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='precedence_purchases',
        verbose_name="خریدار"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    number_of_shares = models.BigIntegerField(verbose_name="تعداد سهام")
    price = models.BigIntegerField(verbose_name="قیمت")
    document = models.FileField(
        upload_to='stock_affairs/documents/',
        null=True, 
        blank=True,
        verbose_name="سند"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "انتقال حق تقدم"
        verbose_name_plural = "انتقال‌های حق تقدم"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.seller} - {self.buyer} - {self.company}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self.seller == self.buyer:
            raise ValidationError({
                "error": "فروشنده و خریدار نمی‌توانند یک شخص باشند"
            })


class UnusedPrecedenceProcess(models.Model):
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    total_amount = models.BigIntegerField(
        verbose_name=" مقدار کل"
    )
    used_amount = models.BigIntegerField(
        verbose_name=" مقدار موجود"
    )
    price = models.BigIntegerField(
        verbose_name="قیمت"
    )
    description = models.TextField(
        null=True , 
        blank=True , 
        verbose_name="توضیحات"
    )
    agreement = models.BooleanField(
        default=True , 
        verbose_name="موافقت نامه"
    )
    payment_gateway = models.ForeignKey(
        PaymentGateway , 
        on_delete=models.CASCADE , 
        null=True , 
        blank=True , 
        verbose_name="درگاه پرداخت"
    )
    is_active = models.BooleanField(
        default=True , 
        verbose_name="فعال"
    )
    end_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ اتمام "
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )
    class Meta:
        verbose_name = "ایجاد فرایند خرید حق تقدم استفاده نشده"
        verbose_name_plural = "فرایند خرید حق تقدم استفاده نشده"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.company}"

    
class UnusedPrecedencePurchase(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    requested_amount = models.BigIntegerField(
        null=True ,
        blank=True,
        verbose_name="مقدار درخواست شده"
    )
    type = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True , 
        choices=[('1' , '1') , ('2' , '2')],
        # 1 : فیش
        # 2 : درگاه پرداخت
        verbose_name="نوع"
    )
    price = models.BigIntegerField(
        null=True , 
        blank=True,
        verbose_name="قیمت"
    )
    process = models.ForeignKey(
        UnusedPrecedenceProcess, 
        on_delete=models.CASCADE, 
        verbose_name="فرایند"
    )
    document = models.FileField(
        upload_to='stock_affairs/documents/' , 
        null=True , 
        blank=True, 
        verbose_name="تصویر فیش"
    )
    invoice_unique_id = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="شماره فاکتور"
    )
    error_code = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="کد خطا"
    )
    error = models.TextField(
        null=True , 
        blank=True,
        verbose_name="خطا"
    )
    payment_gateway = models.ForeignKey(
        PaymentGateway , 
        on_delete=models.CASCADE , 
        null=True , 
        blank=True , 
        verbose_name="درگاه پرداخت"
    )
    transaction_url = models.CharField(
        max_length=500 , 
        null=True , 
        blank=True,
        verbose_name="آدرس تراکنش"
    )
    verify_transaction = models.BooleanField(
        default=False,
        verbose_name="تراکنش بررسی شده"
    )
    code_payment = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="کد پرداخت"
    )
    refrence_number = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="شماره پیگیری شاپرک"
    )
    code_state_payment = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="کد وضعیت پرداخت"
    )
    cart_number = models.CharField(
        max_length=255 ,  
        null=True , 
        blank=True,
        verbose_name="شماره کارت"
    )
    hashed_cart_number = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="شماره کارت به فرمت هش شده"
    )
    referal_number = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="شماره مرجع"
    )
    track_id = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True,
        verbose_name="شناسه تراکنش"
    )
    status = models.CharField(
        max_length=255 , 
        null=True , 
        blank=True , 
        choices=[('pending' , 'درحال بررسی') , ('approved' , 'تایید شده') , ('rejected' , 'رد شده')] , 
        verbose_name="وضعیت"
    )
    description = models.TextField(
        null=True , 
        blank=True , 
        verbose_name="توضیحات"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )
    
    class Meta:
        verbose_name = "خرید حق تقدم استفاده نشده"
        verbose_name_plural = "خرید حق تقدم استفاده نشده"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user}"



