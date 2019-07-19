"""
Kore Address Validation Service
"""

import waves_gateway as wg
from bitcoinrpc.authproxy import AuthServiceProxy


class KoreAddressValidationService(wg.AddressValidationService):
    """
    Validates a KORE address by using an RPC service.
    """

    def __init__(self, kore_proxy: AuthServiceProxy) -> None:
        self._kore_proxy = kore_proxy

    def validate_address(self, address: str) -> bool:
        validation_result = self._kore_proxy.validateaddress(address)
        return validation_result['isvalid']
