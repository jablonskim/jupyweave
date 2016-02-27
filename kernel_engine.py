from jupyter_client import MultiKernelManager
from jupyter_client.kernelspec import KernelSpecManager

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

        self.kernels_uuids = {}

    def __del__(self):
        self.manager.shutdown_all()

    def kernel_name_by_language(self, language):
        try:
            return self.available_kernel_names_mappings[language]
        except KeyError:
            raise InvalidLanguageNameError(language, self.available_kernel_names_mappings.keys())

    def get_kernel(self, language):
        kernel_name = self.kernel_name_by_language(language)

        try:
            uuid = self.kernels_uuids[kernel_name]
        except KeyError:
            uuid = self.manager.start_kernel(kernel_name)
            self.kernels_uuids[kernel_name] = uuid

        # TODO: if not in manager (dead etc)?

        return self.manager.get_kernel(uuid)

    def get_client(self, language, context=None):
        pass

    def execute(self, language, code, context=None):
        return ''
