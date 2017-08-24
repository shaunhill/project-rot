from multiprocessing.managers import BaseManager
import pymongo

class StatusLookupManager(BaseManager): pass

StatusLookupManager.register('get_work_queue')
SL_manager = StatusLookupManager(address=('127.0.0.1',5000), authkey = b'SML')
SL_manager.connect()

        
if __name__ == '__main__':
    work_queue = SL_manager.get_work_queue()
    client = pymongo.MongoClient()
    db = client['rot']
    raw_status_staging = db.twitter_staging_001
    db_keys = []    
    col_cur = raw_status_staging.find()
    
    for doc in col_cur:
        reply_status_id = doc['in_reply_to_status_id']
        if reply_status_id != None and reply_status_id not in db_keys:
            work_queue.put(reply_status_id)

