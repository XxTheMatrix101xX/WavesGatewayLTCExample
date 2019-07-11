import unittest
from unittest.mock import MagicMock

from waves_kore_gateway.lib import KoreAddressFactory


class KoreAddressFactoryTest(unittest.TestCase):
    def setUp(self):
        self._kore_proxy = MagicMock()
        self._address_factory = KoreAddressFactory(self._kore_proxy)

    def test_create_address(self):
        expected_result = MagicMock()

        self._kore_proxy.getnewaddress.return_value = expected_result

        self.assertEqual(self._address_factory.create_address(), expected_result)

        self._kore_proxy.getnewaddress.assert_called_once_with()
