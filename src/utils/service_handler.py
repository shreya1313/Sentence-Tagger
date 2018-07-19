import requests
from flask import current_app as app
from utils.pbj import copy_pb_to_dict
import urllib
import os
import subprocess
import logging


logger = logging.getLogger(__name__)


def compile_proto_files():
    """
    compiles the proto files present in the directory specified
    """

    protofiles_dir = app.config['PROTOFILES_DIRECTORY']
    descriptors_dir = app.config['DESCRIPTORS_DIRECTORY']

    command = [
        'protoc', '--proto_path={}'.format(protofiles_dir),
        '--python_out={} {}/*.proto'.format(descriptors_dir,
                                            protofiles_dir)
    ]

    process = subprocess.Popen(' '.join(command), shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    process.wait()


def download_external_proto_files():
    """
    downloads the external proto files given in the configuration
    and saves it to the path
    """

    externals = app.config['EXTERNAL_PROTOBUF_CONFIG']
    protofiles_dir = app.config['PROTOFILES_DIRECTORY']

    if not externals:
        return

    for url in externals:
        file_name = url.split('/')[-1]
        file_path = os.path.join(protofiles_dir, file_name)

        urllib.request.urlretrieve(url, file_path)


def validate_protobuf_request(message, payload):
    """
    validates the protobuf validations
    """

    try:
        message_obj = message(**payload)
        serialized_data = message_obj.SerializeToString()

        return serialized_data, True
    except Exception as exc:
        logger.error('Validation failed for {} with payload {}'.format(
            message, payload
        ))

        return exc.args[0], False


def parse_response_data(response, response_message):
    """
    parses the response data into the dictionary object
    """

    message = response_message()

    message.ParseFromString(response.content)

    data_dict = {}

    copy_pb_to_dict(data_dict, message)

    return data_dict


def perform_microservice_request(method, endpoint, response_message=None,
                                 request_message=None, payload={},
                                 query_params={}, headers={}):
    """
    this function performs the microservice requests
    given certain parameters and returns the output
    of the request along with the status code. this
    will also start using the protobuf which will be
    common while validating the data to be sent to the
    service
    """

    headers.update({
        'Content-Type': 'application/x-protobuf',
        'Accept': 'application/x-protobuf',
    })

    message = None

    if method in ['POST', 'PUT']:
        message, validation_status = validate_protobuf_request(
                request_message, payload)

        if not validation_status:
            return {'errorMessage': message}

    response = requests.request(method=method, url=endpoint, data=message,
                                headers=headers, params=query_params)

    output = parse_response_data(response, response_message)

    return output
