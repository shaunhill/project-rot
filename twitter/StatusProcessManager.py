from multiprocessing import Queue
from multiprocessing.managers import BaseManager

class StatusProcessManager(BaseManager): pass
StatusProcessManager.register('get_raw_data_queue',callable=lambda:raw_data_queue)
StatusProcessManager.register('get_in_process_keys',callable=lambda:in_process_keys)
raw_data_queue = Queue()
in_process_keys  = list()
SP_manager = StatusProcessManager(address=('',5002), authkey = b'SP')
SP_server = SP_manager.get_server()
SP_server.serve_forever() 

