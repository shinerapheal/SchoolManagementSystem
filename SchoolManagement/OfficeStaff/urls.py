from django.urls import path
from . views import *
urlpatterns = [
    path('officestaff_feehystory/',FeeRecord.as_view()),
    path('officestaff_feeview/',FeeView.as_view()),
    path('officestaff_feeedit/',Feeedit.as_view()),
    path('officestaff_studentview/',StudentDetailsView.as_view()),
    path('officestaff_feedelete/',FeeDelete.as_view()),




    ]