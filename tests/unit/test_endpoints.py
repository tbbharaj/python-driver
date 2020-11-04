# Copyright DataStax, Inc.
#
# Licensed under the DataStax DSE Driver License;
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
# http://www.datastax.com/terms/datastax-dse-driver-license-terms
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # noqa

import itertools

from cassandra.connection import (DefaultEndPoint, SniEndPoint, SniEndPointFactory,
                                  _HostnameEndPoint, _HostnameEndPointFactory)

from mock import patch


def socket_getaddrinfo(*args):
    return [
        (0, 0, 0, '', ('127.0.0.1', 30002)),
        (0, 0, 0, '', ('127.0.0.2', 30002)),
        (0, 0, 0, '', ('127.0.0.3', 30002))
    ]


@patch('socket.getaddrinfo', socket_getaddrinfo)
class HostnameEndPointTest(unittest.TestCase):

    endpoint_factory = _HostnameEndPointFactory("proxy.datastax.com", 30002)
    peer_row = {'peer': '10.0.0.1'}

    def test_hostname_endpoint_properties(self):

        endpoint = _HostnameEndPoint('proxy.datastax.com', 30002)
        self.assertEqual(endpoint.address, 'proxy.datastax.com')
        self.assertEqual(endpoint.port, 30002)
        self.assertIsNone(endpoint.resolved_address)
        self.assertEqual(str(endpoint), 'proxy.datastax.com:30002')

        endpoint = self.endpoint_factory.create(self.peer_row)
        self.assertEqual(endpoint.address, 'proxy.datastax.com')
        self.assertEqual(endpoint.port, 30002)
        self.assertEqual(endpoint.resolved_address, '10.0.0.1')
        self.assertEqual(str(endpoint), 'proxy.datastax.com:10.0.0.1:30002')

    def test_endpoint_equality(self):
        self.assertNotEqual(
            DefaultEndPoint('10.0.0.1'),
            self.endpoint_factory.create(self.peer_row)
        )

        self.assertEqual(
            self.endpoint_factory.create(self.peer_row),
            self.endpoint_factory.create(self.peer_row)
        )

        self.assertNotEqual(
            self.endpoint_factory.create(self.peer_row),
            self.endpoint_factory.create({'peer': '10.0.0.2'})
        )

        self.assertNotEqual(
            self.endpoint_factory.create(self.peer_row),
            SniEndPointFactory("proxy.datastax.com", 30002).create_from_sni('10.0.0.1')
        )

        self.assertNotEqual(
            self.endpoint_factory.create(self.peer_row),
            _HostnameEndPoint("proxy.datastax.com", 30002)
        )

        self.assertNotEqual(
            self.endpoint_factory.create(self.peer_row),
            _HostnameEndPoint("proxy.datastax.com", 9999, resolved_address='10.0.0.1')
        )

    def test_endpoint_resolve(self):
        endpoint = self.endpoint_factory.create(self.peer_row)
        for i in range(10):
            (address, _) = endpoint.resolve()
            self.assertEqual(address, '10.0.0.1')

    def test_multiple_endpoints_resolve(self):
        ips = ['127.0.0.1', '127.0.0.2', '127.0.0.3']
        it = itertools.cycle(ips)

        _HostnameEndPoint._offset = -1  # reset the class attr
        endpoint = _HostnameEndPoint('proxy.datastax.com')
        endpoint2 = _HostnameEndPoint('proxy.datastax.com')

        # endpoint will return the cached ip when resolved
        endpoint_ip = next(it)
        endpoint2_ip = next(it)
        for _ in range(10):
            self.assertEqual(endpoint.resolve()[0], endpoint_ip)
            self.assertEqual(endpoint2.resolve()[0], endpoint2_ip)

        self.assertEqual(_HostnameEndPoint('proxy.datastax.com').resolve()[0], next(it))


@patch('socket.getaddrinfo', socket_getaddrinfo)
class SniEndPointTest(unittest.TestCase):

    endpoint_factory = SniEndPointFactory("proxy.datastax.com", 30002)

    def test_sni_endpoint_properties(self):

        endpoint = self.endpoint_factory.create_from_sni('test')
        self.assertEqual(endpoint.address, 'proxy.datastax.com')
        self.assertEqual(endpoint.port, 30002)
        self.assertEqual(endpoint._server_name, 'test')
        self.assertEqual(str(endpoint), 'proxy.datastax.com:30002:test')

    def test_endpoint_equality(self):
        self.assertNotEqual(
            DefaultEndPoint('10.0.0.1'),
            self.endpoint_factory.create_from_sni('10.0.0.1')
        )

        self.assertNotEqual(
            _HostnameEndPoint('10.0.0.1'),
            self.endpoint_factory.create_from_sni('10.0.0.1')
        )

        self.assertEqual(
            self.endpoint_factory.create_from_sni('10.0.0.1'),
            self.endpoint_factory.create_from_sni('10.0.0.1')
        )

        self.assertNotEqual(
            self.endpoint_factory.create_from_sni('10.0.0.1'),
            self.endpoint_factory.create_from_sni('10.0.0.0')
        )

        self.assertNotEqual(
            self.endpoint_factory.create_from_sni('10.0.0.1'),
            SniEndPointFactory("proxy.datastax.com", 9999).create_from_sni('10.0.0.1')
        )
