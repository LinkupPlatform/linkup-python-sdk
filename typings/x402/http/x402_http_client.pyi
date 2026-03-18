from ..client import x402Client, x402ClientSync

class x402HTTPClientSync:  # noqa: N801
    def __init__(self, client: x402ClientSync) -> None: ...
    def handle_402_response(
        self,
        headers: dict[str, str],
        body: bytes | None,
    ) -> tuple[dict[str, str], object]: ...

class x402HTTPClient:  # noqa: N801
    def __init__(self, client: x402Client) -> None: ...
    async def handle_402_response(
        self,
        headers: dict[str, str],
        body: bytes | None,
    ) -> tuple[dict[str, str], object]: ...
