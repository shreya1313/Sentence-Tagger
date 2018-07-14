import pytest
import mongoengine


@pytest.fixture
def client():
    from app import application

    with application.app_context():
        application.config.from_object('settings.test_settings')

        # disconnect existing connections
        mongoengine.connection.disconnect(alias='default')

        conn = mongoengine.connect(
            alias='default',
            host='{}/{}'.format(
                application.config['MONGO_SETTINGS']['HOST'],
                application.config['MONGO_SETTINGS']['DB_NAME']
            )
        )

    client = application.test_client()

    yield client

    conn.drop_database('test')
    conn.close()
