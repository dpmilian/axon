from axon import broker
from axon import store
import time
import sys


def messageHandler(multipart_msg):
    topic, can = broker.parseMessage(multipart_msg)
    print ("[%s/%d] : %s" % (topic, can["cnt"], can["msg"]))


hub = broker.Broker()
st = store.Store()
st.setDatabase(dbname="arducopter-log")

hub.setPublisher(port=4000)
hub.setSuscriber(ip="localhost", port=4001)
hub.suscribe(["STS", "POS"], messageHandler)

hub.spin()

cnt = 0
try :
    while (True):
        can = {
            "msg": "BLA BLA BLA",
            "cnt": cnt
        }
        hub.publish("CMD", can)
        cnt+=1
        print("Publish %d" % cnt)

        time.sleep(1)

except KeyboardInterrupt:
    hub.stop()
    sys.exit()


