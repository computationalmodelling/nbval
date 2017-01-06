"""
pytest ipython plugin modification

Authors: D. Cortes, O. Laslett, T. Kluyver, H. Fangohr, V.T. Fauske

"""

import os

# Kernel for jupyter notebooks
from jupyter_client.manager import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
import ipykernel.kernelspec


CURRENT_ENV_KERNEL_NAME = ':nbval-parent-env'


class NbvalKernelspecManager(KernelSpecManager):
    """Kernel manager that also allows for python kernel in parent environment
    """

    def get_kernel_spec(self, kernel_name):
        """Returns a :class:`KernelSpec` instance for the given kernel_name.

        Raises :exc:`NoSuchKernel` if the given kernel name is not found.
        """
        if kernel_name == CURRENT_ENV_KERNEL_NAME:
            return self.kernel_spec_class(
                resource_dir=ipykernel.kernelspec.RESOURCES,
                **ipykernel.kernelspec.get_kernel_dict())
        else:
            return super().get_kernel_spec(kernel_name)


def start_new_kernel(startup_timeout=60, kernel_name='python', **kwargs):
    """Start a new kernel, and return its Manager and Client"""
    km = KernelManager(kernel_name=kernel_name,
                       kernel_spec_manager=NbvalKernelspecManager())
    km.start_kernel(**kwargs)
    kc = km.client()
    kc.start_channels()
    try:
        kc.wait_for_ready(timeout=startup_timeout)
    except RuntimeError:
        kc.stop_channels()
        km.shutdown_kernel()
        raise

    return km, kc


class RunningKernel(object):
    """
    Running a Kernel a Jupyter, info can be found at:
    http://jupyter-client.readthedocs.org/en/latest/messaging.html

    The purpose of this class is to encapsulate interaction with the
    jupyter kernel. Thus any changes on the jupyter side to how
    kernels are started/managed should not require any changes outside
    this class.

    """
    def __init__(self, kernel_name):
        """
        Initialise a new kernel
        specfiy that matplotlib is inline and connect the stderr.
        Stores the active kernel process and its manager.
        """

        self.km, self.kc = start_new_kernel(
            kernel_name=kernel_name,
            stderr=open(os.devnull, 'w'))

    def get_message(self, stream, timeout=None):
        """
        Function is used to get a message from the iopub channel.
        Timeout is None by default
        When timeout is reached
        """
        if stream == 'iopub':
            return self.kc.get_iopub_msg(timeout=timeout)
        elif stream == 'shell':
            return self.kc.get_shell_msg(timeout=timeout)

    def execute_cell_input(self, cell_input, allow_stdin=None):
        """
        Executes a string of python code in cell input.
        We do not allow the kernel to make requests to the stdin
             this is the norm for notebooks

        Function returns a unique message id of the reply from
        the kernel.
        """
        return self.kc.execute(cell_input, allow_stdin=allow_stdin)

    # These options are in case we wanted to restart the nb every time
    # it is executed a certain task
    def restart(self):
        """
        Instructs the kernel manager to restart the kernel process now.
        """
        self.km.restart_kernel(now=True)

    def stop(self):
        """
        Instructs the kernel process to stop channels
        and the kernel manager to then shutdown the process.
        """
        self.kc.stop_channels()
        self.km.shutdown_kernel(now=True)
        del self.km
