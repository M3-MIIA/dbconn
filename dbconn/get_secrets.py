import os
import json
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError


def _parse_secret(secret_obj: Dict[str, Any]) -> str:
    try:
        return (f"postgresql+psycopg://{secret_obj['username']}:{secret_obj['password']}@"
                f"{secret_obj['host']}:{secret_obj['port']}/{secret_obj['dbname']}")
    except KeyError as e:
        raise KeyError(f"Missing required database parameter in secret: {e}") from e


def _get_secret(secret_name: Optional[str] = None, region_name: Optional[str] = None) -> Dict[str, Any]:
    try:
        secret_name = secret_name or os.environ['MIIA_DBCONN_SECRET_NAME']
    except KeyError as e:
        raise EnvironmentError(f"{e} environment variable is required")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")

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

def get_secret(secret_name: Optional[str] = None, region_name: Optional[str] = None) -> str:
    secret = _get_secret(secret_name=secret_name, region_name=region_name)
    return _parse_secret(secret)
