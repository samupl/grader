import jsonpickle

from lib.sshrpc.exceptions import RemoteMethodException


class SSHRPCClient:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def __dispach_method(self, method_name, *args, **kwargs):
        stdin, stdout, stderr = self.ssh_client.exec_command('python3 sshrpc_endpoint.py')
        stdin.write(method_name + '\n')
        client_args = [list(args), kwargs]
        client_args = jsonpickle.dumps(client_args)
        stdin.write(client_args + '\n')
        output = stdout.read()
        # print(output)
        result = jsonpickle.loads(output.decode("utf-8"))
        if result.get('failure'):
            tb = result.get('traceback')
            print('---- Traceback received from remote endpoint ----\n')
            print(tb)
            print('\n----\n')
            raise RemoteMethodException(result.get('exception_class'))
        self.ssh_client.close()
        return result.get('result')

    def __getattr__(self, item):
        def getattr_callback(*args, **kwargs):
            return self.__dispach_method(item, *args, **kwargs)
        return getattr_callback
