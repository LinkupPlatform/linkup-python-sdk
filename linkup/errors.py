class LinkupInvalidRequestError(Exception):
    """Invalid request error, raised when the Linkup API returns a 400 status code.

    It is returned by the Linkup API when the request is invalid, typically when a mandatory
    parameter is missing.
    """

    def __str__(self) -> str:
        return (
            "The Linkup API returned an invalid request error (400). Make sure the parameters "
            "you are using are valid (e.g. when using a structured_output_schema, it must "
            "represent a valid object, with 'type': 'object') and you are using the latest "
            f"version of the Python SDK. Original error message: {', '.join(self.args)}."
        )


class LinkupAuthenticationError(Exception):
    """Authenfication error, raised when the Linkup API returns a 403 status code.

    It is returned when there is an authenfication issue or when the user doesn't have anymore
    credits.
    """

    def __str__(self) -> str:
        return (
            f"The Linkup API returned an authentication error (403). Make sure your API key is "
            f"valid and has enough credits. Original error message: {', '.join(self.args)}."
        )


class LinkupUnknownError(Exception):
    """Unknown error, raised when the Linkup API returns an unknown status code."""

    def __str__(self) -> str:
        return (
            f"The Linkup API returned an unknown error. Original error message: "
            f"{', '.join(self.args)}."
        )
