from .models import Announcement , ShortCut 
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from .serializers import AnnouncementSerializer , ShortCutSerializer 
from rest_framework.response import Response
from stock_affairs.permission import IsShareholder , IsPrecedence , IsUnusedPrecedencePurchase



class AnnouncementView(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class ShortCutView(viewsets.ModelViewSet):
    queryset = ShortCut.objects.all()
    serializer_class = ShortCutSerializer
    permission_classes = [AllowAny] 

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    


class MenuView(APIView):
    permission_classes = [IsAuthenticated]


    def menu_stock_affairs(self, request):
        main = {'title': 'امور سهام','path': '/stock_affairs'}
        sub_menu = []

        if IsShareholder().has_permission(request, self):
            sub_menu.append({'title': 'سهام','path': '/stock_affairs/stock'})

        if IsPrecedence().has_permission(request, self):
            sub_menu.append({'title': 'حق تقدم','path': '/stock_affairs/precedence'})

        if IsUnusedPrecedencePurchase().has_permission(request, self):
            sub_menu.append({'title': 'خرید حق تقدم استفاده نشده','path': '/stock_affairs/unused_precedence_purchase'})

        if len(sub_menu)>0:
            main['sub_menu'] = sub_menu
            return main
        else:
            return None

    def menu_correspondence(self, request):
        return {'title': 'مکاتبات', 'path': '/correspondence'}

    def get(self, request):
        self.menu_items = []
        # home
        home = {
            'title': 'خانه',
            'path': '/',
        }
        self.menu_items.append(home)
        # stock_affairs
        stock_affairs = self.menu_stock_affairs(request)
        if stock_affairs:
            self.menu_items.append(stock_affairs)



        return Response(self.menu_items)
    
    

        
