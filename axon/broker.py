import zmq
import sys
import json
import time
import base64
from threading import Thread

from zmq.eventloop import ioloop, zmqstream
ioloop.install()

def screen(s):
    return s.encode("utf-8")

def descreen(b):
    return b.decode("utf-8")

def screen64(s):
    return base64.b64encode(screen(s))

def descreen64(b):
    return descreen(base64.b64decode(b))

# ------------------------------
class Broker(object):

    def __init__(self):
        self._publisher = None
        self._suscriber = None
        self._thread = None

    def __del__(self):
        ioloop.IOLoop.instance().stop()        

    def setPublisher(self, port):
        self._publisher = _Publisher(port)

    def publish(self, topic, message):
        self._publisher.send(topic, message)

    def setSuscriber(self, ip, port):
        self._suscriber = _Suscriber(ip, port)
        self._suscriber.connect()

    def suscribe(self, topics, callback):
        self._suscriber.suscribe(topics, callback)
 
    def spin(self):
        """
        Runs listen event loop in a separate process
        Returns inmediately, shouldn't block outer thread
        """
        #print("Spin new process")
        loop = ioloop.IOLoop.instance()
        self._thread = Thread(target=self._suscriber.listen, args=(loop,))
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        ioloop.IOLoop.instance().stop()
  
        # self._thread.join()      


# --------
    def parseMessage(self, rcvd):

        topic=""
        can = None

        try:
            topic = descreen(rcvd[0])
            msg = descreen64(rcvd[1])

            can = json.loads(msg)            

        except zmq.ZMQError:
            topic = 'ERR'

        return(topic, can)
            

# ------------------------------
class _Publisher(object):

    def __init__(self, port):
        self.port = port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%d" % (self.port))
        print ("ZeroMQ Publisher bound on tcp://*:%d" % (self.port))

    # --------
    def send(self, topic, message):
        json_bytes = screen64(json.dumps(message))
        topic_bytes = screen(topic)
        self.socket.send_multipart([topic_bytes, json_bytes])

# ------------------------------
class _Suscriber(object):

    def __init__(self, ip, port):
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.port = port
        self.ip = ip
        self._stream_sub = None

    # --------
    def connect(self):
            print("Connecting Suscriber to tcp://%s:%d" % (self.ip, self.port))
            errok = self.socket.connect("tcp://%s:%d" % (self.ip, self.port))
            if (errok):
                print("Connection returned error: ")
                print(errok)

    # --------
    def suscribe(self, topics, callback):
        """
        """
        for topic in topics:
            print ("Suscribe to topic %s" % topic)
            try:
                self.socket.setsockopt(zmq.SUBSCRIBE, screen(topic))
            except TypeError:
                self.socket.setsockopt_string(zmq.SUBSCRIBE, screen(topic))
            

        self._callback = callback
        self._stream_sub = zmqstream.ZMQStream(self.socket)
        self._stream_sub.on_recv(self._callback)

    def listen(self, loop):
        """
        Starts polling the suscribed/ peer sockets already connected to
        Blocks the process/ thread that called it
        """

        #print("Listen in new process")
        loop.start()
        #print("Finished listening")


    # --------
    def peek(self, topics):
        """
        Tries to receive message of any of the topics in the array
        does not block; returns the topic and message as a named tuple, or
        if there were no messages, returns topic "ERR"
        """
        for topic in topics:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)

        try:
            rcvd = self.socket.recv(flags=zmq.NOBLOCK)
            topic, msg = rcvd.split()
            msg = base64.b64decode(msg)

            return (topic, json.loads(msg))

        except zmq.ZMQError:
            topic = 'ERR'
            return ('ERR', None)



