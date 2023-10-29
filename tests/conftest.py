import mongoengine
import mongomock
import mongomock.gridfs
import pytest

import program

@pytest.fixture(scope='session')
def bib():
    # see https://github.com/mongomock/mongomock/issues/639
    mongomock.gridfs.enable_gridfs_integration()


    connection = mongoengine.connect(
        'pytest',
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    bib = program.Bib()
    bib.connection = connection
    yield bib
    mongoengine.disconnect()
