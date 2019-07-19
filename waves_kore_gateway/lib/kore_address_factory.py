"""
KORE Address Factory
"""

import waves_gateway as gw
from bitcoinrpc.authproxy import AuthServiceProxy


class KoreAddressFactory(gw.CoinAddressFactory):
    """
    Implements an AddressFactory using the getnewaddress function provided by the KORE client.
    """

    def __init__(self, kore_proxy: AuthServiceProxy) -> None:
        self._kore_proxy = kore_proxy

    def create_address(self) -> gw.CoinAddress:
        return self._kore_proxy.getnewaddress()
