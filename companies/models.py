from django.db import models



class Company(models.Model):
    name = models.CharField(max_length=255 , verbose_name="نام شرکت")
    description = models.TextField(verbose_name="توضیحات")
    address = models.TextField(verbose_name="آدرس")

    phone = models.CharField(max_length=20,verbose_name="تلفن")
    email = models.EmailField(verbose_name="ایمیل")
    website = models.URLField(verbose_name="وب سایت")

    postal_code = models.CharField(
        max_length=15,
        null=True,
        blank = True,
        verbose_name="کد پستی")
    
    national_id = models.CharField(
        max_length=20,
        verbose_name="شناسه ملی")
    
    year_of_establishment = models.PositiveSmallIntegerField(verbose_name="سال تاسیس")
    registration_number = models.PositiveIntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name="شماره ثبت")
    
    registered_capital = models.BigIntegerField(
            null=True,
            blank=True ,
            verbose_name="سرمایه ثبتی",
            help_text="مقدار به ریال وارد شود")
    
    
    type_of_activity = models.CharField(
        max_length=255,
        verbose_name="نوع فعالیت")
    
    company_type = models.CharField(max_length=100,
        verbose_name="نوع شرکت",
        choices=[
            ('private', 'سهامی خاص'),
            ('public', 'سهامی عام'),
            ('limited', 'مسئولیت محدود'),
            ('cooperative', 'تضامنی'),
            ('mixed', 'مختلط غیر سهامی'),
            ('mixed_stock', 'مختلط سهامی'),
            ('proportional', 'نسبی'),
            ('production_coop', 'تعاونی تولید و مصرف'),
        ])
    
    logo = models.FileField(
        upload_to='logo/company/',
        null=True, blank=True,
        verbose_name="لوگو")
    
    class Meta:
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت ها"
        indexes = [
            models.Index(fields=['national_id']),
        ]

    def __str__(self):
        return self.name

