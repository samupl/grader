import subprocess
from tempfile import NamedTemporaryFile

from sshrpc.server import SSHRPCServerEndpoint, expose_method


class GraderEndpoint(SSHRPCServerEndpoint):
    @expose_method
    def grd_run(self, command, timeout=10):
        # Create temporary files for stdout/stderr
        std_out_file = NamedTemporaryFile(delete=False)
        std_err_file = NamedTemporaryFile(delete=False)

        # Call the command
        subprocess.Popen(
            args=command,
            stderr=std_err_file,
            stdout=std_out_file
        ).wait(timeout=timeout)

        # Reset file pointers
        std_out_file.seek(0)
        std_err_file.seek(0)

        # Read standard out/err
        std_out = std_out_file.read().decode()
        std_err = std_err_file.read().decode()

        # Return results for further serialisation
        return {
            'stdout': std_out,
            'stderr': std_err
        }


if __name__ == '__main__':
    se = GraderEndpoint()
    se.serve()
