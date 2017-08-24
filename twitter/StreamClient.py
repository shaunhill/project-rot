from multiprocessing import current_process
from multiprocessing.managers import BaseManager

class StreamManager(BaseManager): pass
class StreamClient(object):
    def __init__(self):
        current_process().authkey = b"S"
        StreamManager.register('get_stream_queue')
        self.s_manager = StreamManager(address=('127.0.0.1',5004), authkey = b'S')
        self.s_manager.connect()
        self.stream_queue = self.s_manager.get_stream_queue()
        
