import asyncio
from datetime import datetime
from functools import wraps

import click
from babel.dates import format_datetime

from github.util import (
    get_current_deployment_id,
    get_repo_fallback,
    read_github_event_data,
)

PRODUCTION_ENVIRONMENTS = ("live",)
ORDERED_ENVIRONMENTS = ("dev", "test") + PRODUCTION_ENVIRONMENTS


def coroutine(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def click_repo_option(required: bool = True):
    return click.option(
        "-r",
        "--repo",
        envvar="GITHUB_REPOSITORY",
        required=required,
        default=get_repo_fallback(read_github_event_data()),
        help="Repository to use, e.g. moneymeets/ghd",
    )


def click_deployment_id_option():
    deployment_id = get_current_deployment_id()
    return click.option(
        "-d", "--deployment-id", type=int, required=deployment_id is None, default=deployment_id, help="Deployment ID",
    )


def localize_date(date: str, max_length: int = 0):
    result = format_datetime(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"))
    return result[:max_length] if max_length else result
