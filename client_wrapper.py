from queue import Empty


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
        request_id = self.client.execute(code, allow_stdin=False)

        print(request_id)
        print()

        try:
            while True:
                msg = self.client.get_shell_msg(timeout=30.1)
                if msg['msg_type'] != 'execute_reply':
                    # TODO: ?
                    print('SHELL - Type %s' % msg['msg_type'])
                    continue

                if msg['parent_header']['msg_id'] != request_id:
                    # TODO: ?
                    print('SHELL - Invalid parent ID')
                    continue

                status = msg['content']['status']

                if status == 'ok':
                    print('SHELL - OK!')
                    # TODO: ?
                    break
                elif status == 'error':
                    # TODO: ?
                    print('SHELL - ERROR!')
                    print(msg)
                    break
                else:
                    # TODO: ?
                    print('SHELL - ABORT!')
                    break
        except Empty:
            # TODO: ?
            pass

        outputs = []

        try:
            while True:
                msg = self.client.get_iopub_msg(timeout=30.1)
                msg_type = msg['msg_type']
                parent_id = msg['parent_header']['msg_id']

                if parent_id != request_id:
                    # TODO: ?
                    print('IOPUB - Unknown parent ID')
                    continue

                # End of calculations
                if msg_type == 'status' and msg['content']['execution_state'] == 'idle':
                    break

                if msg_type == 'error':
                    print(msg)

                if msg_type != 'stream':
                    print('IOPUB - Type: %s' % msg_type)
                    continue

                outputs.append(msg['content'])
        except Empty:
            # TODO: ?
            pass

        # TODO: stderr/stdout
        output = ''.join([x['text'] for x in outputs])

        return output
