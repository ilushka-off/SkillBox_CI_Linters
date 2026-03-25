import pytest

@pytest.mark.parametrize("route", [
    "/api/v1/clients",
])
@pytest.mark.asyncio
async def test_get_methods_200(client, route):
    response = await client.get(route)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_create_client(client):
    data = {
        "name": "Ivan",
        "surname": "Ivanov",
        "credit_card": "1111222233334444",
        "car_number": "B222BB"
    }
    response = await client.post("/api/v1/clients", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == "Ivan"

@pytest.mark.asyncio
async def test_create_parking(client):
    data = {
        "address": "Lenina 1",
        "opened": True,
        "count_places": 50,
        "count_available_places": 50
    }
    response = await client.post("/api/v1/parkings", json=data)
    assert response.status_code == 201
    assert response.json()["address"] == "Lenina 1"

@pytest.mark.parking
@pytest.mark.asyncio
async def test_entry_parking(client):
    c_res = await client.post("/api/v1/clients", json={
        "name": "Entry", "surname": "Test", "credit_card": "123", "car_number": "A1"
    })
    client_id = c_res.json()["id"]

    p_res = await client.post("/api/v1/parkings", json={
        "address": "Entry Park", "opened": True, "count_places": 10, "count_available_places": 10
    })
    parking_id = p_res.json()["id"]

    res = await client.post("/api/v1/client_parkings", json={
        "client_id": client_id, "parking_id": parking_id
    })
    assert res.status_code == 201
    assert res.json()["time_in"] is not None

@pytest.mark.parking
@pytest.mark.asyncio
async def test_exit_parking(client):
    c_res = await client.post("/api/v1/clients", json={
        "name": "Exit", "surname": "Test", "credit_card": "123", "car_number": "A2"
    })
    client_id = c_res.json()["id"]

    p_res = await client.post("/api/v1/parkings", json={
        "address": "Exit Park", "opened": True, "count_places": 10, "count_available_places": 10
    })
    parking_id = p_res.json()["id"]

    await client.post("/api/v1/client_parkings", json={
        "client_id": client_id, "parking_id": parking_id
    })

    res = await client.request("DELETE", "/api/v1/client_parkings", json={
        "client_id": client_id, "parking_id": parking_id
    })
    
    assert res.status_code == 200
    assert res.json()["time_out"] is not None

from tests.factories import ClientFactory, ParkingFactory

@pytest.mark.asyncio
async def test_create_client_with_factory(client):
    client_obj = ClientFactory.build()
    data = {
        "name": client_obj.name,
        "surname": client_obj.surname,
        "credit_card": client_obj.credit_card,
        "car_number": client_obj.car_number
    }
    response = await client.post("/api/v1/clients", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == client_obj.name

@pytest.mark.asyncio
async def test_create_parking_with_factory(client):
    parking_obj = ParkingFactory.build()
    data = {
        "address": parking_obj.address,
        "opened": parking_obj.opened,
        "count_places": parking_obj.count_places,
        "count_available_places": parking_obj.count_available_places
    }
    response = await client.post("/api/v1/parkings", json=data)
    assert response.status_code == 201
    assert response.json()["address"] == parking_obj.address

