from rest_framework import serializers
from . import models



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Otp
        fields = '__all__'



class AccountsSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Accounts
        fields = '__all__'



class AddressesSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.Addresses
        fields = '__all__'



class JobInfoSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.JobInfo
        fields = '__all__'



class AgentUserSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.AgentUser
        fields = '__all__'



class LegalPersonSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.LegalPerson
        fields = '__all__'



class legalPersonShareholdersSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.legalPersonShareholders
        fields = '__all__'



class legalPersonStakeholdersSerializer(serializers.ModelSerializer):
    class Meta :
        model = models.legalPersonStakeholders
        fields = '__all__'

