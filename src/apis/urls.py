from apis import views
from flask import current_app as app


api_urls = [
    ("/", views.index, ["GET"], "flask scaffolding index url"),
    ("/error", views.error, ["GET"], "testing 500 as json"),
    ("/proto-test", views.proto, ['GET'], 'testing proto requests')
]

other_urls = []

if app.config['ENVIRONMENT'] != 'development':
    print('Removing the default api urls')
    api_urls = []

all_urls = api_urls + other_urls
