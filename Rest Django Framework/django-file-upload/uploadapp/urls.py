from django.urls import path
from .views import *

urlpatterns = [
    path('', FileUploadView.as_view()),
    path("polls/", polls_list, name="polls_list")
]