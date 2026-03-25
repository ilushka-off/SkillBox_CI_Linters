import factory
from faker import Faker
from db.models import Client, Parking

faker = Faker()


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.LazyAttribute(
        lambda x: faker.credit_card_number() if faker.boolean() else None
    )
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=10, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)
