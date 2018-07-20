from __future__ import absolute_import, unicode_literals
from common.bootstrap_app import bootstrap_app
from scripts import ALL_CLI_COMMANDS
import mongoengine


application = bootstrap_app()

# establishing mongo connection for the entire lifecycle of the project
mongoengine.connect(
    alias='default',
    db=application.config['MONGO_SETTINGS']['DB_NAME'],
    host=application.config['MONGO_SETTINGS']['HOST'],
    port=application.config['MONGO_SETTINGS']['PORT'],
    username=application.config['MONGO_SETTINGS']['USERNAME'],
    password=application.config['MONGO_SETTINGS']['PASSWORD'],
)


for cli_name, cli_command in ALL_CLI_COMMANDS.items():
    application.cli.add_command(cli_command, name=cli_name)


with application.app_context():
    from apis.urls import api_urls

    # Adding all the url rules in the api application
    for url, view, methods, _ in api_urls:
        application.add_url_rule(url, view_func=view, methods=methods)
