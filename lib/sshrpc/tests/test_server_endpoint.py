import unittest

from lib.sshrpc.server import SSHRPCServerEndpoint, expose_method


class TestServerEndpoint(SSHRPCServerEndpoint):
    @expose_method
    def example_method(self, number):
        return number + 1


class ServerEndpointTestCase(unittest.TestCase):
    def test_method_call_method_ping_endpoint(self):
        """ Check if the default `ping_endpoint` callable is accessible using call_exposed_method. """
        se = SSHRPCServerEndpoint()
        self.assertTrue(se.call_exposed_method('ping_endpoint'))

    def test_method_call_method(self):
        """ Check if an exposed callable is accessible using call_exposed_method. """
        se = TestServerEndpoint()
        self.assertEqual(se.call_exposed_method('example_method', 2), 3)
