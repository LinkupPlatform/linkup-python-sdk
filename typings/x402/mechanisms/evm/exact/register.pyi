from typing import TypeVar

from x402.client import x402Client, x402ClientSync
from x402.mechanisms.evm.signers import EthAccountSigner

ClientT = TypeVar("ClientT", x402Client, x402ClientSync)

def register_exact_evm_client(
    client: ClientT,
    signer: EthAccountSigner,
    networks: str | list[str] | None = None,
    policies: list[object] | None = None,
) -> ClientT: ...
