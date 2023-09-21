from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Plant


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
