import time

class LogDocument:
    def __init__(self):
        self.pid = None
        self.category = None
        self.type = None
        self.type_id = None
        self.status = None
        self.error = None
        self.result = None
        self.db_target = None
        self.record_type = None
        self.record_count = None
        self.result = None
        self.start_time = time.time()
        self.end_time = None
        self.queue_size = None
        
#     def setQueueSize(self,queue_size):
#         self.queue_size = queue_size
#         
#     def setEndTime(self,end_time):
#         self.end_time = end_time
#         
#     def setStartTime(self,start_time):
#         self.start_time = start_time
#         
#     def setPid(self,pid):
#         self.pid = pid
#         
#     def setType(self,type):
#         self.type = type        
#         
#     def setCategory(self,category):
#         self.category = category
#         
#     def setStatus(self,status):
#         self.status = status
#         
#     def setTypeID(self,type_id):
#         self.type_id = type_id
#           
#     def setError(self,error):
#         self.error = error 
# 
#     def setResult(self,result):
#         self.result = result
#         
#     def setDBTarget(self,db_target):
#         self.db_target = db_target
#         
#     def setRecordType(self,record_type):
#         self.record_type = record_type
#         
#     def setRecordCount(self,record_count):
#         self.record_count = record_count

    def getDocument(self):
        doc = \
            {
            'PID' : self.pid,
            'type': self.type,
            'category' : self.category,
            'status': self.status,
            'type_id' : self.type_id,
            'error' : self.error,
            'db_target' : self.db_target,
            'record_type' : self.record_type,
            'record_count' : self.record_count,
            'result' : self.result,
            'start_time':self.start_time,
            'end_time':self.end_time,
            'queue_size': self.queue_size
            }
        
        return(doc)
    
    