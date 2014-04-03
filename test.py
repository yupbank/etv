import socket
import threading
import json
import time
#import urllib.request
import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379)#, db=0)
BUFFER_SIZE = 1024

message = {'values':
               {'push': True,
                'version':1},
           'category': 'tracker',
           'request': 'set'}
pull = {
    "category": "tracker",
    "request" : "get",
    "values": [ "frame" ]
}

heatbit = {'category': 'heartbeat',
           'request': 'null'}

NoUse = '{"category":"heartbeat","statuscode":200}'

def connect(host='localhost', port=6555):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    while 1:
        time.sleep(0.25)
        s.send(json.dumps(pull))
        fs = s.makefile()
        data = fs.readline()
        data = data.replace(NoUse, '')
        data = data.strip()
        if data:
            r.publish('chat', data)
            print data
        print 'heat bearing'
        

def connect_nouse(host='localhost', port=6555):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(json.dumps(message))
    print 'sent messgae'
    #t = threading.Thread(target=hb, args=(s,))
    #t.start()

    while 1:
        fs = s.makefile()
        data = fs.readline()
        data = data.replace(NoUse, '')
        data = data.strip()
        if data:
            r.publish('chat', data)
            print data
            try:
                data = json.loads(data.strip())
            except Exception, e:
                print e
            #print data.keys() if isinstance(data, dict)  else data
            #r.lpush('time_data', data)
            #print data
        else:
            print '-----------'
    t.join()


if __name__ == '__main__':
    connect()
               
