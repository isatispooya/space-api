from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class InvitationCode(models.Model):
    code = models.CharField(
        max_length=6,
        unique=True,
        blank=True,
        null=True,
        verbose_name='کد دعوت'
    )
    introducer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invitation_codes'
    )
    description = models.TextField(
        verbose_name='توضیحات',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )
    class Meta:
        verbose_name = 'کد دعوت'
        verbose_name_plural = 'کد های دعوت'

    def __str__(self):
        return self.code


class Invitation(models.Model):
    invitation_code = models.ForeignKey(
        InvitationCode,
        on_delete=models.CASCADE,
        verbose_name='کد دعوت'
    )
    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاریخ بروزرسانی'
    )
    class Meta:
        verbose_name = 'دعوت'
        verbose_name_plural = 'دعوت ها' 
    
    def __str__(self):
        return f'{self.invited_user.username} - {self.invitation_code.code}'


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='کاربر'
    )
    title = models.CharField(max_length=255, verbose_name='عنوان')
    tag = models.CharField(max_length=255, verbose_name='تگ',blank=True,null=True)
    message = models.TextField(verbose_name='متن')
    read = models.BooleanField(default=False, verbose_name='خوانده شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان ها'

    def __str__(self):
        return self.title

