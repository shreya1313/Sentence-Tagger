import pytest
import mongoengine


class DatabaseFixture():
    """
    for database fixture process two methods that
    connect to a database and then delete it on calling
    after yielding the client
    """

    def __init__(self, application):
        self.application = application

    def connect_db(self):
        """
        establishes connection to the database
        """

        mongoengine.connection.disconnect(alias='default')

        self.conn = mongoengine.connect(
            alias='default',
            host='{}/{}'.format(
                self.application.config['MONGO_SETTINGS']['HOST'],
                self.application.config['MONGO_SETTINGS']['DB_NAME']
            )
        )

    def delete_db(self):
        """
        deletes the test database
        """

        self.conn.drop_database('test')
        self.conn.close()


@pytest.fixture
def client():
    from app import application

    db_fixture = DatabaseFixture(application)

    with application.app_context():
        application.config.from_object('settings.test_settings')

        db_fixture.connect_db()

    client = application.test_client()

    yield client

    db_fixture.delete_db()
