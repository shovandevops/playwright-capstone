import json
from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse
from playwright.sync_api import Error as PlaywrightError

from utils.logger import get_logger, log_debug, log_error, log_step, log_warning

MAX_LOGGED_BODY_CHARS = 500


class ApiClientError(Exception):
    """Raised when an API request fails or returns an unusable response."""

    def __init__(self, message: str, status: int | None = None, url: str | None = None):
        super().__init__(message)
        self.status = status
        self.url = url


class BaseApiClient:
    """Shared request, logging and response-parsing behaviour for API clients."""

    endpoint = ""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context
        self.logger = get_logger(self.__class__.__name__)
        log_step(self.logger, f"{self.__class__.__name__} initialized")

    def _send(self, method: str, path: str, **kwargs: Any) -> APIResponse:
        """
        Sends a request, logs the outcome and returns the raw response.
        Network/transport failures are wrapped in ApiClientError; HTTP error
        statuses are logged as warnings and returned so tests can assert on them.
        """
        log_step(self.logger, f"{method.upper()} {path}")
        try:
            response = getattr(self.request, method)(path, **kwargs)
        except PlaywrightError as error:
            log_error(self.logger, f"{method.upper()} {path} failed: {error}")
            raise ApiClientError(f"{method.upper()} {path} failed: {error}", url=path) from error

        log_step(self.logger, f"{method.upper()} {path} -> {response.status}")
        if not response.ok:
            log_warning(self.logger, f"{method.upper()} {path} returned HTTP {response.status}")
        log_debug(self.logger, f"Response body: {self._body_preview(response)}")
        return response

    @staticmethod
    def parse_json(response: APIResponse) -> Any:
        """
        Returns the decoded JSON body, or None when the body is empty.
        Raises ApiClientError with the status and a body preview if the
        body is not valid JSON.
        """
        text = response.text()
        if not text.strip():
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError as error:
            raise ApiClientError(
                f"Response from {response.url} is not valid JSON "
                f"(HTTP {response.status}): {text[:MAX_LOGGED_BODY_CHARS]}",
                status=response.status,
                url=response.url,
            ) from error

    def ensure_ok(self, response: APIResponse, action: str) -> None:
        """Raises ApiClientError when the response status is not 2xx."""
        if not response.ok:
            message = f"Failed to {action}: HTTP {response.status} from {response.url}"
            log_error(self.logger, message)
            raise ApiClientError(message, status=response.status, url=response.url)

    @staticmethod
    def _body_preview(response: APIResponse) -> str:
        """Returns a truncated body for DEBUG logging; never raises."""
        try:
            text = response.text()
        except PlaywrightError:
            return "<body unavailable>"
        if not text:
            return "<empty>"
        if len(text) > MAX_LOGGED_BODY_CHARS:
            return f"{text[:MAX_LOGGED_BODY_CHARS]}... ({len(text)} chars)"
        return text
