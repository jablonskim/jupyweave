
class ClientWrapper:

    def __init__(self, client):
        self.client = client

        client.start_channels()

        try:
            # TODO: configure
            client.wait_for_ready(timeout=60)
        except RuntimeError:
            client.stop_channels()
            # TODO: ?
            raise

    def execute(self, code):
        return ''
