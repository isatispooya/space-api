from django.shortcuts import render
from rest_framework import viewsets
from .models import Shareholders , StockTransfer , Precedence , CapitalIncreasePayment , DisplacementPrecedence , UnusedPrecedencePurchase , UnusedPrecedenceProcess
from rest_framework.permissions import IsAuthenticated , IsAdminUser 
from .serializers import ShareholdersSerializer , StockTransferSerializer , PrecedenceSerializer , CapitalIncreasePaymentSerializer , DisplacementPrecedenceSerializer , UnusedPrecedencePurchaseSerializer , UnusedPrecedenceProcessSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError
from stock_affairs.permission import IsShareholder , IsPrecedence , IsUnusedPrecedencePurchase , IsUnusedPrecedenceProcess
from django.db import transaction
from django.utils import timezone



class ShareholdersViewset(viewsets.ModelViewSet):
    queryset = Shareholders.objects.all()
    serializer_class = ShareholdersSerializer
    permission_classes = [IsAuthenticated , IsShareholder | IsAdminUser]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif not self.request.user.is_staff:
            self.queryset = Shareholders.objects.filter(user=self.request.user)
        return super().get_permissions()
    

class StockTransferViewset(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif not self.request.user.is_staff:
            self.queryset = StockTransfer.objects.filter(
                Q(buyer=self.request.user) | Q(seller=self.request.user)
            )
        return super().get_permissions()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # بررسی موجودی سهام فروشنده
        seller_shares = Shareholders.objects.filter(user=serializer.validated_data['seller'],company=serializer.validated_data['company']).first()
        
        if not seller_shares or seller_shares.number_of_shares < serializer.validated_data['number_of_shares']:
            raise ValidationError({"error": "تعداد سهام فروشنده کافی نیست"})

        # ذخیره انتقال سهام
        self.perform_create(serializer)
        
        # به‌روزرسانی سهام فروشنده
        seller_shares.number_of_shares -= serializer.validated_data['number_of_shares']
        seller_shares.save()
        
        # به‌روزرسانی یا ایجاد سهام خریدار
        buyer_shares = Shareholders.objects.filter(user=serializer.validated_data['buyer'],company=serializer.validated_data['company']).first()
        
        if buyer_shares:
            buyer_shares.number_of_shares += serializer.validated_data['number_of_shares']
            buyer_shares.save()
        else:
            Shareholders.objects.create(
                user=serializer.validated_data['buyer'],
                company=serializer.validated_data['company'],
                number_of_shares=serializer.validated_data['number_of_shares']
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                instance = self.get_object()
                old_number_of_shares = instance.number_of_shares
                
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                
                new_number_of_shares = serializer.validated_data.get('number_of_shares')
                
                if new_number_of_shares is None:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                difference = new_number_of_shares - old_number_of_shares
                
                if difference != 0:
                    seller_shares = Shareholders.objects.select_for_update().get(
                        user=instance.seller,
                        company=instance.company
                    )
                    
                    buyer_shares = Shareholders.objects.select_for_update().get(
                        user=instance.buyer,
                        company=instance.company
                    )
                    
                    if difference > 0:  # افزایش تعداد سهام
                        if seller_shares.number_of_shares < difference:
                            raise ValidationError({"error": "تعداد سهام فروشنده کافی نیست"})
                        seller_shares.number_of_shares -= difference
                        buyer_shares.number_of_shares += difference
                    else:  # کاهش تعداد سهام
                        seller_shares.number_of_shares += abs(difference)
                        buyer_shares.number_of_shares -= abs(difference)
                    
                    seller_shares.updated_at = timezone.now()
                    buyer_shares.updated_at = timezone.now()
                    seller_shares.save()
                    buyer_shares.save()
                    
                    instance.number_of_shares = new_number_of_shares
                    instance.updated_at = timezone.now()
                    instance.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            except Shareholders.DoesNotExist:
                return Response(
                    {"error": "سهامدار مورد نظر یافت نشد"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "شما اجازه ویرایش را ندارید"}, 
                status=status.HTTP_403_FORBIDDEN
            )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                instance = self.get_object()
                
                # بازگرداندن سهام به فروشنده و کم کردن از خریدار
                seller_shares = Shareholders.objects.select_for_update().get(
                    user=instance.seller,
                    company=instance.company
                )
                
                buyer_shares = Shareholders.objects.select_for_update().get(
                    user=instance.buyer,
                    company=instance.company
                )
                
                # برگرداندن سهام به فروشنده
                seller_shares.number_of_shares += instance.number_of_shares
                # کم کردن سهام از خریدار
                buyer_shares.number_of_shares -= instance.number_of_shares
                
                seller_shares.save()
                buyer_shares.save()
                
                # حذف رکورد انتقال سهام
                instance.delete()
                
                return Response(
                    {"message": "انتقال سهام با موفقیت حذف شد"}, 
                    status=status.HTTP_204_NO_CONTENT
                )
                
            except Shareholders.DoesNotExist:
                return Response(
                    {"error": "سهامدار مورد نظر یافت نشد"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "شما اجازه حذف را ندارید"}, 
                status=status.HTTP_403_FORBIDDEN
            )



class PrecedenceViewset(viewsets.ModelViewSet):
    queryset = Precedence.objects.all()
    serializer_class = PrecedenceSerializer
    permission_classes = [IsAuthenticated, IsPrecedence]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class CapitalIncreasePaymentViewset(viewsets.ModelViewSet):
    queryset = CapitalIncreasePayment.objects.all()
    serializer_class = CapitalIncreasePaymentSerializer
    permission_classes = [IsAuthenticated , IsPrecedence]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class DisplacementPrecedenceViewset(viewsets.ModelViewSet):
    queryset = DisplacementPrecedence.objects.all()
    serializer_class = DisplacementPrecedenceSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # بررسی موجودی حق تقدم فروشنده
        seller_precedence = Precedence.objects.filter(user=serializer.validated_data['seller'],company=serializer.validated_data['company']).first()
        
        if not seller_precedence or seller_precedence.precedence < serializer.validated_data['number_of_shares']:
            raise ValidationError({"error": "تعداد حق تقدم فروشنده کافی نیست"})

        # ذخیره انتقال حق تقدم
        self.perform_create(serializer)
        
        # به‌روزرسانی حق تقدم فروشنده
        seller_precedence.precedence -= serializer.validated_data['number_of_shares']
        seller_precedence.save()
        
        # به‌روزرسانی یا ایجاد حق تقدم خریدار
        buyer_precedence = Precedence.objects.filter(user=serializer.validated_data['buyer'],company=serializer.validated_data['company']).first()
        
        if buyer_precedence:
            buyer_precedence.precedence += serializer.validated_data['number_of_shares']
            buyer_precedence.save()
        else:
            Precedence.objects.create(
                user=serializer.validated_data['buyer'],
                company=serializer.validated_data['company'],
                precedence=serializer.validated_data['number_of_shares'],
                used_precedence=0  # مقدار اولیه برای حق تقدم استفاده شده
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                instance = self.get_object()
                old_number_of_shares = instance.number_of_shares
                
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                
                new_number_of_shares = serializer.validated_data.get('number_of_shares')
                
                if new_number_of_shares is None:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                difference = new_number_of_shares - old_number_of_shares
                
                if difference != 0:
                    seller_precedence = Precedence.objects.select_for_update().get(
                        user=instance.seller,
                        company=instance.company
                    )
                    
                    buyer_precedence = Precedence.objects.select_for_update().get(
                        user=instance.buyer,
                        company=instance.company
                    )
                    
                    if difference > 0:  # افزایش تعداد حق تقدم
                        if seller_precedence.precedence < difference:
                            raise ValidationError({"error": "تعداد حق تقدم فروشنده کافی نیست"})
                        seller_precedence.precedence -= difference
                        buyer_precedence.precedence += difference
                    else:  # کاهش تعداد حق تقدم
                        seller_precedence.precedence += abs(difference)
                        buyer_precedence.precedence -= abs(difference)
                    
                    seller_precedence.updated_at = timezone.now()
                    buyer_precedence.updated_at = timezone.now()
                    seller_precedence.save()
                    buyer_precedence.save()
                    
                    instance.number_of_shares = new_number_of_shares
                    instance.updated_at = timezone.now()
                    instance.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
                
            except Precedence.DoesNotExist:
                return Response(
                    {"error": "حق تقدم مورد نظر یافت نشد"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "شما اجازه ویرایش را ندارید"}, 
                status=status.HTTP_403_FORBIDDEN
            )

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                instance = self.get_object()
                
                # بازگرداندن سق تقدم به فروشنده و کم کردن از خریدار
                seller_precedence = Precedence.objects.select_for_update().get(
                    user=instance.seller,
                    company=instance.company
                )
                
                buyer_precedence = Precedence.objects.select_for_update().get(
                    user=instance.buyer,
                    company=instance.company
                )
                
                # برگرداندن سق تقدم به فروشنده
                seller_precedence.precedence += instance.number_of_shares
                # کم کردن حق تقدم از خریدار
                buyer_precedence.precedence -= instance.number_of_shares
                
                seller_precedence.save()
                buyer_precedence.save()
                
                # حذف رکورد انتقال حق تقدم
                instance.delete()
                
                return Response(
                    {"message": "انتقال حق تقدم با موفقیت حذف شد"}, 
                    status=status.HTTP_204_NO_CONTENT
                )
                
            except Precedence.DoesNotExist:
                return Response(
                    {"error": "حق تقدم مورد نظر یافت نشد"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "شما اجازه حذف را ندارید"}, 
                status=status.HTTP_403_FORBIDDEN
            )

# خرید از فرایند
class UnusedPrecedencePurchaseViewset(viewsets.ModelViewSet):
    queryset = UnusedPrecedencePurchase.objects.all()
    serializer_class = UnusedPrecedencePurchaseSerializer
    permission_classes = [IsAuthenticated , IsUnusedPrecedencePurchase]

    def get_permissions(self):
        if self.action in ['create' , 'list' , 'retrieve']:
            self.permission_classes = [IsAdminUser | IsAuthenticated]
        elif self.action in ['update' , 'partial_update' , 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
    def create(self, request):
        process_id = request.data.get('process')
        requested_amount = request.data.get('amount')
        process = UnusedPrecedenceProcess.objects.get(id=process_id)
        # بررسی موجودی
        if int(requested_amount) > int(process.used_amount):
            raise ValidationError({"error": "مقدار درخواستی بیشتر از موجودی است"})
        # محاسبه قیمت
        calculated_price = int(requested_amount) * int(process.price)
        # بررسی نوع فرایند

        document = None
        transaction_id = None
        transaction_url = None

        if request.data.get('type') == '1':
            # فیش
            document = request.FILES.get('document')
            if not document:
                raise ValidationError({"error": "فیش الزامی است"})
        elif request.data.get('type') == '2':
            # درگاه پرداخت
            transaction_id = '1234567890'
            transaction_url = 'https://example.com/transaction/1234567890'
        # ساخت دیتای اولیه
        data = {
            'user': request.user.id,
            'process': process.id,
            'requested_amount': requested_amount,
            'amount': process.used_amount,
            'price': calculated_price,
            'status': 'pending', 
            'document': document,
            'transaction_id': transaction_id,
            'transaction_url': transaction_url,
            'type': request.data.get('type')
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset().filter(user=self.request.user)
        
    
    def update(self, request, *args, **kwargs):
        status = request.data.get('status')
        if status == 'approved':
            process = UnusedPrecedenceProcess.objects.get(id=request.data.get('process'))
            requested_amount = request.data.get('requested_amount')
            used_amount = int(process.used_amount) - int(requested_amount)
            process.used_amount = used_amount
            process.save()

        return super().update(request, *args, **kwargs)
    
    
class UnusedPrecedenceProcessViewset(viewsets.ModelViewSet):
    queryset = UnusedPrecedenceProcess.objects.all()
    serializer_class = UnusedPrecedenceProcessSerializer
    permission_classes = [IsAuthenticated , IsUnusedPrecedenceProcess]

    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return super().get_queryset()
