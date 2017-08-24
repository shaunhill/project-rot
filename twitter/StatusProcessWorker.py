import sys
import os
sys.path.append('E:/Cloud/OneDrive/rot/')
from twitter.DatabaseClient import DatabaseClient
from twitter.StatusProcessClient import StatusProcessClient
from twitter.StatusLookupClient import StatusLookupClient
from twitter.LogDocument import LogDocument
from multiprocessing import Process
import pprint

class StatusProcessWorker(Process,DatabaseClient,StatusProcessClient,StatusLookupClient):
    def __init__(self):
        StatusLookupClient.__init__(self)
        DatabaseClient.__init__(self)
        StatusProcessClient.__init__(self)
        Process.__init__(self)
   
    def run(self):
        log_doc = LogDocument()
        pid = os.getpid()
        log_doc.pid = pid
        print('Starting process ID : {0}'.format(pid))
        package_count = 0 
        status_count = 0
        reply_count = 0
        
        while True:
            work = self.raw_data_queue.get()
            if work != None:
                package_count += 1
                log_doc.type = 'Process Package'
                log_doc.category = 'Execution' 
                log_doc.type_id = package_count
                
                try:    
                    for status in work:
                        status_count += 1
                        data = status._json
                        key = data['id']
                        
                        if key not in self.in_process_keys._getvalue():
                            
                            self.in_process_keys.append(key)
                            data['_id'] = key
                            reply_key = data['in_reply_to_status_id']
                            self.status_staging_001.put(data)
                            
                            if reply_key != None:
                                if reply_key not in self.in_process_keys._getvalue() \
                                or reply_key  not in self.db_keys._getvalue():
                                    reply_count += 1
                                    self.status_lookup_queue.put(reply_key)
                                    
                            self.in_process_keys.remove(key) 
                            
                    
                    log_doc.status = 'Success'
                    
                except Exception as e:
                    log_doc.status = 'Failed'
                    log_doc.error = e
                finally:
                    result = {'status_count':status_count,'reply_count':reply_count}
                    log_doc.result = result 
                    log_doc_print = log_doc.getDocument()
                    self.logs.put(log_doc_print)
                    pprint.pprint(log_doc_print)
                    log_doc.result = None
                              
                status_count = 0
                reply_count = 0  
                 
if __name__ == '__main__':
    
    
    processes = []  
    for x in range(4):
        process = StatusProcessWorker()
        processes.append(process)

    for process in processes:
        process.start()
        
    for process in processes:
        process.join()


   
   



   
    
