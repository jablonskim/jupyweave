from queue import Empty
from exceptions.processor_errors import KernelClientStartingError, ExecutionTimeoutError


class ClientWrapper:

    def __init__(self, client, language, execution_timeout):
        self.__client = client
        self.__execution_timeout = execution_timeout

        self.__client.start_channels()

        try:
            self.__client.wait_for_ready()
        except RuntimeError:
            self.__client.stop_channels()
            raise KernelClientStartingError(language)

    def execute(self, code):
        request_id = self.__client.execute(code, allow_stdin=False)

        try:
            while True:
                msg = self.__client.get_shell_msg(timeout=self.__execution_timeout)
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
            raise ExecutionTimeoutError(code)

        outputs = []

        try:
            while True:
                msg = self.__client.get_iopub_msg(timeout=self.__execution_timeout)
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
            raise ExecutionTimeoutError(code)

        # TODO: stderr/stdout
        output = ''.join([x['text'] for x in outputs])

        return output
