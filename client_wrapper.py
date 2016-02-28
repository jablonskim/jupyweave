
class ClientWrapper:

    def __init__(self, client):
        self.client = client

        client.start_channels()

        try:
            pass
            # TODO: configure
            client.wait_for_ready()
        except RuntimeError:
            client.stop_channels()
            # TODO: ?
            raise

    def execute(self, code):
        msg_id = self.client.execute(code)

        print(self.client.get_shell_msg(timeout=5))
        print()
        #print(self.client.get_iopub_msg(timeout=5))

        return ''
