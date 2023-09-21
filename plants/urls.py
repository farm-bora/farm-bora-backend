from django.urls import path

from .views import PlantList, PlantDetail

urlpatterns = [
    path("<int:pk>/", PlantDetail.as_view(), name="plant_details"),
    path("", PlantList.as_view(), name="plant_list"),
]
