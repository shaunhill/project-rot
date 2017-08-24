import sys
sys.path.append('E:/Cloud/OneDrive/rot/')
from twitter.DatabaseClient import DatabaseClient
from twitter.StatusLookupClient import StatusLookupClient
from twitter.StatusProcessClient import StatusProcessClient
import pymongo

class DatabaseWorker(DatabaseClient):
    def __init__(self):                
        super(DatabaseWorker, self).__init__()
pass
  
d = DatabaseWorker()
d.status_staging_001.qsize()
        
class StatusLookupWorker(StatusLookupClient):
    def __init__(self):                
        super(StatusLookupWorker, self).__init__()
        
        
sl = StatusLookupWorker()
sl.status_lookup_queue.qsize()
        
class StatusProcessWorker(StatusProcessClient):
    def __init__(self):                
        super(StatusProcessWorker, self).__init__()
    

sp = StatusProcessWorker()
d = DatabaseWorker()
sp.raw_data_queue.qsize()

db_client_key_init = DatabaseClient()
sl_client_missing_status = StatusLookupClient()
client = pymongo.MongoClient()
db = client['rot']
raw_status_staging = db.twitter_staging_001
temp_reply_keys = []
temp_db_keys = []

print('Initializing...')
for doc in raw_status_staging.find():
    key = doc['_id']
    reply_status_id = doc['in_reply_to_status_id']
    if reply_status_id != None:
        temp_reply_keys.append(reply_status_id)
    temp_db_keys.append(key)
            
print('Getting missing statues...')
temp_reply_keys = set(temp_reply_keys) - set(temp_db_keys)
print('Transfer keys to mangers...')
            
for key in temp_db_keys:
    db_client_key_init.DB_keys.append(key)
print('{0} DB Keys transfered'.format(len(temp_db_keys)))
temp_db_keys = []
                
for key in temp_reply_keys:
    sl_client_missing_status.work_queue.put(key)
print('{0} Missing Statues transfered'.format(len(temp_reply_keys)))
temp_reply_keys = []    
print('Completed.')

for doc in raw_status_staging.find():
    if doc['id'] != doc['_id']:
        print(doc['_id']) 