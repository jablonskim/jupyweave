from client_wrapper import ClientWrapper


class KernelClientManager:

    def __init__(self, kernel_name, manager):
        self.manager = manager
        self.kernel_name = kernel_name
        self.default_uuid = manager.start_kernel(kernel_name)
        self.uuids = {}

        self.default_client = None
        self.clients = {}

    def kernel(self, context=None):
        return self.manager.get_kernel(self.default_uuid if context is None else self.uuids[context])

    def create_client(self, context=None):
        return ClientWrapper(self.kernel(context).client())

    def client(self, context=None):
        if context is None:
            if self.default_client is None:
                self.default_client = self.create_client()

            return self.default_client

        try:
            return self.clients[context]
        except KeyError:
            self.uuids[context] = self.manager.start_kernel(self.kernel_name)
            self.clients[context] = self.create_client(context)
            return self.clients[context]
