import os
import asyncio
from datetime import datetime, timezone, timedelta
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

os.environ["ENVIRONMENT"] = "test"

from main import app as fastapi_app
from db.session import get_engine, get_async_sessionmaker
from db.models import BaseModel, Client, Parking, ClientParking

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture(loop_scope="session")
async def db() -> AsyncGenerator[None, None]:
    async_session = get_async_sessionmaker()
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture(loop_scope="session")
async def app(db):
    client = Client(name="Test", surname="User", credit_card="1234", car_number="A123AA")
    parking = Parking(address="Test Address", opened=True, count_places=100, count_available_places=99)
    
    db.add(client)
    db.add(parking)
    await db.flush()
    
    log = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.now(timezone.utc) - timedelta(hours=2),
        time_out=datetime.now(timezone.utc) - timedelta(hours=1)
    )
    db.add(log)
    await db.commit()
    
    return fastapi_app

@pytest_asyncio.fixture(loop_scope="session")
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
