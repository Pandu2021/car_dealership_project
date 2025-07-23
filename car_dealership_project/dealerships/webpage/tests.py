from django.test import TestCase
from .models import CarMake, CarModel

class CarModelTestCase(TestCase):
    def setUp(self):
        make = CarMake.objects.create(name="Toyota", description="Reliable Japanese cars")
        CarModel.objects.create(make=make, name="Yaris", dealer_id=3, year=2021)

    def test_str_representation(self):
        car = CarModel.objects.get(name="Yaris")
        self.assertEqual(str(car), "Toyota Yaris (2021)")