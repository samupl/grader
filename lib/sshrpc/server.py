import traceback

import jsonpickle
import sys

from .exceptions import MethodNotRegistered


def expose_method(m):
    m.ssh_rpc_exposed = True
    return m


class SSHRPCServerEndpoint:
    def __init__(self):
        self.exposed_methods = []

    def call_exposed_method(self, method_name, *args, **kwargs):
        """
        This is a private method used to call every method that has been exposed by the endpoint.

        :param method_name:
        :type method_name: str
        :param args: Arguments that a method will be called with
        :type args: list or tuple
        :param kwargs: Keyword arguments that a method will be called with
        :type kwargs: dict
        """
        method = getattr(self, method_name)
        if not hasattr(method, 'ssh_rpc_exposed') and method.ssh_rpc_exposed:
            raise MethodNotRegistered('Method `{}` is not exposed within this endpoint'.format(method_name))
        return method(*args, **kwargs)

    @staticmethod
    def deserialize_arguments(args_serialized):
        """
        Provides a method to deserialize arguments provided by the endpoint client.

        :param args_serialized: arguments and keyword arguments serialized by the client
        :type args_serialized: str
        :return: Deserialized representation of the arguments
        :rtype: object
        """
        return jsonpickle.loads(args_serialized)

    @staticmethod
    def serialize_return_value(ret_value):
        """
        Serializes any python object using jsonpickle.

        :param ret_value: Any python object that is to be serialized
        :type ret_value: object
        :return: Serialized form of the object
        :rtype: str
        """
        return jsonpickle.encode(ret_value)

    @expose_method
    def ping_endpoint(self):
        """
        An example exposed endpoint, that returns True boolean value.

        :rtype: bool
        """
        return True

    def serve(self):
        method_name = input()
        args_serialized = input()
        if not args_serialized:
            args = [(), {}]
        else:
            args = self.deserialize_arguments(args_serialized)

        failure = False
        tb_str = None
        exception_class = None
        # noinspection PyBroadException
        try:
            result = self.call_exposed_method(method_name, *args[0], **args[1])
        except:
            failure = True
            exception, exception_class, exc_tb = sys.exc_info()
            tb_str = traceback.format_exc()
            result = None

        ret = {
            'failure': failure,
            'traceback': tb_str,
            'result': result,
            'exception_class': exception_class
        }
        print(self.serialize_return_value(ret))


if __name__ == '__main__':
    se = SSHRPCServerEndpoint()
    se.serve()
