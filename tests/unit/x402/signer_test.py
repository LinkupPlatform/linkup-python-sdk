import builtins
import sys
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock

import pytest

from linkup.x402._signer import LinkupX402Signer, _DefaultX402Signer, create_x402_signer


def _setup_x402_mocks(monkeypatch: pytest.MonkeyPatch) -> dict[str, MagicMock]:
    """Set up mock modules for x402 dependencies and return key mocks."""
    mock_account = MagicMock()

    mock_signer_instance = MagicMock()
    mock_evm_signer_class = MagicMock(return_value=mock_signer_instance)

    mock_sync_x402_client = MagicMock()
    mock_async_x402_client = MagicMock()
    mock_sync_x402_client_class = MagicMock(return_value=mock_sync_x402_client)
    mock_async_x402_client_class = MagicMock(return_value=mock_async_x402_client)

    mock_sync_http_client = MagicMock()
    mock_async_http_client = MagicMock()
    mock_sync_http_class = MagicMock(return_value=mock_sync_http_client)
    mock_async_http_class = MagicMock(return_value=mock_async_http_client)

    mock_register = MagicMock()

    # Create mock modules
    mock_x402 = ModuleType("x402")
    mock_x402.x402Client = mock_async_x402_client_class  # type: ignore[attr-defined]
    mock_x402.x402ClientSync = mock_sync_x402_client_class  # type: ignore[attr-defined]

    mock_x402_http = ModuleType("x402.http")
    mock_x402_http.x402HTTPClient = mock_async_http_class  # type: ignore[attr-defined]
    mock_x402_http.x402HTTPClientSync = mock_sync_http_class  # type: ignore[attr-defined]

    mock_x402_mechanisms = ModuleType("x402.mechanisms")
    mock_x402_mechanisms_evm = ModuleType("x402.mechanisms.evm")
    mock_x402_mechanisms_evm.EthAccountSigner = mock_evm_signer_class  # type: ignore[attr-defined]

    mock_x402_exact = ModuleType("x402.mechanisms.evm.exact")
    mock_x402_exact_register = ModuleType("x402.mechanisms.evm.exact.register")
    mock_x402_exact_register.register_exact_evm_client = mock_register  # type: ignore[attr-defined]

    modules = {
        "x402": mock_x402,
        "x402.http": mock_x402_http,
        "x402.mechanisms": mock_x402_mechanisms,
        "x402.mechanisms.evm": mock_x402_mechanisms_evm,
        "x402.mechanisms.evm.exact": mock_x402_exact,
        "x402.mechanisms.evm.exact.register": mock_x402_exact_register,
    }
    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    return {
        "account": mock_account,
        "evm_signer_class": mock_evm_signer_class,
        "signer_instance": mock_signer_instance,
        "sync_x402_client_class": mock_sync_x402_client_class,
        "async_x402_client_class": mock_async_x402_client_class,
        "sync_http_class": mock_sync_http_class,
        "async_http_class": mock_async_http_class,
        "sync_http_client": mock_sync_http_client,
        "async_http_client": mock_async_http_client,
        "register": mock_register,
    }


def test_create_x402_signer(monkeypatch: pytest.MonkeyPatch) -> None:
    mocks = _setup_x402_mocks(monkeypatch)

    signer = create_x402_signer(mocks["account"])

    mocks["evm_signer_class"].assert_called_once_with(mocks["account"])
    assert mocks["register"].call_count == 2  # sync + async
    mocks["sync_http_class"].assert_called_once()
    mocks["async_http_class"].assert_called_once()
    assert isinstance(signer, _DefaultX402Signer)


def test_create_x402_signer_missing_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    blocked = (
        "x402",
        "x402.http",
        "x402.mechanisms.evm",
        "x402.mechanisms.evm.exact.register",
    )
    for name in blocked:
        monkeypatch.delitem(sys.modules, name, raising=False)

    original_import = builtins.__import__

    def mock_import(name: str, *args: object, **kwargs: object) -> object:
        if name in blocked:
            raise ImportError(f"No module named '{name}'")
        return original_import(name, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(builtins, "__import__", mock_import)

    with pytest.raises(ImportError, match="x402 optional dependencies"):
        create_x402_signer(MagicMock())


def test_default_signer_create_payment_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    mocks = _setup_x402_mocks(monkeypatch)
    mocks["sync_http_client"].handle_402_response.return_value = (
        {"X-Payment": "signed"},
        MagicMock(),
    )

    signer = create_x402_signer(mocks["account"])
    headers = signer.create_payment_headers(
        response_headers={"X-Payment-Required": "true"},
        response_body=b"payment details",
    )

    assert headers == {"X-Payment": "signed"}
    mocks["sync_http_client"].handle_402_response.assert_called_once_with(
        {"X-Payment-Required": "true"}, b"payment details"
    )


@pytest.mark.asyncio
async def test_default_signer_async_create_payment_headers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mocks = _setup_x402_mocks(monkeypatch)
    mocks["async_http_client"].handle_402_response = AsyncMock(
        return_value=({"X-Payment": "signed"}, MagicMock())
    )

    signer = create_x402_signer(mocks["account"])
    headers = await signer.async_create_payment_headers(
        response_headers={"X-Payment-Required": "true"},
        response_body=b"payment details",
    )

    assert headers == {"X-Payment": "signed"}
    mocks["async_http_client"].handle_402_response.assert_called_once_with(
        {"X-Payment-Required": "true"}, b"payment details"
    )


def test_linkup_x402_signer_protocol() -> None:
    class MySigner:
        def create_payment_headers(
            self, response_headers: dict[str, str], response_body: bytes
        ) -> dict[str, str]:
            return {}

        async def async_create_payment_headers(
            self, response_headers: dict[str, str], response_body: bytes
        ) -> dict[str, str]:
            return {}

    assert isinstance(MySigner(), LinkupX402Signer)
