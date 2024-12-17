from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from Accounts.models import *
from . serializers import *
from rest_framework import authentication
from rest_framework import status
from rest_framework import filters
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


#admin views


#view for librarian register
class LibrarianRegister(generics.GenericAPIView):
    serializer_class=LibrarianSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if User.objects.filter(email=email).exists():
            return Response ({"error":"librariran already exist with this email"},status = status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response ({"error":"librariran already exist with this phone number"},status = status.HTTP_400_BAD_REQUEST)

        password=serializer.validated_data.get('password')
        #user creation
        user=User.objects.create(
            email= serializer.validated_data.get('email'),
            phone_number= serializer.validated_data.get('phone_number'),
            full_name= serializer.validated_data.get('full_name'),
            address= serializer.validated_data.get('address'),
            pin_code= serializer.validated_data.get('pin_code'),
            district =serializer.validated_data.get('district'),
            state= serializer.validated_data.get('state'),
            is_librarian=True)
        user.set_password(password)
        user.save()

        #librarian creation
        librarian=Librarian.objects.create(user=user,profile_image=serializer.validated_data.get('profile_image'),
                                           date_of_birth=serializer.validated_data.get('date_of_birth'),
                                           gender=serializer.validated_data.get('gender'),
                                           address_proof=serializer.validated_data.get('address_proof'),
                                           adhar_id=serializer.validated_data.get('adhar_id'))
        librarian.save()
        return Response({"msg":"librarian created successfully","lbid":librarian.custom_id})

        
#read librarian data
class LibrarianData(generics.ListCreateAPIView):
    serializer_class = LibrarianviewSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__full_name','custom_id']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        obj = Librarian.objects.all()
        print(obj)
        serializer = LibrarianviewSerializer(obj,many=True)
        print(serializer.data)
        return Librarian.objects.all()


#update librarian data
class LibrarianUpdate(generics.GenericAPIView):
    serializer_class = LibrarianviewSerializer,UserSerializer
    permission_classes = [IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        if data:
            if Librarian.objects.filter(custom_id=data['id']).exists():
                obj = Librarian.objects.get(custom_id=data['id'])
                print(obj.user)
                user = User.objects.get(email=obj.user)
                user_serializer = UserSerializer(user,data=data,partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                serializer = LibrarianviewSerializer(obj,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response ({"message":data['id']+"updated","data":serializer.data})
            else:
                return Response({"error":"no data in that id"},status = status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"error":"id or data not passed for update"},status = status.HTTP_400_BAD_REQUEST)

#librarian delete
class LibrarianDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data= self.request.data
        
        if data:
            if Librarian.objects.filter(custom_id=data['id']).exists():
                lb= Librarian.objects.get(custom_id=data['id'])
                obj = User.objects.get(email=lb.user)
                obj.delete()
                return Response({"message":data['id']+" deleted"})
            else:
                return Response({"error":"no librarian in that id"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"pass id to delete"},status=status.HTTP_204_NO_CONTENT)
        
#office staff register
class OfficeRegister(generics.GenericAPIView):
    serializer_class=OfficeSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if User.objects.filter(email=email).exists():
            return Response ({"error":"officestaff already exist with this email"},status = status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response ({"error":"officestaff already exist with this phone number"},status = status.HTTP_400_BAD_REQUEST)

        password=serializer.validated_data.get('password')
        #user creation
        user=User.objects.create(
            email= serializer.validated_data.get('email'),
            phone_number= serializer.validated_data.get('phone_number'),
            full_name= serializer.validated_data.get('full_name'),
            address= serializer.validated_data.get('address'),
            pin_code= serializer.validated_data.get('pin_code'),
            district =serializer.validated_data.get('district'),
            state= serializer.validated_data.get('state'),
            is_staff=True)
        user.set_password(password)
        user.save()

        #office creation
        officestaff=OfficeStaff.objects.create(user=user,profile_image=serializer.validated_data.get('profile_image'),
                                           date_of_birth=serializer.validated_data.get('date_of_birth'),
                                           gender=serializer.validated_data.get('gender'),
                                           address_proof=serializer.validated_data.get('address_proof'),
                                           adhar_id=serializer.validated_data.get('adhar_id'))
        officestaff.save()
        return Response({"msg":"officestaff created successfully","lbid":officestaff.custom_id})
        

#officestaff data
class OfficeData(generics.ListAPIView):
    serializer_class = OfficedataSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__full_name','custom_id']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        obj = OfficeStaff.objects.all()
        serializer = OfficedataSerializer(obj,many=True)
        return OfficeStaff.objects.all()


#office staff update
class OfficeUpdate(generics.GenericAPIView):
    serializer_class = OfficedataSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        if data:
            if OfficeStaff.objects.filter(custom_id=data['id']).exists():
                obj = OfficeStaff.objects.get(custom_id=data['id'])
                user = User.objects.get(email=obj.user)
                user_serializer = UserSerializer(user,data=data,partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                serializer = OfficedataSerializer(obj,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response ({"message":data['id']+"updated","data":serializer.data})
            else:
                return Response({"error":"no data in that id"},status = status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"error":"id or data not passed for update"},status = status.HTTP_400_BAD_REQUEST)
        
#office staff del
class OfficeDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data= self.request.data
        
        if data:
            if OfficeStaff.objects.filter(custom_id=data['id']).exists():
                of= OfficeStaff.objects.get(custom_id=data['id'])
                obj = User.objects.get(email=of.user)
                obj.delete()
                return Response({"message":data['id']+" deleted"})
            else:
                return Response({"error":"no officestaf in that id"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"pass id to delete"},status=status.HTTP_204_NO_CONTENT)
        

#student details
class StudentRegister(generics.GenericAPIView):
    serializer_class=StudentSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        phone_number = serializer.validated_data.get('phone_number')

        if User.objects.filter(email=email).exists():
            return Response ({"error":"studennt already exist with this email"},status = status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response ({"error":"student already exist with this phone number"},status = status.HTTP_400_BAD_REQUEST)

        password=serializer.validated_data.get('password')
        #user creation
        user=User.objects.create(
            email= serializer.validated_data.get('email'),
            phone_number= serializer.validated_data.get('phone_number'),
            full_name= serializer.validated_data.get('full_name'),
            address= serializer.validated_data.get('address'),
            pin_code= serializer.validated_data.get('pin_code'),
            district =serializer.validated_data.get('district'),
            state= serializer.validated_data.get('state'),
            is_student=True)
        user.set_password(password)
        user.save()

        #student creation
        student=Student_details.objects.create(user=user,profile_image=serializer.validated_data.get('profile_image'),
                                           date_of_birth=serializer.validated_data.get('date_of_birth'),
                                           gender=serializer.validated_data.get('gender'),
                                           address_proof=serializer.validated_data.get('address_proof'),
                                           adhar_id=serializer.validated_data.get('adhar_id'))
        student.save()
        return Response({"msg":"student created successfully","lbid":student.custom_id})
        

#student setails        
class StudentData(generics.ListAPIView):
    serializer_class = StudentdataSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__full_name','custom_id']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        obj = Student_details.objects.all()
        serializer = StudentdataSerializer(obj,many=True)
        return Student_details.objects.all()


#student update
class StudentUpdate(generics.GenericAPIView):
    serializer_class = StudentdataSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        if data:
            if Student_details.objects.filter(custom_id=data['id']).exists():
                obj = Student_details.objects.get(custom_id=data['id'])
                user = User.objects.get(email=obj.user)
                user_serializer = UserSerializer(user,data=data,partial=True)
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()
                serializer = StudentdataSerializer(obj,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response ({"message":data['id']+"updated","data":serializer.data})
            else:
                return Response({"error":"no data in that id"},status = status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"error":"id or data not passed for update"},status = status.HTTP_400_BAD_REQUEST)
        

#student delete
class StudentDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)
        data= self.request.data
        
        if data:
            if Student_details.objects.filter(custom_id=data['id']).exists():
                st= Student_details.objects.get(custom_id=data['id'])
                obj = User.objects.get(email=st.user)
                obj.delete()
                return Response({"message":data['id']+" deleted"})
            else:
                return Response({"error":"no student in that id"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error":"pass id to delete"},status=status.HTTP_204_NO_CONTENT)
        
#library hystory
class LibraryView(generics.ListAPIView):
    serializer_class=LibraryHystorySerilaizer
    permission_classes = [IsAuthenticated]
    search_fields = ['student_id','book_name']
    filter_backends = (filters.SearchFilter,)
    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)

        obj = LibraryHystory.objects.all()
        serializer = LibraryHystorySerilaizer(obj,many=True)
        return LibraryHystory.objects.all()
    
#fee hystory
class FeeView(generics.ListAPIView):
    serializer_class=FeeSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['student_id']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_superuser=False).exists():
            return Response({"error":"not loged in as admin"},status=status.HTTP_205_RESET_CONTENT)

        obj = FeeRemark.objects.all()
        serializer = FeeSerializer(obj,many=True)
        return FeeRemark.objects.all()