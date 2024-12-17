from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken,Token
from . models import *
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from . serializers import *
import os
import hashlib


class CommonloginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)


            if user.is_superuser:
                role="Admin"
                librarianregister= "/SchoolAdmin/admin_librarianregister/"
                librariandata= "/SchoolAdmin/admin_librariandata/"
                librarianupdate= "/SchoolAdmin/admin_librarianupdate/"
                librariandelete= "/SchoolAdmin/admin_librariandelete/"
                officeregister= "/SchoolAdmin/admin_officeregister/"
                officedata= "/SchoolAdmin/admin_officedata/"
                officeupdate= "/SchoolAdmin/admin_officeupdate/"
                officeredelete= "/SchoolAdmin/admin_officedelete/"
                studentregister= "/SchoolAdmin/admin_studentregister/"
                studentdata= "/SchoolAdmin/admin_studentdata/"
                studentupdate= "/SchoolAdmin/admin_studentupdate/"
                studentdelete= "/SchoolAdmin/admin_studentdelete/"
                libraryhystory= "/SchoolAdmin/admin_libraryhystory/"
                feeview= "/SchoolAdmin/admin_feeview/"


                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                    "librarianregister":librarianregister,
                    "librariandata":librariandata,
                    "librarianupdate":librarianupdate,
                    "librariandelete":librariandelete,
                    "officeregister":officeregister,
                    "officedata":officedata,
                    "officeupdate":officeupdate,
                    "officeredelete":officeredelete,
                    "studentregister":studentregister,
                    "studentdata":studentdata,
                    "studentupdate":studentupdate,
                    "studentdelete":studentdelete,
                    "libraryhystory":libraryhystory,
                    "feeview":feeview
                }
                return Response(response_data,status=status.HTTP_200_OK)
            
            elif user.is_staff:
                role="Admin"
                feehystorycreate= "/OfficeStaff/officestaff_feehystory/"
                feehystoryview= "/OfficeStaff/officestaff_feeview/"
                feeedit= "/OfficeStaff/officestaff_feeedit/"
                feeedelete= "/OfficeStaff/officestaff_feedelete/"
                studentview= "/OfficeStaff/officestaff_studentview/"



                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                    "feehystorycreate":feehystorycreate,
                    "feehystoryview":feehystoryview,
                    "feeedit":feeedit,
                    "studentview":studentview,
                    "feeedelete":feeedelete

                    }
                  
                return Response(response_data,status=status.HTTP_200_OK)
            
            elif user.is_librarian:
                role="librarian"
                libraryhystorycreate= "/Librarian/librarian_hystory/"
                libraryhystoryview= "/Librarian/librarian_hystoryview/"
                libraryhystoryedit= "/Librarian/librarian_hystoryedit/"
                libraryhystorydelete= "/Librarian/librarian_hystorydelete/"

                studentview= "/Librarian/librarian_studentdata/"



                response_data = {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "role": role,
                    "email": user.email,
                    "full_name": user.full_name,
                    "libraryhystorycreate":libraryhystorycreate,
                    "libraryhystoryview":libraryhystoryview,
                    "libraryhystoryedit":libraryhystoryedit,
                    "studentview":studentview,
                    "libraryhystorydelete":libraryhystorydelete

                    }
                  
                return Response(response_data,status=status.HTTP_200_OK)

            
            
   


