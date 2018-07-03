import requests
from flask import current_app as app
from functools import reduce
import urllib
import os
import subprocess
import importlib
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

    all_protofiles = reduce(lambda a, x: a + x, externals.values(), [])
    all_protofile_urls = [datum.get('file_path')
                          for datum in all_protofiles]

    for url in all_protofile_urls:
        file_name = url.split('/')[-1]
        file_path = os.path.join(protofiles_dir, file_name)

        urllib.request.urlretrieve(url, file_path)


def validate_protobuf_request(message_name, payload):
    """
    validates the protobuf validations
    """

    module = importlib.import_module('descriptors')
    descriptor = getattr(module, message_name)

    try:
        descriptor(**payload)
    except Exception as exc:
        logger.error('Validation failed for {} with payload {}'.format(
            message_name, payload
        ))

        return repr(exc)


def perform_microservice_request(method, endpoint, payload={},
                                 query_params={}, headers={},
                                 message_name=''):
    """
    this function performs the microservice requests
    given certain parameters and returns the output
    of the request along with the status code. this
    will also start using the protobuf which will be
    common while validating the data to be sent to the
    service
    """

    if method == 'GET':
        response = requests.get(endpoint, params=query_params,
                                headers=headers)

        try:
            return response.json(), response.status_code
        except Exception:
            return {}, response.status_code

    if method == 'POST':
        if message_name:
            response = validate_protobuf_request(message_name, payload)

            return {'errorMessage': response}, 400

        if 'Content-Type' not in headers:
            headers.update({'Content-Type': 'application/json'})

        response = requests.post(endpoint, data=payload,
                                 headers=headers)

        try:
            return response.json(), response.status_code
        except Exception:
            return {}, response.status_code
