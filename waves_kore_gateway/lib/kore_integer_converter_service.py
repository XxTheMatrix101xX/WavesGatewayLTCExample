"""
KORE Integer Converter Service
"""

from numbers import Number

import waves_gateway as gw
from decimal import Decimal


class KoreIntegerConverterService(gw.IntegerConverterService):
    """
    Implementation of an IntegerConverterService.
    Converts the Decimal values provided by the bitcoinrpc package into integers that can be processed
    by the Gateway.
    """

    def __init__(self, kore_factor: int, kore_round_precision: int) -> None:
        self._kore_factor = kore_factor
        self._kore_round_precision = kore_round_precision

    def convert_amount_to_int(self, amount: Decimal) -> int:
        return gw.convert_to_int(amount, self._kore_factor)

    def revert_amount_conversion(self, amount: int) -> Number:
        return gw.convert_to_decimal(amount, self._kore_factor, self._kore_round_precision)
