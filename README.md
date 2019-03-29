# Axon: hub of zmq PUB/SUB Broker and influxdb logging backend 

Extracted Broker functionality from fanequinha as independent module, "should" be installable with:
(inside pipenv shell folder):
`pipenv install git+git://github.com/dpmilian/axon.git#egg=axon`

Broker now runs separate threads for Publisher and Suscriber, for example (server.py in repo):

```
from axon.broker import Broker

def messageHandler(multipart_msg):
    topic, can = broker.parseMessage(multipart_msg)
    print ("[%s/%d] : %s" % (topic, can["cnt"], can["msg"]))


broker = Broker()

broker.setPublisher(port=4000)                        # will publish messages on localhost (default), port 4000
broker.setSuscriber(ip="localhost", port=4001)        # suscribes to Publisher on localhost, port 4001
broker.suscribe(["STS", "POS"], messageHandler)       # selects these two topics to suscribe to, assigns "messageHandler"
                                                      # callback function; other topics can have other callback function

broker.spin()                                         # starts the ioloop thread that receives Suscriber events, non blocking

cnt = 0
try :
    while (True):                                     # Publisher sends out simple message to client, not blocking Suscriber
        can = {
            "msg": "BLA BLA BLA",
            "cnt": cnt
        }
        broker.publish("CMD", can)
        cnt+=1
        print("Publish %d" % cnt)

        time.sleep(1)

except KeyboardInterrupt:                             # Ctrl + c closes
    broker.stop()
    sys.exit()
```

# TODO:
- Version updates? 
- Check import works correctly?
- Store module (`from axon.store import Store`) under development: use *influxdb* as timestamped storage, seems very applicable to task at hand, also very simple to implement
