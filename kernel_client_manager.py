from client_wrapper import ClientWrapper


class KernelClientManager:

    def __init__(self, kernel_name, manager):
        self.manager = manager
        self.uuid = manager.start_kernel(kernel_name)

        self.default_client = None
        self.clients = {}

    def kernel(self):
        return self.manager.get_kernel(self.uuid)

    def create_client(self):
        return ClientWrapper(self.kernel().client())

    def client(self, context=None):
        if context is None:
            if self.default_client is None:
                self.default_client = self.create_client()

            return self.default_client

        try:
            return self.clients[context]
        except KeyError:
            self.clients[context] = self.create_client()
            return self.clients[context]
