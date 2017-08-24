import sys
import os
sys.path.append('E:/Cloud/OneDrive/rot/')
from twitter.DatabaseClient import DatabaseClient
from twitter.StatusLookupClient import StatusLookupClient
from twitter.StatusProcessClient import StatusProcessClient
from twitter.LogDocument import LogDocument
from multiprocessing import Process
import pprint
import tweepy
import time


class StatusLookupWorker(Process,StatusLookupClient,StatusProcessClient,DatabaseClient):
    def __init__(self):
        
        StatusLookupClient.__init__(self)
        StatusProcessClient.__init__(self)
        DatabaseClient.__init__(self)
        Process.__init__(self)
               
    def run(self):
        work_package = []
        consumer_key = 'hZojLYIwrojrE81KSA0qbiI3z'
        consumer_secret = 'BnytOWGfhpyqZJME8YxAqZ8V8CChmTLljSNjTETTHdXLW2I6cj'
        access_token = '4888572562-qPj8uPjuT9xCPohNvEWFPNM8Cv6e5ujJ17CoTgB'
        access_token_secret = 'zNVpFGNi3wLR2xuWAF4wfJaAvw693eyZHgcx3jTmntCVd'
    
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit = True,wait_on_rate_limit_notify = True)
        
        pid = os.getpid()
        call_count = 0
        
        log_doc = LogDocument()
        log_doc.pid = pid
        
        print('Starting process ID : {0}'.format(pid))
        while True:
            log_doc.type = 'Status Lookup'
            log_doc.category = 'Execution'
            
            call_count += 1
            log_doc.type_id = call_count
            
            work_package = []
            work_count = 0
            start_time = time.time()
            log_doc.start_time = start_time 
            while work_count < 100 and (time.time() - start_time) <= 60:
                work = self.status_lookup_queue.get()
                if work != None:
                    try:
                        work_package.append(work)
                        work_count += 1
                    except Exception as e:
                        print(e)
            if work_count > 0:
                try:
                    statuses = api.statuses_lookup(work_package)
                    self.raw_data_queue.put(statuses)
                    log_doc.status = 'Success'
                except Exception as e:
                    log_doc.status = 'Failed'
                    log_doc.error = e
                finally:
                    result = {'work_count':work_count,'work_package':work_package}
                    log_doc.result  = result 
                    log_doc.end_time = time.time()
                    log_doc_print = log_doc.getDocument()
                    self.logs.put(log_doc_print)
                    pprint.pprint(log_doc_print)
                    log_doc.result = None
                    

if __name__ == '__main__':
    

    processes = []
    for x in range(4):
        process = StatusLookupWorker()
        processes.append(process)
        
    for process in processes:
        process.start()
        
    for process in processes:
        process.join()
        
    
    
        
        



   
   



   
    
