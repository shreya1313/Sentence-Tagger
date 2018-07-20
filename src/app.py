from __future__ import absolute_import, unicode_literals
from blueprint_app import create_blueprint_app
import mongoengine


application = create_blueprint_app()

# establishing mongo connection for the entire lifecycle of the project
mongoengine.connect(
    alias='default',
    db=application.config['MONGO_SETTINGS']['DB_NAME'],
    host=application.config['MONGO_SETTINGS']['HOST'],
    port=application.config['MONGO_SETTINGS']['PORT'],
    username=application.config['MONGO_SETTINGS']['USERNAME'],
    password=application.config['MONGO_SETTINGS']['PASSWORD'],
)
