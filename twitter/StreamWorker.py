import sys
import os
from tweepy.streaming import StreamListener

sys.path.append('E:/Cloud/OneDrive/rot/')
# from twitter.DatabaseClient import DatabaseClient
from twitter.StatusProcessClient import StatusProcessClient
from twitter.StreamClient import StreamClient
from twitter.LogDocument import LogDocument
from multiprocessing import Process
import tweepy


class StreamWorker(Process,StreamClient,StatusProcessClient,tweepy.StreamListener):
    def __init__(self):
        StreamClient.__init__(self)
        Process.__init__(self)
        tweepy.StreamListener.__init__(self)
        
    def on_status(self, status):
        self.raw_data_queue.put(status)
        
    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        
    def run(self):
        log_doc = LogDocument()
        pid = os.getpid()
        
        print('Starting process ID : {0}'.format(pid))
        stream_count = 0 
        
        log_doc.pid = pid
        log_doc.type = 'stream'
        
        consumer_key = 'hZojLYIwrojrE81KSA0qbiI3z'
        consumer_secret = 'BnytOWGfhpyqZJME8YxAqZ8V8CChmTLljSNjTETTHdXLW2I6cj'
        access_token = '4888572562-qPj8uPjuT9xCPohNvEWFPNM8Cv6e5ujJ17CoTgB'
        access_token_secret = 'zNVpFGNi3wLR2xuWAF4wfJaAvw693eyZHgcx3jTmntCVd'
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
                        
        api = tweepy.API(auth,wait_on_rate_limit = True,wait_on_rate_limit_notify = True)
        
        myStream = tweepy.Stream(auth = api.auth, listener=self)
        
        while True:
            work = self.stream_queue.get()
            if work != None:
                stream_count += 1
                log_doc.type_id = stream_count
                log_doc.category = 'Execution'
                log_doc.db_target = work
                
                try:
                    log_doc.status = 'Started'
                    print(log_doc.getDocument())
                    myStream.filter(eval(work))
                    
                except Exception as e:
                    
                    log_doc.status = 'Failed'
                    log_doc.error = e
                    print(log_doc.getDocument())

if __name__ == '__main__':
    
    s = StreamClient()
    s.stream_queue.put( "locations=[15.82,-34.8,34.28,-22.07]")
    
    processes = []  
    for x in range(s.stream_queue.qsize()):
        process = StreamWorker()
        processes.append(process)

    for process in processes:
        process.start()
        
    for process in processes:
        process.join()


   
   



   
    
