class LinkupInvalidRequestError(Exception):
    """Invalid request error, raised when the Linkup API returns a 400 status code.

    It is returned by the Linkup API when the request is invalid, typically when a mandatory
    parameter is missing, or isn't valid (type, structure, etc.)
    """

    pass


class LinkupAuthenticationError(Exception):
    """Authenfication error, raised when the Linkup API returns a 403 status code.

    It is returned when there is an authenfication issue, typically when the API key is not valid
    or when the user has exhausted its credits.
    """

    pass


class LinkupUnknownError(Exception):
    """Unknown error, raised when the Linkup API returns an unknown status code."""

    pass
