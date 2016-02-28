from jupyter_client import MultiKernelManager
from jupyter_client.kernelspec import KernelSpecManager

from kernel_client_manager import KernelClientManager
from exceptions.engine_errors import InvalidLanguageNameError


class KernelEngine:

    def __init__(self):
        spec_manager = KernelSpecManager()
        kernel_names = spec_manager.find_kernel_specs()

        self.available_kernel_names_mappings = {}

        for name in kernel_names:
            spec = spec_manager.get_kernel_spec(name)
            self.available_kernel_names_mappings[spec.display_name] = name

        self.manager = MultiKernelManager()

        self.client_managers = {}

    def __del__(self):
        self.manager.shutdown_all()

    def kernel_name_by_language(self, language):
        try:
            return self.available_kernel_names_mappings[language]
        except KeyError:
            raise InvalidLanguageNameError(language, self.available_kernel_names_mappings.keys())

    def get_client(self, language, context=None):
        kernel_name = self.kernel_name_by_language(language)

        try:
            manager = self.client_managers[kernel_name]
        except KeyError:
            manager = KernelClientManager(kernel_name, self.manager)
            self.client_managers[kernel_name] = manager

        return manager.client(context)

    def execute(self, language, code, context=None):
        client = self.get_client(language, context)
        return client.execute(code)

