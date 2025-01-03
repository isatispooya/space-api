import requests
from typing import Optional
import os


class NotificationService:
    def __init__(self, email_config: Optional[dict] = None):
        # استفاده از کانفیگ پیش‌فرض
        self.sms_config = {
            'from': os.getenv('SMS_FROM' , '30001526'),
            'username': os.getenv('SMS_USERNAME' , 'isatispooya'),
            'password': os.getenv('SMS_PASSWORD' , '5246043adeleh'),
            'url': os.getenv('SMS_URL' , 'http://tsms.ir/url/tsmshttp.php')
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
            'from': self.sms_config['from'],
            'to': to,
            'username': self.sms_config['username'],
            'password': self.sms_config['password'],
            'message': message
        }
        try:
            response = requests.get(url=self.sms_config['url'], params=params)
            response.raise_for_status()  # بررسی خطاهای HTTP
            return response.json()
        except requests.RequestException as e:
            print(e)
            return {
                'success': False,
                'error': str(e)
            }
    
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

