import mongoengine
import mongomock
import pytest

@pytest.fixture(scope='session')
def client():
    yield mongoengine.connect(
        'pytest',
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    mongoengine.disconnect()
