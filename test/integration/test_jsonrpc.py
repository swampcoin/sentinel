import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from vecod import VecoDaemon
from veco_config import VecoConfig


def test_vecod():
    config_text = VecoConfig.slurp_config_file(config.veco_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000003fd1dff397d1be86183efd9e13f0316b5f5a3082bac91975a421bc43021'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bafbc94add76cb75e2ec92894837288a481e5c005f6563d91623bf8bc2c'

    creds = VecoConfig.get_rpc_creds(config_text, network)
    vecod = VecoDaemon(**creds)
    assert vecod.rpc_command is not None

    assert hasattr(vecod, 'rpc_connection')

    # Veco testnet block 0 hash == 00000997e30aad936446ab7226cecd21875e867a57aca1a46d17be4316bab391
    # test commands without arguments
    info = vecod.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert vecod.rpc_command('getblockhash', 0) == genesis_hash
