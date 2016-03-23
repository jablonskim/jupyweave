from queue import Empty
from exceptions.processor_errors import KernelClientStartingError, ExecutionTimeoutError
from results_processor import ResultsProcessor


class ClientWrapper:
    """Wrapper for Jupyter Client"""

    def __init__(self, client, language, execution_timeout):
        """Initializes and starts client"""
        self.__client = client
        self.__execution_timeout = execution_timeout

        self.__client.start_channels()

        try:
            self.__client.wait_for_ready()
        except RuntimeError:
            self.__client.stop_channels()
            raise KernelClientStartingError(language)

    def execute(self, code, execution_timeout=None, allow_errors=False):
        """Executes code, returns results"""
        timeout = execution_timeout if execution_timeout is not None else self.__execution_timeout
        request_id = self.__client.execute(code, allow_stdin=False)

        # Processing SHELL messages
        try:
            while True:
                msg = self.__client.get_shell_msg(timeout=timeout)

                # Ignore 'Execute requests'
                if msg['msg_type'] != 'execute_reply':
                    continue

                # Ignore answers to other messages
                if msg['parent_header']['msg_id'] != request_id:
                    continue

                status = msg['content']['status']

                # Go to next step if status OK
                if status in ['ok', 'error']:
                    break

                # TODO: ?
                print('SHELL - ABORT!')

        except Empty:
            raise ExecutionTimeoutError(code)

        output = ResultsProcessor(allow_errors)

        # Processing IOPUB messages
        try:
            while True:
                msg = self.__client.get_iopub_msg(timeout=timeout)
                msg_type = msg['msg_type']
                parent_id = msg['parent_header']['msg_id']

                # Ignore answers to other requests
                if parent_id != request_id:
                    continue

                # End of calculations
                if msg_type == 'status' and msg['content']['execution_state'] == 'idle':
                    break

                if msg_type == 'error':
                    content = msg['content']
                    output.process_error(content['ename'], content['evalue'], content['traceback'])
                    continue

                if msg_type == 'stream':
                    output.process_stream(msg['content']['text'], msg['content']['name'])
                    continue

                if msg_type in ['display_data', 'execute_result']:
                    data = msg['content']['data']
                    for key, value in data.items():
                        output.process_data(key, value)
                    continue

                # TODO: remove
                #print('IOPUB - Type: %s' % msg_type)

        except Empty:
            raise ExecutionTimeoutError(code)

        return output.get_result()
