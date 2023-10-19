from django.urls import path

from .views import PlantList, PlantDetail, PlantImageSearch, DiseaseList, DiseaseDetail

urlpatterns = [
    path("<int:pk>", PlantDetail.as_view(), name="plant_details"),
    path("search_disease", PlantImageSearch.as_view(), name="search_disease"),
    path("<int:plant_id>/diseases", DiseaseList.as_view(), name="disease_list"),
    path(
        "<int:plant_id>/diseases/<int:pk>",
        DiseaseDetail.as_view(),
        name="disease_details",
    ),
    path("", PlantList.as_view(), name="plant_list"),
]
