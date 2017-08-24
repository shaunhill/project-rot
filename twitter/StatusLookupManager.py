
from multiprocessing import Queue
from multiprocessing.managers import BaseManager

class StatusLookupManager(BaseManager): pass
StatusLookupManager.register('get_status_lookup_queue',callable=lambda:status_lookup_queue)

status_lookup_queue = Queue()
sl_manager = StatusLookupManager(address=('',5000), authkey = b'SL')
sl_server = sl_manager.get_server()
sl_server.serve_forever() 

