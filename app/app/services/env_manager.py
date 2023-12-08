"""
Handles environment variables.
This module will raise a key error if any of the required environment
variables are missing.
Import env variable from this module.
"""

import os
from typing import Any

ENV_NAMES = [
    'DJ_DB_NAME',
    'DJ_DB_USER',
    'DJ_DB_PASS',
    'DJ_DB_HOST',
    'DJ_DB_PORT',
    
    'ALLOWED_HOSTS',
    'CSRF_TRUSTED_ORIGINS',
]

ENVS: dict[str, Any] = {}
errs: list[Any] = []


def convert_env(env: str, value: str) -> Any:
    """Converts the environment variables to the correct type.

    Args:
        env (str): environment variable name
        value (str): environment variable value

    Returns:
        Any: converted value
    """
    match env:
        case 'DEBUG':
            return value.lower() == 'true'
        case 'ALLOWED_HOSTS':
            res = value.split(',')
            return [host.strip() for host in res if host != '']
        case 'CSRF_TRUSTED_ORIGINS':
            res = value.split(',')
            return [host.strip() for host in res if host != '']
        case _:
            return value


for env in ENV_NAMES:
    try:
        ENVS[env] = convert_env(env, os.environ[env])
    except KeyError as e:
        # TODO: TOBE REMOVED IN PRODUCTION
        errs.append(str(e).strip("'"))

if errs:
    raise EnvironmentError(f'Envs not found: {", ".join(errs)}')
