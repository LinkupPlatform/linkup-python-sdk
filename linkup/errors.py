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
    """Authentication error, raised when the Linkup API returns a 403 status code.

    It is returned when there is an authentication issue, typically when the API key is not valid.
    """

    pass


class LinkupInsufficientCreditError(Exception):
    """Insufficient credit error, raised when the Linkup API returns a 429 status code.

    It is returned when you have run out of credits.
    """

    pass


class LinkupUnknownError(Exception):
    """Unknown error, raised when the Linkup API returns an unknown status code."""

    pass
