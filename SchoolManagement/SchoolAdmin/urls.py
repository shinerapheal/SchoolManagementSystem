from django.urls import path
from . views import *
urlpatterns = [
    path('admin_librarianregister/',LibrarianRegister.as_view()),
    path('admin_librariandata/',LibrarianData.as_view()),
    path('admin_librarianupdate/',LibrarianUpdate.as_view()),
    path('admin_librariandelete/',LibrarianDelete.as_view()),
    path('admin_officeregister/',OfficeRegister.as_view()),
    path('admin_officedata/',OfficeData.as_view()),
    path('admin_officeupdate/',OfficeUpdate.as_view()),
    path('admin_officedelete/',OfficeDelete.as_view()),
    path('admin_studentregister/',StudentRegister.as_view()),
    path('admin_studentdata/',StudentData.as_view()),
    path('admin_studentupdate/',StudentUpdate.as_view()),
    path('admin_studentdelete/',StudentDelete.as_view()),
    path('admin_libraryhystory/',LibraryView.as_view()),
    path('admin_feeview/',FeeView.as_view()),

    ]