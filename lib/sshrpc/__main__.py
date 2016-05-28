from .server import SSHRPCServerEndpoint


class GraderSSHRPCEndpoint(SSHRPCServerEndpoint):
    pass


if __name__ == '__main__':
    se = GraderSSHRPCEndpoint()
    se.serve()
