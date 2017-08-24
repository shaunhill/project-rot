
import sys
import os
sys.path.append('e:/Cloud/OneDrive/rot/')
from twitter.DatabaseClient import DatabaseClient
from twitter.StatusLookupClient import StatusLookupClient
from twitter.LogDocument import LogDocument
from multiprocessing import Process
import pymongo
import time
import pprint

class DatabaseWorker(Process,DatabaseClient):
    def __init__(self,target_queue,target_db):
        self.target_queue = target_queue
        self.target_db = target_db
        DatabaseClient.__init__(self)
        Process.__init__(self)
    
    def run(self):
        #connect to DB
        client = pymongo.MongoClient()
        db = client['rot']
        
        pid = os.getpid()
        bulkop_count = 0
        
        log_doc = LogDocument()
        log_doc.pid = pid
        
        pprint.pprint('Starting process ID : {0}'.format(pid))
        while True:
            pprint.pprint('top')
            bulkop_count += 1
            
#             log_doc.setStartTime(time.time())
#             log_doc.setType('Bulk Write')
#             log_doc.setDBTarget(self.target_db)
#             log_doc.setCategory('Initialization')
#             log_doc.setTypeID(bulkop_count)            
            log_doc.start_time = time.time()
            log_doc.type = 'Bulk Write'
            log_doc.db_target = self.target_db
            log_doc.category = 'Initialization'
            log_doc.type_id = bulkop_count

            try:
                bulkop = db[self.target_db].initialize_ordered_bulk_op()
                log_doc.status = 'Success'
  
            except Exception as e:

                log_doc.error = e
                log_doc.status = 'Failed'
    
            finally:
                log_doc.end_time = time.time()
                log_doc_print = log_doc.getDocument()
                self.logs.put(log_doc_print)
                pprint.pprint(log_doc_print)
                
            op_count = 0
            start_time = time.time()
            log_doc.start_time = start_time
            while op_count < 50 and (time.time() - start_time) <= 10:
                try:
                    work = eval('self.'+self.target_queue).get()
                    log_doc.queue_size = eval('self.'+self.target_queue).qsize()
                except:
                    work = None
                if work != None:
                    try:
                        key = work['_id']
                    except:
                        key = 'Pass'
                    try:
                        op_count += 1
                        if key == 'Pass':
                            result = bulkop.insert(work)
                        else:
                            result = bulkop.find({'_id':key}).upsert().replace_one(work)
                        if key != 'Pass':
                            self.db_keys.append(key)
                    except Exception as e:
                        pprint.pprint(e)    
                    
            if op_count > 0:
                print('Trying to Execute bulk')
                log_doc.record_type = 'op_count'
                log_doc.record_count = op_count
                log_doc.category = 'Execution'    
                try:
                    result = bulkop.execute()                    
                    log_doc.result = result
                    log_doc.status = 'Success'
                except Exception as e:
                    log_doc.error = e
                    log_doc.status = 'Failed'
                finally:
                    log_doc.end_time =  time.time()
                    log_doc_print = log_doc.getDocument()
                    self.logs.put(log_doc_print)
                    pprint.pprint(log_doc_print)
                    log_doc.result = None
                    
            
                                                         
if __name__ == '__main__':
    
    db_client_key_init = DatabaseClient()
    sl_client_missing_status = StatusLookupClient()
    client = pymongo.MongoClient()
    db = client['rot']
    status_staging_001 = db.twitter_staging_001
    
    temp_reply_keys = []
    temp_db_keys = []
    
    log_doc = LogDocument()
    print('Trying to initialize DB keys and missing statues...')
    
    if len(db_client_key_init.db_keys._getvalue()) == 0:
            
        log_doc.type = 'DB keys'
        log_doc.category = 'Initialization'
        log_doc.start_time = time.time() 
        
        try:
            for doc in status_staging_001.find():
                key = doc['_id']
                reply_status_id = doc['in_reply_to_status_id']
                if reply_status_id != None:
                    temp_reply_keys.append(reply_status_id)
                temp_db_keys.append(key)        
                log_doc.status = 'Success'
                
        except Exception as e:
            log_doc.status = 'Failed'
            log_doc.error(e)
#             try:
#                 result = {'temp_reply_keys':len(temp_reply_keys),'temp_db_keys':len(temp_db_keys)}
#                 log_doc.setResult(result)
#             except:
#                 pass
        finally:
            log_doc.result = temp_reply_keys
            log_doc.end_time = time.time()
            log_doc.record_type = 'temp_reply_keys'
            log_doc.record_count = len(temp_reply_keys)
            log_doc_print = log_doc.getDocument()
            db_client_key_init.logs.put(log_doc_print)
#             print(log_doc_print)
            
            log_doc.result = temp_db_keys
            log_doc.record_type = 'temp_db_keys'
            log_doc.record_count = len(temp_db_keys)
            log_doc_print = log_doc.getDocument()
            db_client_key_init.logs.put(log_doc_print)
#             print(log_doc_print)
            log_doc.result = None
                
        try:
            
            log_doc.start_time = time.time()
    
            print('Getting missing statues...')
            log_doc.type = 'Missing Statues'
            log_doc.category = 'Initialization'
            temp_reply_keys = set(temp_reply_keys) - set(temp_db_keys)
            log_doc.status = 'Success'
            log_doc.record_type = 'temp_reply_keys'
            log_doc.record_count = len(temp_reply_keys)
            
        except Exception as e:
            log_doc.status = 'Failed'
            log_doc.error = e
            
        finally:
            log_doc.end_time = (time.time())
            log_doc_print = log_doc.getDocument()
            db_client_key_init.logs.put(log_doc_print)
            print(log_doc_print)
            
        print('Transfer keys to mangers...')
        
        log_doc.type = 'DB keys'
        log_doc.category = 'Execution'
        
        try:       
            log_doc.start_time = time.time()
            for key in temp_db_keys:
                db_client_key_init.db_keys.append(key)
                
            log_doc.status = 'Success'
            log_doc.record_type = 'temp_db_keys'
            log_doc.record_count = len(temp_db_keys)
            temp_db_keys = []
            
        except Exception as e:
            log_doc.status = 'Failed'
            log_doc.error = e
            
        finally:
            log_doc.end_time = time.time()
            log_doc_print = log_doc.getDocument()
            db_client_key_init.logs.put(log_doc_print)
#             print(log_doc_print)
            
        log_doc.type = 'Missing Statues'
        log_doc.category = 'Execution'  
          
        try:       
            log_doc.start_time = time.time()
            for key in temp_reply_keys:
                sl_client_missing_status.status_lookup_queue.put(key)
                
            log_doc.status = 'Success'        
            log_doc.record_type = 'temp_reply_keys'
            log_doc.record_count = len(temp_reply_keys)
            temp_reply_keys = []
            
        except Exception as e:
            log_doc.status = 'Failed'
            log_doc.error = e
            
        finally:
            log_doc.end_time = time.time()
            log_doc_print = log_doc.getDocument()
            db_client_key_init.logs.put(log_doc_print)
#             print(log_doc_print)

    else:
        print('Already Initialized')

    processes = []  
    
    for x in range(1):
        process = DatabaseWorker('status_staging_001','twitter_staging_001')
        processes.append(process)

    for x in range(1):
        process = DatabaseWorker('logs','logs')
        processes.append(process)
        
    for process in processes:
        process.start()
        
    for process in processes:
        process.join()


