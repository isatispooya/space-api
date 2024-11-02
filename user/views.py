from django.shortcuts import render
from rest_framework.views import APIView
from GuardPyCaptcha.Captch import GuardPyCaptcha
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from rest_framework.response import Response
from rest_framework import status
from .models import User , Otp , legalPersonStakeholders , legalPersonShareholders , AgentUser,  LegalPerson , JobInfo , Addresses ,Accounts    
from rest_framework.permissions import AllowAny
import json
import requests
import os
from space_api import settings
from django.utils import timezone
from . import fun
import datetime


def parse_date(date_str):
    try:
        # تبدیل تاریخ به فرمت YYYY-MM-DD
        return datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
    except (ValueError, TypeError):
        return None
# captcha
class CaptchaViewset(APIView) :
    permission_classes = [AllowAny]
    @method_decorator(ratelimit(key='ip', rate='5/m', method='GET', block=True))
    def get (self,request):
        captcha = GuardPyCaptcha ()
        captcha = captcha.Captcha_generation(num_char=4 , only_num= True)
        return Response ({'captcha' : captcha} , status = status.HTTP_200_OK)

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

        return Response({'message' : 'اطلاعات شما یافت نشد'},status=status.HTTP_400_BAD_REQUEST)   
                

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
        # try:
        #     user = User.objects.get(uniqueIdentifier=uniqueIdentifier)
        #     # if user.is_locked():
        #          return Response({'message': 'حساب شما قفل است، لطفاً بعد از مدتی دوباره تلاش کنید.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        # except  :
        #     pass
        # if user : 
        #     try:
        #         mobile = user.mobile
        #         otp_obj = Otp.objects.filter(mobile=mobile , code = otp ).order_by('-date').first()
        #         if otp_obj is None:
        #             user.attempts += 1  
        #             if user.attempts >= 3:
        #                 user.lock() 
        #                 return Response({'message': 'تعداد تلاش‌های شما بیش از حد مجاز است. حساب شما برای 5 دقیقه قفل شد.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        #             user.save()  
        #             return Response({'message': 'کد تأیید اشتباه است'}, status=status.HTTP_400_BAD_REQUEST)

        #         if otp_obj.expire and timezone.now() > otp_obj.expire:
        #             return Response({'message': 'زمان کد منقضی شده است'}, status=status.HTTP_400_BAD_REQUEST)

        #     except Exception as e:
        #         return Response({'message': 'کد تأیید نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)
        #     user.attempts = 0
        #     user.save()
        #     otp_obj.delete()
        #     token = fun.encryptionUser(user)
        #     return Response({'access': token}, status=status.HTTP_200_OK)
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
            if  not new_user :
                # new_user  =User(
                #     username = data['uniqueIdentifier'],    
                #     email = data['email'],
                #     password = data['uniqueIdentifier'],
                #     is_active = None,
                #     first_name = data['firstName'],
                #     last_name = data['lastName'],
                #     mobile = data['mobile'],
                #     gender = data['gender'],
                #     birth_date = data['birthDate'],
                #     created_at = data['createdAt'],
                #     updated_at = data['updatedAt'],
                #     address = data['address'],
                #     profile_image = data['profileImage'],
                #     last_login = data['lastLogin'],
                #     status = data['status'],
                #     bio = data['bio'],
                #     uniqueIdentifier = data['uniqueIdentifier'],
                #     chat_id_telegram = data['chatIdTelegram'],
                #     last_password_change = data['lastPasswordChange'],
                #     login_attempts = data['loginAttempts'],
                #     seri_shenasname = data['seriSh'],
                #     seri_shenasname_char = data['seriShChar'],
                #     serial_shenasname = data['serial'],
                #     place_of_birth = data['placeOfBirth'],
                #     place_of_issue = data['placeOfIssue'],
                #     father_name = data['fatherName'],
                #     education_level = data['educationLevel'],
                #     marital_status = data['maritalStatus'],
                    
                # )
                # new_user.save()
                
                

                new_user = User(
                    username=data.get('uniqueIdentifier'),
                    email=data.get('email'),
                    password=data.get('uniqueIdentifier'),
                    is_active=True,
                    first_name=private_person_data.get('firstName'),
                    last_name=private_person_data.get('lastName'),
                    mobile=data.get('mobile'),
                    gender='M' if private_person_data.get('gender') == 'Male' else 'F' if private_person_data.get('gender') == 'Female' else None,
                    birth_date=parse_date(private_person_data.get('birthDate')),  # تبدیل تاریخ به فرمت صحیح
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

            token = fun.encryptionUser(new_user)

            return Response({'message': data , 'access' : ''} , status=status.HTTP_200_OK)
