from multiprocessing import current_process
from multiprocessing.managers import BaseManager

class DatabaseManager(BaseManager): pass
class DatabaseClient(object):
    def __init__(self):
        current_process().authkey = b"DB"
        DatabaseManager.register('get_status_staging_queue')
        DatabaseManager.register('get_db_keys')
        DatabaseManager.register('get_log_queue')
        self.work_package = []
        self.db_manager = DatabaseManager(address=('127.0.0.1',5001), authkey = b'DB')
        self.db_manager.connect()
        self.db_keys = self.db_manager.get_db_keys()
        self.status_staging_001 = self.db_manager.get_status_staging_queue()
        self.logs = self.db_manager.get_log_queue()
        
