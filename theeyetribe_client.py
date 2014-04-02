import socket
import threading
import json
import time
#import urllib.request
import redis

r = redis.StrictRedis(host='192.168.1.169', port=6379)

message = {'values':
        {'push': True,
            'version':1},
        'category': 'tracker',
        'request': 'set'}

heatbit = {'category': 'heartbeat',
           'request': 'null'}

def hb(s):
    while 1:
        time.sleep(0.25)
        s.send(json.dumps(heatbit))
        print 'heat bearing'
        
NoUse = '{"category":"heartbeat","statuscode":200}'

def connect(host='localhost', port=6555):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(json.dumps(message))
    print 'sent messgae'
    t = threading.Thread(target=hb, args=(s,))
    t.start()

    while 1:
        fs = s.makefile()
        data = fs.readline()
        data = data.replace(NoUse, '')
        data = data.strip()
        if data:
            r.publish('chat', data)
            try:
                data = json.loads(data.strip())
            except Exception, e:
                print data
            print data.keys() if isinstance(data, dict)  else data
        else:
            print '-----------'
    t.join()


if __name__ == '__main__':
    connect()
               
