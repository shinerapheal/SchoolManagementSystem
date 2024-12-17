from rest_framework import serializers
from Accounts.models import *

class LibrarianSerializer(serializers.Serializer):
    

    #User fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    landmark = serializers.CharField(required=True)
    place = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    password = serializers.CharField(required=True)
    joining_date = serializers.DateField(required=True)
    watsapp = serializers.CharField(required=True)

#librarian fields
    profile_image = serializers.ImageField()
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    address_proof = serializers.ImageField()
    adhar_id = serializers.CharField(required=True)



    
    class Meta:
        model=Librarian
        fields=['email','password','phone_number','full_name','address','pin_code','district','state','place','landmark','profile_image','date_of_birth','gender','address_proof','adhar_id']
        

class LibrarianviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Librarian
        fields='__all__'

class OfficeSerializer(serializers.Serializer):
    

    #User fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    landmark = serializers.CharField(required=True)
    place = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    password = serializers.CharField(required=True)
    joining_date = serializers.DateField(required=True)
    watsapp = serializers.CharField(required=True)

#office fields
    profile_image = serializers.ImageField()
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    address_proof = serializers.ImageField()
    adhar_id = serializers.CharField(required=True)



    
    class Meta:
        model=OfficeStaff
        fields=['email','password','phone_number','full_name','address','pin_code','district','state','place','landmark','profile_image','date_of_birth','gender','address_proof','adhar_id']
        
class OfficedataSerializer(serializers.ModelSerializer):
    class Meta:
        model=OfficeStaff
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class StudentSerializer(serializers.Serializer):
     #User fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    landmark = serializers.CharField(required=True)
    place = serializers.CharField(required=True)
    pin_code = serializers.CharField(required=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    password = serializers.CharField(required=True)
    joining_date = serializers.DateField(required=True)
    watsapp = serializers.CharField(required=True)

#student fields
    profile_image = serializers.ImageField()
    date_of_birth = serializers.DateField(required=True)
    gender = serializers.CharField(required=True)
    address_proof = serializers.ImageField()
    adhar_id = serializers.CharField(required=True)



    
    class Meta:
        model=OfficeStaff
        fields=['email','password','phone_number','full_name','address','pin_code','district','state','place','landmark','profile_image','date_of_birth','gender','address_proof','adhar_id']
        
class StudentdataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_details
        fields='__all__'

class LibraryHystorySerilaizer(serializers.ModelSerializer):
    class Meta:
        model=LibraryHystory
        fields='__all__'

class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=FeeRemark
        fields='__all__'
