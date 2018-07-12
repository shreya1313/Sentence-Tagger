from flask_caching import Cache
from flask import current_app as app


cache = Cache(app, config=app.config.get('CACHE_CONFIGURATION'))
