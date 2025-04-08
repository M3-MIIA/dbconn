import os
import json
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError

service = os.environ['SERVICE_NAME']
region_name = os.environ['DEPLOY_AWS_REGION']

def _parse_secret(secret_obj):
    return f"postgresql+psycopg://{secret_obj['username']}:{secret_obj['password']}@{secret_obj['host']}:{secret_obj['port']}/{secret_obj['dbname']}"


def _get_secret():

    secret_name = f"{service}/postgres"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value_response["SecretString"]

        if not secret_string:
            raise ValueError("Retrieved secret is empty")
        return json.loads(secret_string)

    except ClientError as e:
        error_message = f"Error retrieving secret '{secret_name}': {str(e)}"
        raise ClientError(e.response, e.operation_name) from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in secret: {str(e)}") from e

def get_secret():
    secret = _get_secret()
    return _parse_secret(secret)
