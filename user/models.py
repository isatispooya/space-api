from django.db import models

class Gender(models.TextChoices):
    MALE = 'M', 'مرد'
    FEMALE = 'F', 'زن'
    OTHER = 'O', 'دیگر'


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=11)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True) 
    last_login = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True)
    national_id = models.CharField(max_length=10)
    chat_id_telegram = models.CharField(max_length=255, null=True, blank=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    login_attempts = models.IntegerField(default=0) 
    seri_shenasname = models.CharField(max_length=10, null=True, blank=True)
    seri_shenasname_char = models.CharField(max_length=10, null=True, blank=True)
    serial_shenasname = models.CharField(max_length=10, null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    place_of_issue = models.CharField(max_length=255, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)

    EDUCATION_LEVELS = [
    ('highschool', 'دیپلم'),
    ('bachelor', 'کارشناسی'),
    ('master', 'کارشناسی ارشد'),
    ('phd', 'دکترا'),
    ]
    education_level = models.CharField(max_length=15, choices=EDUCATION_LEVELS, blank=True, null=True) 
    MARITAL_STATUS = [
    ('single', 'مجرد'),
    ('married', 'متاهل'),
    ]
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, blank=True, null=True)


    def __str__(self):
        return self.username


class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10)
    bank = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=10)
    branch_name = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    sheba_number = models.CharField(max_length=24)


    def __str__(self):
        return self.user.username


class Addresses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=100, verbose_name='کشور')
    country_prefix = models.CharField(max_length=10, verbose_name='پیش شماره کشور', null=True, blank=True)
    province = models.CharField(max_length=100, verbose_name='استان')
    city = models.CharField(max_length=100, verbose_name='شهر')
    city_prefix = models.CharField(max_length=10, verbose_name='پیش شماره شهر', null=True, blank=True)
    section = models.CharField(max_length=100, verbose_name='بخش')
    remnant_address = models.TextField(verbose_name='ادامه آدرس')
    alley = models.CharField(max_length=100, verbose_name='کوچه', null=True, blank=True)
    plaque = models.CharField(max_length=20, verbose_name='پلاک')
    postal_code = models.CharField(max_length=10, verbose_name='کد پستی')
    tel = models.CharField(max_length=20, verbose_name='تلفن ثابت', null=True, blank=True)
    emergency_tel = models.CharField(max_length=20, verbose_name='تلفن اضطراری', null=True, blank=True)
    emergency_tel_city_prefix = models.CharField(max_length=10, verbose_name='پیش شماره شهر تلفن اضطراری', null=True, blank=True)
    emergency_tel_country_prefix = models.CharField(max_length=10, verbose_name='پیش شماره کشور تلفن اضطراری', null=True, blank=True)
    fax = models.CharField(max_length=20, verbose_name='فکس', null=True, blank=True)
    fax_prefix = models.CharField(max_length=10, verbose_name='پیش شماره فکس', null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.city}"


class JobInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_infos')
    company_name = models.CharField(max_length=255, verbose_name='نام شرکت', null=True, blank=True)
    company_address = models.TextField(verbose_name='آدرس شرکت', null=True, blank=True)
    company_city_prefix = models.CharField(max_length=10, verbose_name='پیش شماره شهر شرکت', null=True, blank=True)
    company_phone = models.CharField(max_length=20, verbose_name='تلفن شرکت', null=True, blank=True)
    company_postal_code = models.CharField(max_length=10, verbose_name='کد پستی شرکت', null=True, blank=True)
    company_email = models.EmailField(verbose_name='ایمیل شرکت', null=True, blank=True)
    company_fax = models.CharField(max_length=20, verbose_name='فکس شرکت', null=True, blank=True)
    company_fax_prefix = models.CharField(max_length=10, verbose_name='پیش شماره فکس شرکت', null=True, blank=True)    
    job_title = models.CharField(max_length=255, verbose_name='عنوان شغل', null=True, blank=True)
    position = models.CharField(max_length=255, verbose_name='سمت', null=True, blank=True)
    job_description = models.TextField(verbose_name='شرح شغل', null=True, blank=True)
    employment_date = models.DateField(verbose_name='تاریخ استخدام', null=True, blank=True)
    is_current = models.BooleanField(default=True, verbose_name='شغل فعلی')

    class Meta:
        verbose_name = 'اطلاعات شغلی'
        verbose_name_plural = 'اطلاعات شغلی'

    def __str__(self):
        return f"{self.user.username} - {self.job_title or 'بدون عنوان شغلی'}"



