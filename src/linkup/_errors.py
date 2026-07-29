"""Linkup custom errors."""


class LinkupInvalidRequestError(Exception):
    """Invalid request error, raised when the Linkup API returns a 400 status code.

    It is returned by the Linkup API when the request is invalid, typically when a mandatory
    parameter is missing, or isn't valid (type, structure, etc.).
    """

    pass


class LinkupNoResultError(Exception):
    """No result error, raised when the Linkup API returns a 400 status code.

    It is returned by the Linkup API when the search query did not yield any result.
    """

    pass


class LinkupAuthenticationError(Exception):
    """Authentication error, raised when the Linkup API returns a 401 or 403 status code.

    It is returned when there is an authentication issue, typically when the API key is not valid.
    """

    pass


class LinkupPaymentRequiredError(Exception):
    """Payment required error, raised when the Linkup API returns a 402 status code.

    It is returned when the endpoint requires x402 payment and either no signer is
    configured, or the payment attempt failed.
    """

    pass


class LinkupInsufficientCreditError(Exception):
    """Insufficient credit error, raised when the Linkup API returns a 429 status code.

    It is returned when you have run out of credits.
    """

    pass


class LinkupTooManyRequestsError(Exception):
    """Too many requests error, raised when the Linkup API returns a 429 status code.

    It is returned when you are sending too many requests at a time.
    """

    pass


class LinkupFailedFetchError(Exception):
    """Failed fetch error, raised when the Linkup API search returns a 400 status code.

    It is returned when the Linkup API failed to fetch the content of an URL due to technical
    reasons.
    """

    pass


class LinkupFetchResponseTooLargeError(Exception):
    """Fetch response too large error, raised when the Linkup API search returns a 400 status code.

    It is returned when the Linkup API can't return the full response because it is too large.
    """

    pass


class LinkupFetchTargetUnreachableError(Exception):
    """Fetch target unreachable error, raised when the Linkup API returns a 400 status code.

    It is returned when the Linkup API cannot connect to the requested target URL, such as when
    the host is unreachable or the request times out before a response is received.
    """

    pass


class LinkupFetchUnsupportedContentTypeError(Exception):
    """Unsupported fetch content type error, raised when the Linkup API returns a 400 status code.

    It is returned when the URL resolves to a content type that Linkup cannot convert into a web
    page response.
    """

    pass


class LinkupFetchUrlIsFileError(LinkupFetchUnsupportedContentTypeError):
    """Backward-compatible alias for unsupported fetch content type errors.

    Older Linkup API deployments could report this case as a file URL. Current deployments return
    the more general unsupported content type error instead.
    """

    pass


class LinkupBudgetLimitExceededError(Exception):
    """Budget limit exceeded error, raised when the Linkup API returns a 429 status code.

    It is returned when the API key has reached its configured budget limit.
    """

    pass


class LinkupTasksQueueLimitExceededError(Exception):
    """Tasks queue limit exceeded error, raised when the Linkup API returns a 429 status code.

    It is returned when too many tasks are already pending or processing for the organization.
    """

    pass


class LinkupTaskNotFoundError(Exception):
    """Task not found error, raised when the Linkup API returns a 404 status code.

    It is returned when a task or research task identifier does not exist.
    """

    pass


class LinkupTimeoutError(Exception):
    """Timeout error, raised when the HTTP request to the Linkup API times out.

    It is raised when a timeout is specified and the request exceeds the given duration.
    """

    pass


class LinkupUnknownError(Exception):
    """Unknown error, raised when the Linkup API returns an unknown status code."""

    pass


class LinkupUnsupportedTaskTypeError(Exception):
    """Unsupported task type error, raised when a task type is not supported by this SDK."""

    pass
