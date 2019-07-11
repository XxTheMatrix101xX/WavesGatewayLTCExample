"""
Litecoin Gateway
"""
import gevent.monkey
gevent.monkey.patch_all()

from waves_kore_gateway import KoreGateway

file = open("config.cfg", "r")

gateway = KoreGateway.from_config_file(file.read())

gateway.run()
