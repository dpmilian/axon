from influxdb import InfluxDBClient

class Store(object):

    def __init__(self, database, host='localhost', port=8086):
        
        self.host = host
        self.port = port
        self.client = InfluxDBClient(host=self.host, port=self.port)
        
        if (not self.client.describeDatabases().contains(database)):
            self.client.create(database)
        
        self.client.switch_database(database)    

    def put(self, time, tags, fields):
        pass

    def get(self):
        pass

    
