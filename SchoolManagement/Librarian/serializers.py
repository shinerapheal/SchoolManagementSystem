from Accounts.models import *
from rest_framework import serializers

class LibraryHystorySerializer(serializers.Serializer):
    student_id = serializers.CharField(required=True)
    book_name = serializers.CharField(required=True)
    borrow_date = serializers.DateField(required=True)
    return_date = serializers.DateField(required=True)
    is_returned = serializers.BooleanField(required=False)
    class Meta:
        models = LibraryHystory
        fields='__all__'

class LibraryHistoryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHystory
        fields = '__all__'
        
class StudentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student_details
        fields = '__all__'

