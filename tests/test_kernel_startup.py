import pytest

from nbval.kernel import start_new_kernel


def kernel_managers(mocker, dying):
    """Replace KernelManager by mocks whose first `dying` kernels die."""
    managers = []

    def new_kernel_manager(**kwargs):
        km = mocker.Mock()
        if len(managers) < dying:
            km.client.return_value.wait_for_ready.side_effect = RuntimeError(
                'Kernel died before replying to kernel_info')
        managers.append(km)
        return km

    mocker.patch('nbval.kernel.KernelManager', side_effect=new_kernel_manager)
    return managers


def test_a_kernel_that_dies_is_replaced(mocker):
    managers = kernel_managers(mocker, dying=1)

    km, kc = start_new_kernel(startup_retries=1)

    assert km is managers[1]
    managers[0].shutdown_kernel.assert_called_once()


def test_the_error_is_raised_when_all_kernels_die(mocker):
    managers = kernel_managers(mocker, dying=2)

    with pytest.raises(RuntimeError, match='Kernel died'):
        start_new_kernel(startup_retries=1)

    assert len(managers) == 2
