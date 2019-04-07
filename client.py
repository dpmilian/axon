from broker import Broker
import time
import sys


def messageHandler(multipart_msg):
    topic, can = broker.parseMessage(multipart_msg)
    print ("[%s/%d] : %s" % (topic, can["cnt"], can["msg"]))


broker = Broker()

broker.setPublisher(port=4001)
broker.setSuscriber(ip="localhost", port=4000)
broker.suscribe(["CMD", "UPD"], messageHandler)

broker.spin()

cnt = 0
try :
    while (True):
        can = {
            "msg": "WHASSUP DUDE",
            "cnt": cnt
        }
        broker.publish("STS", can)
        cnt+=1
        print("Publish %d" % cnt)

        time.sleep(1)

except KeyboardInterrupt:
    broker.stop()
    sys.exit()


