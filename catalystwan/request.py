# Copyright 2024 Cisco Systems, Inc. and its affiliates
from logging import getLogger
from typing import Callable, Tuple, Type, TypeVar

from requests import delete, get, head, options, patch, post, put, request
from requests.exceptions import ConnectionError, Timeout
from typing_extensions import Concatenate, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")
logger = getLogger(__name__)


def retry(function: Callable[P, T], catch: Tuple[Type[Exception], ...]) -> Callable[Concatenate[int, P], T]:
    def decorator(retries: int, *args: P.args, **kwargs: P.kwargs) -> T:
        for _ in range(retries):
            try:
                return function(*args, **kwargs)
            except catch as e:
                logger.warning(f"Retrying: {e}")
        return function(*args, **kwargs)

    return decorator


# retry decorators for request methods, retries count added as first positional argument
catch = (ConnectionError, Timeout)
retry_request = retry(request, catch)
retry_get = retry(get, catch)
retry_options = retry(options, catch)
retry_head = retry(head, catch)
retry_post = retry(post, catch)
retry_put = retry(put, catch)
retry_patch = retry(patch, catch)
retry_delete = retry(delete, catch)
