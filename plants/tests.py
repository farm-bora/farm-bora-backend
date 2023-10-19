from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

from .models import Plant, Disease


# Create your tests here.
class PlantModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.plant = Plant.objects.create(
            name="Maize",
            botanical_name="Zea Mays",
            details="Also called corn by our friends from the West",
        )

    def test_model_content(self) -> None:
        self.assertEqual(self.plant.name, "Maize")
        self.assertEqual(self.plant.botanical_name, "Zea Mays")
        self.assertEqual(
            self.plant.details, "Also called corn by our friends from the West"
        )

    def test_api_listview(self) -> None:
        response = self.client.get(reverse("plant_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Plant.objects.count(), 1)
        self.assertContains(response, self.plant)

    def test_api_detailview(self) -> None:
        response = self.client.get(
            reverse("plant_details", kwargs={"pk": self.plant.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Plant.objects.count(), 1)
        self.assertContains(response, "Zea Mays")


class DiseaseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.plant = Plant.objects.create(
            name="Maize",
            botanical_name="Zea Mays",
            details="Also called corn by our friends from the West",
        )
        cls.disease = Disease.objects.create(
            plant=cls.plant, name="Lorem Ipsum", details="Dolor sit amet consecteteur"
        )

        other_plant = Plant.objects.create(
            name="Other Plant",
            botanical_name="othias plantanimus",
            details="Another plant",
        )
        Disease.objects.create(
            plant=other_plant, name="scaramus botanicus", details="Pretty scary"
        )

    def test_model_content(self) -> None:
        self.assertEqual(self.disease.name, "Lorem Ipsum")
        self.assertEqual(self.disease.details, "Dolor sit amet consecteteur")
        self.assertEqual(self.disease.plant.name, "Maize")

    def test_plants_api_listview_shows_diseases(self) -> None:
        response = self.client.get(reverse("plant_details", args=[self.plant.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)["diseases"]), 1)

    def test_api_listview(self) -> None:
        response = self.client.get(reverse("disease_list", args=[self.plant.id]))
        self.assertEqual(len(json.loads(response.content)), 2)

    def test_api_detailview(self) -> None:
        response = self.client.get(
            reverse("disease_details", args=[self.plant.id, self.disease.id])
        )
        self.assertContains(response, "Lorem Ipsum")
