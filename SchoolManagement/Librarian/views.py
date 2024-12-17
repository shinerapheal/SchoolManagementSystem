from django.shortcuts import render
from Accounts.models import *
from . serializers import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.filters import SearchFilter


# librarian view.


class LibrarianHystoryCreate(generics.GenericAPIView):
    serializer_class = LibraryHystorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_librarian=False).exists():
            return Response({"error":"not loged in as librarian"},status=status.HTTP_205_RESET_CONTENT)

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        stu_id = serializer.validated_data.get('student_id')
        print(stu_id)
        if Student_details.objects.filter(custom_id=stu_id).exists():
            if LibraryHystory.objects.filter(student_id=stu_id,is_returned=False).exists():
                return Response({"error":"previou book not returned"},status=status.HTTP_204_NO_CONTENT)



          

            lb=LibraryHystory.objects.create(student_id=serializer.validated_data.get('student_id'),
                                            book_name= serializer.validated_data.get('book_name'),
                                            return_date=serializer.validated_data.get('return_date'),
                                            borrow_date=serializer.validated_data.get('borrow_date'),
                                            is_returned=serializer.validated_data.get('is_returned'))
            lb.save()
            return Response({"message":"record created"})
        else:
    
            return Response({"error":"no such student"},status=status.HTTP_204_NO_CONTENT)
        

#library hystory view
class LibraryHystoryView(generics.ListAPIView):
    serializer_class = LibraryHystorySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['student_id','is_returned','book_name']
    filter_backends = ( filters.SearchFilter ,)
    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_librarian=False).exists():
            return Response({"error":"not loged in as librarian"},status=status.HTTP_205_RESET_CONTENT)


        obj = LibraryHystory.objects.all()
        serializer = LibraryHystorySerializer
        return LibraryHystory.objects.all()

        
#library edit
class LibraryHystoryEdit(generics.GenericAPIView):
    serializer_class = LibraryHistoryEditSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        if User.objects.filter(email=user,is_librarian=False).exists():
            return Response({"error":"not loged in as librarian"},status=status.HTTP_205_RESET_CONTENT)


    

        
        data = self.request.data
        print(data)
        if data:

            if LibraryHystory.objects.filter(student_id=data['id'],is_returned=False).exists():
                obj = LibraryHystory.objects.get(student_id=data['id'],is_returned=False)
                serializer = LibraryHistoryEditSerializer(obj,data=data,partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"ser":serializer.data})
            else:
                return Response({"error":"data not editable or student not found edit"})

        else:
            return Response({"error":"pass the id to edit"})
        
#libhys delete
class LibraryHystoryDelete(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        user = self.request.user
        if User.objects.filter(email=user,is_librarian=False).exists():
            return Response({"error":"not loged in as librarian"},status=status.HTTP_205_RESET_CONTENT)
        data = self.request.data
        obj = LibraryHystory.objects.get(student_id=data['id'],is_returned=True)
        obj.delete()
        return Response({"msg":"data deleted"})


#student data
class StudentDataView(generics.ListAPIView): 
    serializer_class = StudentDataSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['user__full_name','custom_id']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        user = self.request.user
        if User.objects.filter(email=user,is_librarian=False).exists():
            return Response({"error":"not loged in as librarian"},status=status.HTTP_205_RESET_CONTENT)


        obj = Student_details.objects.all()
        serializer = StudentDataSerializer(obj,many=True)
        return Student_details.objects.all()
