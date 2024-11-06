from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import status
from .models import User , Otp , legalPersonStakeholders , legalPersonShareholders , AgentUser,  LegalPerson , JobInfo , Addresses ,Accounts , UUid
from rest_framework.permissions import AllowAny,IsAuthenticated , IsAdminUser
import json
import requests
import os
from space_api import settings
from django.utils import timezone
from .serializers import UUidSerializer , UserSerializer , AccountsSerializer , AddressesSerializer , JobInfoSerializer , AgentUserSerializer ,LegalPersonSerializer , legalPersonShareholdersSerializer , legalPersonStakeholdersSerializer
from .date import parse_date
from datetime import timedelta
from uuid import uuid4
from utils.legal import is_legal_person
from utils.sms import SendSmsUUid
from rest_framework_simplejwt.tokens import RefreshToken  # اضافه کردن این خط


# otp sejam
class OtpSejamViewset(APIView):
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        encrypted_response = request.data['encrypted_response'].encode()
        if isinstance(encrypted_response, str):
            encrypted_response = encrypted_response.encode('utf-8')
        captcha = GuardPyCaptcha()

        captcha = captcha.check_response(encrypted_response, request.data['captcha'])
        if request.data['captcha'] == ''  or not captcha :
            pass#return Response ({'message' : 'کد کپچا خالی است'} , status=status.HTTP_400_BAD_REQUEST)

        uniqueIdentifier = request.data['uniqueIdentifier']
        if not uniqueIdentifier :
            return Response ({'message' : 'کد ملی را وارد کنید'} , status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter (uniqueIdentifier = uniqueIdentifier).first()
        if not user:
            url = "http://31.40.4.92:8870/otp"
            payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier
            })
            headers = {
            'X-API-KEY': os.getenv('X-API-KEY'),
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code >=300 :
                return Response ({'message' :'شما سجامی نیستید'} , status=status.HTTP_400_BAD_REQUEST)
            return Response ({'registered' :False , 'message' : 'کد تایید ارسال شد'},status=status.HTTP_200_OK)

        return Response({'message' : 'شما قبلا ثبت نام کرده اید'},status=status.HTTP_400_BAD_REQUEST)   
                

# register  user's account for new user
class RegisterViewset(APIView):
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post (self, request) :
        uniqueIdentifier = request.data.get('uniqueIdentifier')
        otp = request.data.get('otp')
        user = None

        if not uniqueIdentifier or not otp:
            return Response({'message': 'کد ملی و کد تأیید الزامی است'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user :
            url = "http://31.40.4.92:8870/information"
            payload = json.dumps({
            "uniqueIdentifier": uniqueIdentifier,
            "otp": otp
            })
            headers = {
            'X-API-KEY': os.getenv('X-API-KEY'),
            'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            response = json.loads(response.content)
            try :
                data = response['data']
                print(data)
            except:
                return Response({'message' :'1دوباره تلاش کن '}, status=status.HTTP_400_BAD_REQUEST)
            if data == None :
                return Response({'message' :'بیشتر تلاش کن '}, status=status.HTTP_400_BAD_REQUEST)
            new_user = User.objects.filter(uniqueIdentifier=uniqueIdentifier).first()
            private_person_data = data['privatePerson']
            if not new_user :
               
                new_user = User(
                    username=data.get('uniqueIdentifier'),
                    email=data.get('email'),
                    is_active=True,
                    first_name=private_person_data.get('firstName'),
                    last_name=private_person_data.get('lastName'),
                    mobile=data.get('mobile'),
                    gender='M' if private_person_data.get('gender') == 'Male' else 'F' if private_person_data.get('gender') == 'Female' else None,
                    birth_date=parse_date(private_person_data.get('birthDate')),  
                    created_at=parse_date(data.get('createdAt')),
                    updated_at=parse_date(data.get('updatedAt')),
                    address=data['addresses'][0].get('remnantAddress') if data.get('addresses') and len(data['addresses']) > 0 else None,
                    profile_image=None,
                    last_login=None,
                    status=True if data.get('status') == 'Sejami' else False,
                    bio=None,
                    uniqueIdentifier=data.get('uniqueIdentifier'),
                    chat_id_telegram=None,
                    last_password_change=None,
                    login_attempts=0,
                    seri_shenasname=private_person_data.get('seriSh'),
                    seri_shenasname_char=private_person_data.get('seriShChar'),
                    serial_shenasname=private_person_data.get('serial'),
                    place_of_birth=private_person_data.get('placeOfBirth'),
                    place_of_issue=private_person_data.get('placeOfIssue'),
                    father_name=private_person_data.get('fatherName'),
                    education_level=None,
                    marital_status=None,
                )
                new_user.set_password(data.get('uniqueIdentifier'))
                new_user.save()
                    
            if len(data['legalPersonStakeholders']) > 0:
                    for legalPersonStakeholders_data in data['legalPersonStakeholders'] :
                        new_legalPersonStakeholders = legalPersonStakeholders(
                        user = new_user ,
                        uniqueIdentifier =legalPersonStakeholders_data['uniqueIdentifier'] ,
                        type = legalPersonStakeholders_data['type'],
                        start_at = legalPersonStakeholders_data ['startAt'],
                        position_type = legalPersonStakeholders_data ['positionType'],
                        last_name = legalPersonStakeholders_data ['lastName'],
                        is_owner_signature = legalPersonStakeholders_data ['isOwnerSignature'],
                        first_name = legalPersonStakeholders_data ['firstName'],
                        end_at = legalPersonStakeholders_data ['endAt'] ,)
                    new_legalPersonStakeholders.save()

            if data['legalPerson']:
                new_LegalPerson = LegalPerson(
                user = new_user ,
                company_name = data['legalPerson']['companyName'] ,
                citizenship_country =data['legalPerson']['citizenshipCountry'] ,
                economic_code = data['legalPerson']['economicCode'],
                evidence_expiration_date = data['legalPerson'] ['evidenceExpirationDate'],
                evidence_release_company = data['legalPerson'] ['evidenceReleaseCompany'],
                evidence_release_date = data['legalPerson'] ['evidenceReleaseDate'],
                legal_person_type_sub_category = data['legalPerson'] ['legalPersonTypeSubCategory'],
                register_date = data['legalPerson'] ['registerDate'],
                legal_person_type_category = data['legalPerson'] ['legalPersonTypeCategory'],
                register_place = data['legalPerson'] ['registerPlace'] ,
                register_number = data['legalPerson'] ['registerNumber'] ,)
                new_LegalPerson.save()

            if len(data['legalPersonShareholders']) > 0:
                    for legalPersonShareholders_data in data['legalPersonShareholders'] :
                        new_legalPersonShareholders = legalPersonShareholders(
                        user = new_user ,
                        uniqueIdentifier = legalPersonShareholders_data['uniqueIdentifier'],
                        postal_code = legalPersonShareholders_data ['postalCode'],
                        position_type = legalPersonShareholders_data ['positionType'],
                        percentage_voting_right = legalPersonShareholders_data ['percentageVotingRight'],
                        first_name = legalPersonShareholders_data ['firstName'],
                        last_name = legalPersonShareholders_data ['lastName'],
                        address = legalPersonShareholders_data ['address'] )
                    new_legalPersonShareholders.save()
            if len(data['accounts']) > 0:
                for acounts_data in data['accounts'] :
                    new_accounts = Accounts(
                        user = new_user ,
                        account_number = acounts_data['accountNumber'] ,
                        bank = acounts_data ['bank']['name'],
                        branch_code = acounts_data ['branchCode'],
                        branch_name = acounts_data ['branchName'],
                        is_default = acounts_data ['isDefault'],
                        type = acounts_data ['type'],
                        sheba_number = acounts_data ['sheba'] ,)
                    new_accounts.save()
            if len (data['addresses']) > 0 :
                for addresses_data in data ['addresses']:
                    new_addresses = Addresses (
                        user = new_user,
                        alley =  addresses_data ['alley'],
                        city =  addresses_data ['city']['name'],
                        city_prefix =  addresses_data ['cityPrefix'],
                        country = addresses_data ['country']['name'],
                        country_prefix =  addresses_data ['countryPrefix'],
                        email =  addresses_data ['email'],
                        emergency_tel =  addresses_data ['emergencyTel'],
                        emergency_tel_city_prefix =  addresses_data ['emergencyTelCityPrefix'],
                        emergency_tel_country_prefix =  addresses_data ['emergencyTelCountryPrefix'],
                        fax =  addresses_data ['fax'],
                        fax_prefix =  addresses_data ['faxPrefix'],
                        plaque =  addresses_data ['plaque'],
                        postal_code =  addresses_data ['postalCode'],
                        province =  addresses_data ['province']['name'],
                        remnant_address =  addresses_data ['remnantAddress'],
                        section =  addresses_data ['section']['name'],
                        tel =  addresses_data ['tel'],
                    )
                    new_addresses.save()
                jobInfo_data = data.get('jobInfo')
                if isinstance(jobInfo_data, dict):
                    new_jobInfo = JobInfo(
                        user=new_user,
                        company_address=jobInfo_data.get('companyAddress', ''),
                        company_city_prefix=jobInfo_data.get('companyCityPrefix', ''),
                        company_email=jobInfo_data.get('companyEmail', ''),
                        company_fax=jobInfo_data.get('companyFax', ''),
                        company_fax_prefix=jobInfo_data.get('companyFaxPrefix', ''),
                        company_name=jobInfo_data.get('companyName', ''),
                        company_phone=jobInfo_data.get('companyPhone', ''),
                        company_postal_code=jobInfo_data.get('companyPostalCode', ''),
                        company_web_site=jobInfo_data.get('companyWebSite', ''),
                        employment_date=jobInfo_data.get('employmentDate', ''),
                        job_title=jobInfo_data.get('job', {}).get('title', ''),
                        job_description=jobInfo_data.get('jobDescription', ''),
                        position=jobInfo_data.get('position', ''),
                    )

                    new_jobInfo.save()
                agent = data.get('agent')
                if isinstance(agent, dict):
                    new_agent = AgentUser(
                        user=new_user,
                        description=new_agent.get('description', ''),
                        expiration_date=new_agent.get('expirationDate', ''),
                        first_name=new_agent.get('firstName', ''),
                        is_confirmed=new_agent.get('isConfirmed', ''),
                        last_name=new_agent.get('lastName', ''),
                        type=new_agent.get('type', ''),
                        father_uniqueIdentifier=new_agent.get('uniqueIdentifier', ''),
     
                    )

                    new_agent.save()
            
            refresh = RefreshToken.for_user(new_user)
            access = str(refresh.access_token)
            return Response({'refresh': str(refresh), 'access':access}, status=status.HTTP_200_OK)


#update user password
class ChangePasswordViewset(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def patch(self, request):
        user = request.user
        last_password = request.data.get('last_password')
        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if not last_password or not new_password or not new_password_confirm:
            return Response({'message': 'اطلاعات وارد شده نادرست است'}, status=status.HTTP_400_BAD_REQUEST)
        if new_password != new_password_confirm:
            return Response({'message': 'رمز عبور وارد شده با تکرار آن مطابقت ندارد'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(last_password):
            return Response({'message': 'رمز عبور قبلی وارد شده اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.last_password_change = timezone.now()
        user.save()
        return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)
    

# forgot password
class ForgotPasswordViewset(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True))
    def post(self, request):
        user = request.user
        mobile = user.mobile
        expire = timezone.now() + timedelta(minutes=10)

        uuid_create, created = UUid.objects.update_or_create(user=user,defaults={'uuid': uuid4(),'expire': expire, 'status': False})
             
        if not uuid_create.uuid:
            uuid_create.uuid = uuid4()
            uuid_create.save()

        uuid_serializer = UUidSerializer(uuid_create).data
        uuid = uuid_serializer['uuid']
        print(uuid)
        
        SendSmsUUid(mobile, uuid)

        if created:
            uuid_create.status = True
            uuid_create.save()
            return Response({'message': 'کد تایید ارسال شد'}, status=status.HTTP_200_OK)

        return Response({'message': 'کد تایید ارسال شد'}, status=status.HTTP_200_OK)


    def patch(self, request):
        user = request.user
        uuid = request.query_params.get('uuid')
        if not uuid:
            return Response({'message': 'کد تایید وارد نشده است'}, status=status.HTTP_400_BAD_REQUEST)
        
        uuid_obj = UUid.objects.filter(uuid=uuid, user=user, status=False, expire__gte=timezone.now()).first()
        print(uuid_obj)
        
        if not uuid_obj:
            return Response({'message': 'کد تایید اشتباه است یا منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        new_password_confirm = request.data.get('new_password_confirm')
        if not new_password or not new_password_confirm or new_password != new_password_confirm:
            return Response({'message': 'رمز عبور وارد شده با تکرار آن مطابقت ندارد'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.last_password_change = timezone.now()
        user.save()
        
        uuid_obj.status = True
        uuid_obj.save()
        
        return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)


# user profile
class ProfileViewset(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
       

        user_serializer = UserSerializer(user).data

        accounts = Accounts.objects.filter(user=user)
        accounts_serializer = AccountsSerializer(accounts, many=True).data

        addresses = Addresses.objects.filter(user=user)
        addresses_serializer = AddressesSerializer(addresses, many=True).data

        jobInfo = JobInfo.objects.filter(user=user).first()
        jobInfo_serializer = JobInfoSerializer(jobInfo, many=False).data

        if AgentUser.objects.filter(user=user) :
            agentUser = AgentUser.objects.filter(user=user).first()
            agentUser_serializer = AgentUserSerializer(agentUser, many=False).data
        else :
            agentUser_serializer = None

        if is_legal_person(user) == True :
            legal_person = LegalPerson.objects.filter(user=user).first()
            legal_person_serializer = LegalPersonSerializer(legal_person, many=False).data

            legal_person_shareholders = legalPersonShareholders.objects.filter(user=user)
            legal_person_shareholders_serializer = legalPersonShareholdersSerializer(legal_person_shareholders, many=True).data

            legal_person_stakeholders = legalPersonStakeholders.objects.filter(user=user)
            legal_person_stakeholders_serializer = legalPersonStakeholdersSerializer(legal_person_stakeholders, many=True).data
        else :
            legal_person_serializer = None
            legal_person_shareholders_serializer = None
            legal_person_stakeholders_serializer = None

        combined_data = {
            **user_serializer,
            'accounts' : accounts_serializer,
            'addresses' : addresses_serializer,
            'jobInfo' : jobInfo_serializer,
            'agentUser' : agentUser_serializer,
            'legal_person' : legal_person_serializer,
            'legal_person_shareholders' : legal_person_shareholders_serializer,
            'legal_person_stakeholders' : legal_person_stakeholders_serializer,
        }
        
        return Response( combined_data,status=status.HTTP_200_OK)


# all users for admin
class UserViewset(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        user = request.user
        user = User.objects.all()
        user_serializer = UserSerializer(user, many=True)
        return Response(user_serializer.data,status=status.HTTP_200_OK)
    

class UserDetailViewset(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user_serializer = UserSerializer(user).data

            accounts = Accounts.objects.filter(user=user)
            accounts_serializer = AccountsSerializer(accounts, many=True).data

            addresses = Addresses.objects.filter(user=user)
            addresses_serializer = AddressesSerializer(addresses, many=True).data

            jobInfo = JobInfo.objects.filter(user=user).first()
            jobInfo_serializer = JobInfoSerializer(jobInfo, many=False).data

            if AgentUser.objects.filter(user=user) :
                agentUser = AgentUser.objects.filter(user=user).first()
                agentUser_serializer = AgentUserSerializer(agentUser, many=False).data
            else :
                agentUser_serializer = None

            if is_legal_person(user) == True :
                legal_person = LegalPerson.objects.filter(user=user).first()
                legal_person_serializer = LegalPersonSerializer(legal_person, many=False).data

                legal_person_shareholders = legalPersonShareholders.objects.filter(user=user)
                legal_person_shareholders_serializer = legalPersonShareholdersSerializer(legal_person_shareholders, many=True).data

                legal_person_stakeholders = legalPersonStakeholders.objects.filter(user=user)
                legal_person_stakeholders_serializer = legalPersonStakeholdersSerializer(legal_person_stakeholders, many=True).data
            else :
                legal_person_serializer = None
                legal_person_shareholders_serializer = None
                legal_person_stakeholders_serializer = None

            combined_data = {
                **user_serializer,
                'accounts' : accounts_serializer,
                'addresses' : addresses_serializer,
                'jobInfo' : jobInfo_serializer,
                'agentUser' : agentUser_serializer,
                'legal_person' : legal_person_serializer,
                'legal_person_shareholders' : legal_person_shareholders_serializer,
                'legal_person_stakeholders' : legal_person_stakeholders_serializer,
            }
        
            return Response( combined_data,status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'message': 'کاربر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)