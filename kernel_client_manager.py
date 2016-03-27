from client_wrapper import ClientWrapper


class KernelClientManager:
    """Manages clients for specified kernel and contexts"""

    def __init__(self, kernel_name, language, doc_language, manager, execution_timeout, results_patterns, output_manager):
        """Initializes kernel for default context"""
        self.__execution_timeout = execution_timeout
        self.__results_patterns = results_patterns
        self.__output_manager = output_manager
        self.__doc_lang = doc_language
        self.__manager = manager
        self.__kernel_name = kernel_name
        self.__language = language
        self.__default_uuid = manager.start_kernel(kernel_name)
        self.__uuids = {}

        self.__default_client = None
        self.__clients = {}

    def client(self, context=None):
        """Returns client for specific context"""
        if context is None:
            if self.__default_client is None:
                self.__default_client = self.__create_client()

            return self.__default_client

        try:
            return self.__clients[context]
        except KeyError:
            self.__uuids[context] = self.__manager.start_kernel(self.__kernel_name)
            self.__clients[context] = self.__create_client(context)
            return self.__clients[context]

    def __kernel(self, context=None):
        return self.__manager.get_kernel(self.__default_uuid if context is None else self.__uuids[context])

    def __create_client(self, context=None):
        return ClientWrapper(self.__kernel(context).client(), self.__language, self.__doc_lang, self.__execution_timeout,
                             self.__results_patterns, self.__output_manager)
