from jupyter_client import MultiKernelManager
from jupyter_client.kernelspec import KernelSpecManager

from exceptions.engine_errors import InvalidLanguageNameError
from core.kernel_client_manager import KernelClientManager


class KernelEngine:
    """Manages kernels for one document"""

    def __init__(self, settings, document_language):
        """Initializes available kernel names"""
        self.__settings = settings
        self.__doc_lang = document_language

        spec_manager = KernelSpecManager()
        kernel_names = spec_manager.find_kernel_specs()

        self.__available_kernel_names_mappings = {}

        for name in kernel_names:
            spec = spec_manager.get_kernel_spec(name)
            self.__available_kernel_names_mappings[spec.display_name] = name

        self.__manager = MultiKernelManager()

        self.__client_managers = {}

    def __del__(self):
        """Safe kernels shutdown"""
        self.__manager.shutdown_all()

    def execute(self, language, code, context, processing_manager, output_types=None, timeout=None, allow_errors=False):
        """Executes code in specified language within specified context"""
        client = self.__get_client(language, context)
        return client.execute(code, processing_manager, output_types, timeout, allow_errors)

    def __kernel_name_by_language(self, language):
        try:
            return self.__available_kernel_names_mappings[language]
        except KeyError:
            raise InvalidLanguageNameError(language, self.__available_kernel_names_mappings.keys())

    def __get_client(self, language, context=None):
        kernel_name = self.__kernel_name_by_language(language)

        try:
            manager = self.__client_managers[kernel_name]
        except KeyError:
            manager = KernelClientManager(kernel_name, language, self.__doc_lang, self.__manager,
                                          self.__settings.timeout(language))
            self.__client_managers[kernel_name] = manager

        return manager.client(context)
