from multiprocessing import current_process
from multiprocessing.managers import BaseManager

class StatusLookupManager(BaseManager): pass
class StatusLookupClient(object):
    def __init__(self):
        current_process().authkey = b"SL"
        StatusLookupManager.register('get_status_lookup_queue')
        self.sl_manager = StatusLookupManager(address=('127.0.0.1',5000), authkey = b'SL')
        self.sl_manager.connect()
        self.status_lookup_queue = self.sl_manager.get_status_lookup_queue()

        
        