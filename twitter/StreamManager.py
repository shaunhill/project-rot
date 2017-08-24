from multiprocessing import Queue
from multiprocessing.managers import BaseManager

class StreamManager(BaseManager): pass
    
StreamManager.register('get_stream_queue',callable=lambda:stream_queue)
stream_queue = Queue()
s_manager = StreamManager(address=('',5004), authkey = b'S')
s_server = s_manager.get_server()
s_server.serve_forever() 

