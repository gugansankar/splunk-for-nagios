# Script to request service SLA by accessing MK Livestatus
import socket,string,mklivestatus
from datetime import datetime, timedelta
import sys,splunk.Intersplunk

results = []

try:

    results,dummyresults,settings = splunk.Intersplunk.getOrganizedResults()

    for r in results:
        if "_raw" in r:
            if "src_host" in r:
                try:
		    PORT = mklivestatus.PORT
		    N = int(r["daysago"])
		    nowepoch = datetime.now()
		    nowepoch2 = nowepoch.strftime("%s")
		    date_N_days_ago = datetime.now() - timedelta(days=N)
		    date_N_days_ago2 = date_N_days_ago.strftime("%s")
		    content = [ "GET statehist\nColumns: host_name service_description\nFilter: time >= ", date_N_days_ago2, "\nFilter: time < ", nowepoch2, "\nStats: sum duration_part_ok", "\n" ]
    		    query = "".join(content)
		    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		    s.connect(((r["host"]), PORT))
		    s.send(query)
		    s.shutdown(socket.SHUT_WR)
		    data = s.recv(100000000)
		    liveservicesla2 = data.strip()
		    liveservicesla = liveservicesla2.split('\n')
		    s.close()
                    r["liveservicesla"] = liveservicesla
                except:
                    r["liveservicesla"] = "UNKNOWN"

except:
    import traceback
    stack =  traceback.format_exc()
    results = splunk.Intersplunk.generateErrorResults("Error : Traceback: " + str(stack))

splunk.Intersplunk.outputResults( results )

