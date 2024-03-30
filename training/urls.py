from django.urls import path
from . import views

app_name = "training"

urlpatterns = [
    path('leadersboard', views.LeadersBoardAPIView.as_view(), name="leadersboard"),
    path('login', views.UserEnterAPIView.as_view(), name="login"),
    path('perform-training', views.PerformActivityAPIView.as_view(), name="run-task"),
    path('activities', views.ActivitiesListAPIView.as_view(), name="activities"),
]

