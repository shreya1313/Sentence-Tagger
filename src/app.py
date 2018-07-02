from __future__ import absolute_import, unicode_literals
from flask import Flask
from celery import Celery, signals
import os
import logging.config
import mongoengine


application = Flask(os.environ.get("APPLICATION_NAME"))
SETTINGS_FILE = os.environ.get("SETTINGS_FILE", "settings.local_settings")

application.config.from_object(SETTINGS_FILE)

with application.app_context():
    # this loads all the views with the app context
    # this is also helpful when the views import other
    # modules, this will load everything under the application
    # context and then one can use the current_app configuration
    # parameters
    from apis.urls import all_urls
    from utils.middlewares import set_trace_id_middleware, \
        delete_trace_id_middleware
    from utils.celery_signals import set_trace_id_arg, set_trace_id_local, \
        delete_trace_id_local
    from scripts import ALL_CLI_COMMANDS

    for cli_name, cli_command in ALL_CLI_COMMANDS.items():
        application.cli.add_command(cli_command, name=cli_name)

    logging.config.dictConfig(application.config["LOGGING"])


# Adding all the url rules in the api application
for url, view, methods, _ in all_urls:
    application.add_url_rule(url, view_func=view, methods=methods)

celery = Celery(application.name,
                broker=application.config['CELERY_BROKER_URL'])

celery.conf.update(application.config)
signals.before_task_publish.connect(set_trace_id_arg)
signals.task_prerun.connect(set_trace_id_local)
signals.task_postrun.connect(delete_trace_id_local)


# establishing mongo connection for the entire lifecycle of the project
mongoengine.connect(
    db=application.config['MONGO_SETTINGS']['DB_NAME'],
    host=application.config['MONGO_SETTINGS']['HOST'],
    port=application.config['MONGO_SETTINGS']['PORT'],
    username=application.config['MONGO_SETTINGS']['USERNAME'],
    password=application.config['MONGO_SETTINGS']['PASSWORD'],
)

print("Connected to database!!!")

application.before_request(set_trace_id_middleware)
application.after_request(delete_trace_id_middleware)
