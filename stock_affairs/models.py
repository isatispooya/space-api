from django.db import models
from positions.models import Position
from companies.models import Company
from django.utils import timezone


class Shareholders(models.Model):
    name = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE,
        verbose_name="نام سهامدار"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    number_of_shares = models.BigIntegerField(verbose_name="تعداد سهام")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاریخ ایجاد"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی"
    )

    class Meta:
        verbose_name = "سهامدار"
        verbose_name_plural = "سهامداران"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.company}"


class StockTransfer(models.Model):
    seller = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='stock_sales',
        verbose_name="فروشنده"
    )
    buyer = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='stock_purchases',
        verbose_name="خریدار"
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


class Precedence(models.Model):
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    precedence = models.BigIntegerField(verbose_name="حق تقدم")
    used_precedence = models.BigIntegerField(verbose_name="حق تقدم استفاده شده")
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
        return f"{self.position} - {self.company}"


class CapitalIncreasePayment(models.Model):
    document = models.FileField(
        upload_to='stock_affairs/documents/',
        verbose_name="سند"
    )
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        verbose_name="شرکت"
    )
    number_of_shares = models.BigIntegerField(verbose_name="تعداد سهام")
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
        verbose_name = "پرداخت افزایش سرمایه"
        verbose_name_plural = "پرداخت‌های افزایش سرمایه"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.position} - {self.company}"


class DisplacementPrecedence(models.Model):
    seller = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='precedence_sales',
        verbose_name="فروشنده"
    )
    buyer = models.ForeignKey(
        Position, 
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


