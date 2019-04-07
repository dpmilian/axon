from influxdb import InfluxDBClient
import datetime

class Store(object):

    def __init__(self, host='localhost', port=8086):
        
        self.host = host
        self.port = port


    def connect(self):
        self.client = InfluxDBClient(host=self.host, port=self.port)


    def setUser(self, user, pw):
        self.client.create_user(user, pw)
        self.client.switch_user(user, pw)


    def setDatabase(self, dbname):
        dbs = self.client.get_list_database()
        print(dbs)
        self.client.create(dbname)        # if it already exists, doesn't give any error...
        self.client.switch_database(dbname)
        self.client.create_retention_policy('forever', 'INF', 3, dbname)


    def put(self, measurement, fields, tags = None, time = None):
        """
        measurement -> id of measurement
        time -> default now, otherwise RFC RFC3339 value
        "tags": {
                "tag1": "server01",
                "tag2": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "field1": 0.64,
                "field2": 3
            }
        """

        if time == None:
            time = self.client.now()

        json_body = [
            {

                "measurement": measurement,
                "tags": tags,
                "time": time,
                "fields": fields
            }
        ]

        self.client.write_points(json_body)


    def get(self, measurement,  fields = None, tags = None, time_start=None, time_end=None):
        """
        tags -> [tag1, tag2]
        fields -> [field1, field2]
        time_* -> RFC 3339 timestamp, i.e. '2017-04-13T14:34:23.111142+00:00'
        """

        stags = ''
        if (tags != None):
            for tag in tags:
                stags += '"' + tag + '"::tag,'

        sfields = ''
        if (fields != None):
            for field in fields:
                sfields += '"' +  field + '"::field,'
            sfields = sfields[:-1]      # remove last comma

        if (sfields == ''):
            if (stags != ''):
                stags = stags[:-1]
        
        sfrom  = 'FROM ' + measurement

        shwere = ''
        if (time_start != None) or (time_end != None):
            swhere = 'WHERE '
        sstart = ''
        if (time_start != None):
            sstart = 'TIME > ' + time_start
        send =''
        if (time_end != None):
            if (time_start != None):
                sstart += ' AND '
            send = 'TIME < ' + time_end
        
        query = "SELECT " + stags + sfields + sfrom + shwere + sstart + send
        result = self.client.query(query)

        return (result.get_points())
    

    def query(self, query):

        result = self.client.query(query)
        return (result.get_points())

    
