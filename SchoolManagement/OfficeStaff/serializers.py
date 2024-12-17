from Accounts.models import *
from rest_framework import serializers


class StudentFeeSerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    fee_type = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=True)
    amount_payed = serializers.IntegerField(required=True)
    payment_date = serializers.DateField(required=True)
    student_id = serializers.CharField(required=True)
    is_payed=serializers.BooleanField(required=False)


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeRemark
        fields='__all__'


class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_details
        fields = '__all__'

