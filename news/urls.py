from django.urls import path
from . import views

urlpatterns = [
    path("<str:section_name>", views.section_index, name="section_index"),
]
