from multiprocessing import Queue
from multiprocessing.managers import BaseManager

class DatabaseManager(BaseManager): pass
           
DatabaseManager.register('get_status_staging_queue',callable=lambda:status_staging_001)
DatabaseManager.register('get_log_queue',callable=lambda:logs)
DatabaseManager.register('get_db_keys',callable=lambda:db_keys)


#Set __id key
#Set Source
status_staging_001 = Queue()

#Categorized into offensive categories.
#Set offensive
classification_training_001 = Queue()

#logging of errors, successes, etc.
logs = Queue()

db_keys = list()
db_manager = DatabaseManager(address=('',5001), authkey = b'DB')
db_server = db_manager.get_server()
db_server.serve_forever() 

