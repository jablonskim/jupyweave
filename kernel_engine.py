from jupyter_client import MultiKernelManager
from jupyter_client.kernelspec import KernelSpecManager


class KernelEngine:

    def __init__(self):
        spec_manager = KernelSpecManager()
        kernel_names = spec_manager.find_kernel_specs()

        self.available_kernel_names_mappings = {}

        for name in kernel_names:
            spec = spec_manager.get_kernel_spec(name)
            self.available_kernel_names_mappings[spec.display_name] = name

        print(self.available_kernel_names_mappings)

        self.manager = MultiKernelManager()

    def __del__(self):
        # TODO
        pass

    def get_kernel(self, language):
        pass

    def get_client(self, language, context=None):
        pass

    def execute(self, language, code, context=None):
        return ''
