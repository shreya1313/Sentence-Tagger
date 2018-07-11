from apis.views import proto
from flask import current_app as app
from descriptors.scaffolding_pb2 import Scaffolding


with app.test_request_context(
    method='GET',
    content_type="application/x-protobuf",
    headers={
        "Accept": "application/x-protobuf"
    }
):
    response, status_code, headers = proto()

data = Scaffolding()
data.ParseFromString(response.data)
print(data)
