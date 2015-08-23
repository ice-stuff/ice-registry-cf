#!/usr/bin/env python
import os
import re
import json

from ice import rest_api
from ice import config
from ice import logging


def _get_mongodb_config():
    try:
        services = json.loads(os.environ['VCAP_SERVICES'])
        uri = services['mongolab'][0]['credentials']['uri']
    except Exception as err:
        raise Exception('getting MongoDB URI: %s' % str(err))

    g = re.match(
        '^mongodb\://(.*):(.*)@(.*):([0-9]*)\/(.*)$', uri
    )
    if g is None:
        raise Exception('parsing MongoDB URI: %s' % uri)

    return """[mongodb]
host = %(hostname)s
port = %(port)d
username = %(username)s
password = %(password)s
db_name = %(db_name)s
""" % {
        "username": g.group(1),
        "password": g.group(2),
        "hostname": g.group(3),
        "port": int(g.group(4)),
        "db_name": g.group(5)
    }


def _get_registry_config():
    cfg = ''

    if 'VCAP_APP_PORT' in os.environ:
        port = int(os.environ['VCAP_APP_PORT'])
        cfg += """[api_server]
port = %d
""" % port

    cfg += _get_mongodb_config()

    return cfg


def _set_config():
    cfg = _get_registry_config()

    dir_path = os.path.expanduser("~/.ice")
    os.mkdir(dir_path)

    f = open(os.path.join(dir_path, "ice.ini"), "w")
    f.write(cfg)
    f.close()


def main():
    # Set config from CF environment
    _set_config()

    # Make the API server
    api = rest_api.APIServer()

    # Is verbose?
    _cfg = config.get_configuration('api_sever')
    if _cfg.get_bool('api_server', 'debug', False):
        # Set root logger to debug
        root_logger = logging.get_logger('ice')
        root_logger.setLevel(logging.DEBUG)
        root_logger.debug('Setting log level to DEBUG')

    # Start the API server
    api.run()


if __name__ == '__main__':
    main()
