from django.urls import path,include
from . views import *
urlpatterns = [
    path('librarian_hystory/',LibrarianHystoryCreate.as_view()),
    path('librarian_hystoryview/',LibraryHystoryView.as_view()),
    path('librarian_hystoryedit/',LibraryHystoryEdit.as_view()),
    path('librarian_studentdata/',StudentDataView.as_view()),
    path('librarian_hystorydelete/',LibraryHystoryDelete.as_view()),

   

]
