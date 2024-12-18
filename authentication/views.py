from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from GuardPyCaptcha.Captch import GuardPyCaptcha
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import Group 
from .serializer import GroupSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from timeflow.models import UserLoginLog
from rest_framework_simplejwt.exceptions import TokenError

class CaptchaViewset(APIView) :
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)

    
class GroupManagementViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            permissions = request.data.get('permissions', [])

            group = Group.objects.create(name=name)
            
            if permissions:
                group.permissions.set(permissions)
            serializer = self.get_serializer(group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            name = request.data.get('name')
            permissions = request.data.get('permissions', [])

            if name:
                instance.name = name
            
            if permissions:
                instance.permissions.set(permissions)
            
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        

User = get_user_model()
class UserToGroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    
    def assign_group(self, request):
        try:
            user_id = request.data.get('user_id')
            group_ids = request.data.get('groups', [])
            
            user = User.objects.get(id=user_id)
            
            user.groups.set(group_ids)
            
            return Response({
                'message': 'کاربر با موفقیت به گروه‌ها اضافه شد',
                'user': user.username,
                'groups': list(user.groups.values_list('name', flat=True))
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'کاربر مورد نظر یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "refresh_token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # تبدیل رشته به شیء RefreshToken
                token = RefreshToken(refresh_token)
                # بلک‌لیست کردن توکن
                token.blacklist()
            except TokenError as e:
                return Response(
                    {"error": f"Invalid token: {str(e)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            UserLoginLog.objects.create(
                user=request.user,
                type='logout',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            return Response(
                {"detail": "Successfully logged out"}, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        



      
            

           
            
 