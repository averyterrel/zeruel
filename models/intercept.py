import threading
import queue
from util import parser
from controllers import server_manager


class InterceptModel:
    def __init__(self, controller):
        self.server_thread = controller.server
        self.client_request_queue = controller.client_request_queue

        self.intercepting = False #TODO: take this as an arg

    def forward_request(self, request: bytes):
        if self.server_thread and self.server_thread.running:
            if request:
                parsed_request = parser.parse_data(request)

                print(request)
                print(parsed_request)

                webserver = parsed_request["host"]
                port = parsed_request["port"]
                data = parsed_request["data"]
                threading.Thread(target=self.server_thread.send_data, args=(webserver, port, data)).start()
            else:
                print("no request intercepted")

    def start_intercepting(self):
        server_manager.stop_all()
        self.server_thread = server_manager.new_server()
        server_manager.start(self.server_thread, intercept=True)

    def stop_intercepting(self):
        server_manager.stop(self.server_thread)
        self.server_thread = server_manager.new_server()
        server_manager.start(self.server_thread, intercept=False)

    def get_client_request_from_queue(self):
        try:
            request = self.client_request_queue.get_nowait().decode('utf-8')
            print(f"data in queue {request}")
            return request
        except queue.Empty:
            return None
