from django.db import models
from positions.models import Position
from companies.models import Company


# سهامداران
class Shareholders(models.Model):
    name = models.ForeignKey(Position, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    number_of_shares = models.BigIntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()


# جابجایی سهام
class StockTransfer(models.Model):
    seller = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='stock_sales')
    buyer = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='stock_purchases')
    number_of_shares = models.BigIntegerField()
    document = models.FileField(upload_to='media/stock_affairs/document/',null=True, blank=True)
    price = models.BigIntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()


# حق تقدم
class Precedence(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    precedence = models.BigIntegerField()
    used_precedence = models.BigIntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()


# پرداخت حق تقدم
class CapitalIncreasePayment(models.Model):
    document = models.FileField(upload_to='media/stock_affairs/document/')
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    number_of_shares = models.BigIntegerField()
    price = models.BigIntegerField()
    created_at = models.DateField()
    updated_at = models.DateField()


# جابجایی حق تقدم
class DisplacementPrecedence(models.Model):
    seller = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='precedence_sales')
    buyer = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='precedence_purchases')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    number_of_shares = models.BigIntegerField()
    price = models.BigIntegerField()
    document = models.FileField(upload_to='media/stock_affairs/document/',null=True, blank=True)
    created_at = models.DateField()
    updated_at = models.DateField()


