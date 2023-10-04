from django.urls import path

from .views import PlantList, PlantDetail, PlantImageSearch

urlpatterns = [
    path("<int:pk>", PlantDetail.as_view(), name="plant_details"),
    path("search_disease", PlantImageSearch.as_view(), name="search_disease"),
    path("", PlantList.as_view(), name="plant_list"),
]
