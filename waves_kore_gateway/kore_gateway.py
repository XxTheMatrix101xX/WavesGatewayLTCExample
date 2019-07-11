"""
KoreGateway
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import List

import bitcoinrpc.authproxy as authproxy
import pymongo
import waves_gateway as wg

import waves_kore_gateway.lib as lib


class KoreGateway(object):
    """
    Implements a KORE Gateway.
    """

    DEFAULT_WAVES_CHAIN = "mainnet"
    DEFAULT_KORE_FACTOR = pow(10, 8) ######What is this?
    DEFAULT_KORE_ROUND_PRECISION = 8
    DEFAULT_TRANSACTION_WEB_LINK = "https://chainz.cryptoid.info/kore/tx.dws?{{tx}}.htm"
    DEFAULT_ADDRESS_WEB_LINK = "https://chainz.cryptoid.info/kore/tx.dws?{{tx}}.htm"
    DEFAULT_MONGO_DATABASE = "kore-gateway"
    WEB_CURRENCY_NAME = "Kore"
    WAVES_ASSET_ID = "HtuMVfunYhNpsqhFotXuwXvrC9wt6UD6ENdpQEQxtGAv" ####we need our own asset ID
    DEFAULT_PORT = 5000
    DEFAULT_HOST = 'localhost'

    def __init__(self,
                 config: wg.GatewayConfigFile,
                 kore_round_precision: int = DEFAULT_KORE_ROUND_PRECISION,
                 kore_factor: int = DEFAULT_KORE_FACTOR,
                 transaction_web_link: str = DEFAULT_TRANSACTION_WEB_LINK,
                 address_web_link: str = DEFAULT_ADDRESS_WEB_LINK) -> None:
        kore_proxy = wg.ProxyGuard(authproxy.AuthServiceProxy(config.coin_node), max_parallel_access=1)
        kore_address_factory = lib.KoreAddressFactory(kore_proxy)
        kore_chain_query_service = lib.KoreChainQueryService(kore_proxy)
        kore_transaction_service = lib.KoreTransactionService(kore_proxy, kore_chain_query_service)
        kore_integer_converter_service = lib.KoreIntegerConverterService(kore_factor, kore_round_precision)
        kore_address_validation_service = lib.KoreAddressValidationService(kore_proxy)
        mongo_client = pymongo.MongoClient(host=config.mongo_host, port=config.mongo_port)
        fee_service = wg.ConstantFeeServiceImpl(config.gateway_fee, config.coin_fee)

        logging_handlers = self._init_logging_handlers(config.environment)

        self._gateway = wg.Gateway(
            coin_address_factory=kore_address_factory,
            coin_chain_query_service=kore_chain_query_service,
            coin_transaction_service=kore_transaction_service,
            gateway_waves_address_secret=config.gateway_waves_address_secret,
            gateway_coin_address_secret=config.gateway_coin_address_secret,
            mongo_database=mongo_client.get_database(config.mongo_database),
            managed_loggers=["BitcoinRPC"],
            logging_handlers=logging_handlers,
            custom_currency_name=KoreGateway.WEB_CURRENCY_NAME,
            coin_integer_converter_service=kore_integer_converter_service,
            asset_integer_converter_service=wg.IntegerConverterService(),
            waves_chain=config.waves_chain,
            waves_asset_id=KoreGateway.WAVES_ASSET_ID,
            waves_node=config.waves_node,
            gateway_owner_address=config.gateway_owner_address,
            fee_service=fee_service,
            only_one_transaction_receiver=False,
            coin_transaction_web_link=transaction_web_link,
            coin_address_web_link=address_web_link,
            host=config.gateway_host,
            port=config.gateway_port,
            coin_address_validation_service=kore_address_validation_service,
            coin_last_block_distance=5)

    def _init_logging_handlers(self, environment: str) -> List[logging.Handler]:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s {%(name)s} - %(message)s")
        logging_handlers = []  # type: List[logging.Handler]

        if environment == "prod":
            file_handler = RotatingFileHandler("kore-gateway.log", maxBytes=10485760, backupCount=20, encoding='utf8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logging_handlers.append(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.WARN)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)
        elif environment == "debug":
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)
        elif environment == "test":
            pass
        else:
            raise Exception('Unknown environment ' + environment + '. Use prod or debug')

        return logging_handlers

    def run(self):
        self._gateway.run()

    def set_log_level(self, level):
        self._gateway.set_log_level(level)

    @staticmethod
    def from_config_file(file_content: str):
        parser = wg.INJECTOR.get(wg.GatewayConfigParser)
        parsed_config = parser.parse_config_file_content(file_content)
        return KoreGateway(config=parsed_config)
