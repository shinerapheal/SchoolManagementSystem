from django.shortcuts import render
from Accounts.models import *
from . serializers import *
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class FeeRecord(generics.GenericAPIView):
    serializer_class = StudentFeeSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self,request,*args,**kargs):
        user = self.request.user
        if User.objects.filter(email=user,is_staff=False).exists():
            return Response({"error":"not loged in as office staff"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        if data:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            stu_id = serializer.validated_data.get('student_id')
            if FeeRemark.objects.filter(student_id=stu_id).exists():
                return Response({"error":"fee record alresdy exist"},status=status.HTTP_204_NO_CONTENT)
            else:
                feerecord = FeeRemark.objects.create(student_id=serializer.validated_data.get('student_id'),
                                                    fee_type=serializer.validated_data.get('fee_type'),
                                                    amount=serializer.validated_data.get('amount'),
                                                    amount_payed=serializer.validated_data.get('amount_payed'),
                                                    payment_date=serializer.validated_data.get('payment_date'),
                                                    is_payed=serializer.validated_data.get('is_payed'))
                feerecord.save()
                return Response({"msg":"data reacted"})
        else:
            return Response({"error":"enter the data to store"},status=status.HTTP_204_NO_CONTENT)


#fee view
class FeeView(generics.ListAPIView):
    serializer_class = FeeSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['student_id']
    filter_backends = ( filters.SearchFilter, )

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_staff=False).exists():
            return Response({"error":"not loged in as office staff"},status=status.HTTP_205_RESET_CONTENT)
        obj = FeeRemark.objects.all()
        serializer = FeeSerializer(obj,many=True)
        return FeeRemark.objects.all()


#fee edit
class Feeedit(generics.GenericAPIView):
    serializer_class = FeeSerializer
    permission_classes = [IsAuthenticated]

    def patch(self,request,*args,**kargs):
        user = self.request.user
        if User.objects.filter(email=user,is_staff=False).exists():
            return Response({"error":"not loged in as office staff"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        if data:
            if FeeRemark.objects.filter(student_id=data['id']).exists():
                obj = FeeRemark.objects.get(student_id=data['id'])
                serializer = FeeSerializer(obj,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error":"student doesnt exist of that is"})
        else:
            return Response({"error":"pass the id to edit"},status=status.HTTP_204_NO_CONTENT)
        
#fee delete
class FeeDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        user = self.request.user
        data = self.request.data
        if User.objects.filter(email=user,is_staff=False).exists():
            return Response({"error":"not loged in as staff"})
        else:
            obj = FeeRemark.objects.get(student_id=data['id'])
            obj.delete()
            return Response({"msg":"record deleted"})
        
 
#student details view
class StudentDetailsView(generics.ListAPIView):
    serializer_class = StudentDetailsSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__full_name']
    filter_backends = ( filters.SearchFilter, )

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_staff=False).exists():
            return Response({"error":"not loged in as office staff"},status=status.HTTP_205_RESET_CONTENT)
        Obj = Student_details.objects.all()

        return Student_details.objects.all()
   
