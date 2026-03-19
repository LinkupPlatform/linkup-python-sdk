"""x402 payment protocol signer for the Linkup SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from eth_account.signers.local import LocalAccount


@runtime_checkable
class LinkupX402Signer(Protocol):
    def create_payment_headers(
        self,
        response_headers: dict[str, str],
        response_body: bytes,
    ) -> dict[str, str]: ...  # pragma: no cover

    async def async_create_payment_headers(
        self,
        response_headers: dict[str, str],
        response_body: bytes,
    ) -> dict[str, str]: ...  # pragma: no cover


class _DefaultX402Signer:
    def __init__(self, account: LocalAccount, network: str) -> None:
        try:
            from x402 import x402Client, x402ClientSync
            from x402.http import x402HTTPClient, x402HTTPClientSync
            from x402.mechanisms.evm import EthAccountSigner
            from x402.mechanisms.evm.exact.register import register_exact_evm_client
        except ImportError as e:
            raise ImportError(
                "The x402 optional dependencies are required to use x402 payment. "
                "Install them with: pip install 'linkup-sdk[x402]'"
            ) from e

        signer = EthAccountSigner(account)

        sync_client = x402ClientSync()
        register_exact_evm_client(sync_client, signer, networks=network)
        self._sync_http_client = x402HTTPClientSync(sync_client)

        async_client = x402Client()
        register_exact_evm_client(async_client, signer, networks=network)
        self._async_http_client = x402HTTPClient(async_client)

    def create_payment_headers(
        self,
        response_headers: dict[str, str],
        response_body: bytes,
    ) -> dict[str, str]:
        payment_headers, _ = self._sync_http_client.handle_402_response(
            response_headers, response_body
        )
        return payment_headers

    async def async_create_payment_headers(
        self,
        response_headers: dict[str, str],
        response_body: bytes,
    ) -> dict[str, str]:
        payment_headers, _ = await self._async_http_client.handle_402_response(
            response_headers, response_body
        )
        return payment_headers


def create_x402_signer(
    account: LocalAccount,
    network: str = "eip155:8453",
) -> _DefaultX402Signer:
    """Create an x402 signer using the x402 Python package with EVM (Base chain).

    Args:
        account: An eth_account LocalAccount instance used to sign payments.
        network: The CAIP-2 network identifier. Only Base mainnet ("eip155:8453") is supported.

    Returns:
        A signer instance that implements the LinkupX402Signer protocol.

    Raises:
        ImportError: If the x402 optional dependencies are not installed.
    """
    return _DefaultX402Signer(account=account, network=network)
