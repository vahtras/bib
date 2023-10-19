import mongoengine
import mongomock
import mongomock.gridfs
import pytest

@pytest.fixture(scope='session')
def client():
    # see https://github.com/mongomock/mongomock/issues/639
    mongomock.gridfs.enable_gridfs_integration()

    yield mongoengine.connect(
        'pytest',
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    mongoengine.disconnect()
