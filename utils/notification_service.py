import requests
from typing import Optional
import os


class NotificationService:
    def __init__(self, email_config: Optional[dict] = None):
        # استفاده از کانفیگ پیش‌فرض
        self.sms_config = {
            'from': os.getenv('SMS_FROM'),
            'username': os.getenv('SMS_USERNAME'),
            'password': os.getenv('SMS_PASSWORD'),
            'url': os.getenv('SMS_URL')
        }

        self.email_config = email_config

    def send_sms(self, to: str, message: str, template: Optional[str] = None) -> dict:
        """
        ارسال پیامک با متن و گیرنده دلخواه
        
        :param to: شماره گیرنده
        :param message: متن پیام
        :param template: قالب پیام (اختیاری)
        :return: پاسخ API
        """
        if template:
            message = self._apply_template(template, message)
            
        params = {
            'from': self.sms_from,
            'to': to,
            'username': self.sms_username,
            'password': self.sms_password,
            'message': message
        }
        
        response = requests.get(url=self.sms_url, params=params)
        return response.json()
    
    def _apply_template(self, template: str, message: str) -> str:
        """
        اعمال قالب روی متن پیام
        """
        templates = {
            'password_reset': f'اتوماسیون اداری ایساتیس پویا\n فراموشی رمز عبور\n کد: {message}',
            'set_password': f'اتوماسیون اداری ایساتیس پویا\nرمز عبور شما :\n{message}',
            'notification': f'اتوماسیون اداری ایساتیس پویا\n {message}',
        }
        return templates.get(template, message)

    def send_email(self, to: str, subject: str, body: str):
        """
        برای پیاده‌سازی در آینده
        """
        pass

