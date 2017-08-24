E:
cd "E:\Cloud\OneDrive\rot\twitter"
start "MongoDB Server" python  startmongodb.py
start "Database Manager" python databasemanager.py
start "Status Process Manager" python statusprocessmanager.py
start "Status Lookup Manager" python statuslookupmanager.py
start "Stream Manager" python streammanager.py

start "Database Worker" python databaseworker.py
start "Status Process Worker" python statusprocessworker.py
start "Status Lookup Worker" python statuslookupworker.py

exit