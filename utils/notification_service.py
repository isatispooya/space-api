import requests

class NotificationService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.notificationservice.com/v1"
    
