import os
import re
import json
import logging
from ice.registry import server
from ice.registry.server import domain


def _get_mongodb_config():
    try:
        services = json.loads(os.environ['VCAP_SERVICES'])
        uri = services['mlab'][0]['credentials']['uri']
    except Exception as err:
        raise Exception('getting MongoDB URI: %s' % str(err))

    g = re.match(
        '^mongodb\://(.*):(.*)@(.*):([0-9]*)\/(.*)$', uri
    )
    if g is None:
        raise Exception('parsing MongoDB URI: %s' % uri)

    return {
        "username": g.group(1),
        "password": g.group(2),
        "hostname": g.group(3),
        "port": int(g.group(4)),
        "db_name": g.group(5)
    }


def _get_logger():
    logger = logging.getLogger('ice.registry-server')

    formatter = logging.Formatter(
        '%(asctime)s [%(name)s] %(levelname)s :: %(message)s'
    )

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger


def main():
    logger = _get_logger()
    logger.setLevel(logging.DEBUG)

    mongo = _get_mongodb_config()
    server.RegistryServer(
        server.CfgRegistryServer(
            host='0.0.0.0',
            port=int(os.environ['PORT']),
            mongo_host=mongo['hostname'],
            mongo_port=mongo['port'],
            mongo_db=mongo['db_name'],
            mongo_user=mongo['username'],
            mongo_pass=mongo['password'],
            debug=True
        ),
        [
            domain.instances.InstancesDomain(),
            domain.sessions.SessionsDomain()
        ],
        logger
    ).run()


if __name__ == '__main__':
    main()
