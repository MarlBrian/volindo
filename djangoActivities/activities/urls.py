from django.urls import re_path
from .views import EventView


app_name = "activities"

urlpatterns = [
    re_path('^', EventView.as_view()),
]