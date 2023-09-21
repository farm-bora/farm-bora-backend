from django.test import TestCase

from .models import Plant

# Create your tests here.
class PlantModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.plant = Plant.objects.create(
            name='Maize',
            botanical_name='Zea Mays',
            details='Also called corn by our friends from the West'
        )

    def test_model_content(self) -> None:
        self.assertEqual(self.plant.name, 'Maize')
        self.assertEqual(self.plant.botanical_name, 'Zea Mays')
        self.assertEqual(self.plant.details, 'Also called corn by our friends from the West')