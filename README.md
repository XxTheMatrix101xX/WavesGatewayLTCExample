# Waves-Korecoin-Gateway

The project realizes a Kore-Gateway for the Wavesplatform.
To do that, it makes use of the Waves-Gateway-Framework.
Common logic of how a such an Gateway operates is already defined in the Framework.
This project does only define the logic that is necessary to communicate with a Kore node.

## Getting started

The requirements of this project are defined in the file: requirements.txt.
Please run the following command to install them:
```bash
pip3 install -r requirements.txt
```
This will also install the framework.

Developing requires additional packages to be installed:
```bash
pip3 install nose coverage yapf mypy pylint
```

You have to provide a configuration for the Waves-Korecoin-Gateway.
An example configuration may look like this:
```
# This can be used for local testing. Mostly be developers.

[node]
coin = http://******:******@localhost:20000
waves = https://testnode1.wavesnodes.com

[fee]
coin = 0.02000000
gateway = 0.01000000

[gateway_address]
owner = **********************************
waves_public_key = ***********************************
waves_private_key = ********************************************
coin_public_key = **********************************

[mongodb]
host = localhost
port = 27017
database = kore-gateway

[server]
host = localhost
port = 5000

[other]
waves_chain = testnet

# when using prod mode, file logging is enabled
environment = debug
```
This configuration file must be named `config.cfg` and be placed in the root directory.
You have to replace the addresses with your own ones.

The server can be started by calling: `python3.5 main.py`.

## Unittests
```bash
python3.5 -m nose waves_korecoin_gateway/test
```

## Coverage
```bash
python3.5 -m nose waves_korecoin_gateway/test --with-coverage --cover-package waves_korecoin_gateway
```

## Linting
```bash
python3.5 -m pylint main.py
python3.5 -m pylint waves_korecoin_gateway
```

## MyPy
```bash
python3.5 -m mypy main.py --ignore-missing-imports
python3.5 -m mypy waves_korecoin_gateway --ignore-missing-imports
```

## yapf
This project uses yapf (https://github.com/google/yapf) as a formatting tool
So, please format your code before committing by running this:
```bash
python3.5 -m yapf -r waves_korecoin_gateway --style pep8 --style {COLUMN_LIMIT:120} -i
python3.5 -m yapf --style pep8 --style {COLUMN_LIMIT:120} -i main.py
```
