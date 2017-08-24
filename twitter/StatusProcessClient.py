
from multiprocessing import current_process
from multiprocessing.managers import BaseManager


class StatusProcessManager(BaseManager): pass
class StatusProcessClient(object):
    def __init__(self):
        current_process().authkey = b"SP"
        StatusProcessManager.register('get_raw_data_queue')
        StatusProcessManager.register('get_in_process_keys')
        self.SP_manager = StatusProcessManager(address=('127.0.0.1',5002), authkey = b'SP')
        self.SP_manager.connect()
        self.raw_data_queue = self.SP_manager.get_raw_data_queue()
        self.in_process_keys = self.SP_manager.get_in_process_keys()

        
        