from locust import User, task, HttpUser
import websocket
import time
import json
import random
import requests



random.seed(time.time_ns())
username = random.randint(30, 50)

def gen_user_name():
    global username
    username = username+1
    return "lxx"+str(username)

url1 = 'https://test-k8s-call-center-web.baijia.com/agent/assembly'
businessId = "4581"
serviceId = gen_user_name()
user_name = serviceId
json_data = {"businessId": businessId, "serviceId": serviceId, "callNum": ""}
data1 = requests.post(url1, json=json_data).json()
cno = str(data1["data"]["cno"])
print(cno)
timestamp = data1['timestamp']
# print("post2")
url2 = 'https://test-k8s-call-center-web.baijia.com/get/wsToken?serviceId=%s&cno=%s&businessId=%s' %\
    (serviceId, cno, businessId)
data2 = requests.get(url2).json()
wsToken = data2['data']['wsToken']


class WebSocketUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_event = self.environment.events.request
        self.web_socket = None



    def on_start(self):
        f = self._fire("on_start")
        try:
            global timestamp
            timestamp = timestamp + 1
            wsConnectionId = "%s.4581.%s" % (user_name, timestamp)
            # print("post2 finish")
            ws = 'ws://test-k8s-call-center-ws.baijia.com/call?token=%s&cno=%s&serviceId=%s&businessId=%s&wsConnectionId=%s' % \
                 (wsToken, cno, serviceId, businessId, wsConnectionId)
            self.web_socket = websocket.WebSocket()
            ws_res = self.web_socket.connect(ws)
            print(ws_res)
        except Exception as e:
            print("on_start err:", e)
            f(0, e)




    def on_stop(self):
        f = self._fire("on_start")
        try:
            print("on_stop close")
            self.web_socket.close()
        except Exception as e:
            print("on_stop err:", e)
            f(0, e)

    def _fire(self, name: str):
        # self.client.request_event.
        start = time.perf_counter()
        ctx = self.context()

        def func(response_length: int, e: Exception = None):
            end = time.perf_counter()
            request_meta = {
                "request_type": "wss",
                "name": name,
                "response_time": (end - start) * 1000,
                "response_length": response_length,
                "context": ctx,
                "exception": e,
            }
            self.request_event.fire(**request_meta)
        return func

    def send(self, data: str):
        f = self._fire('send')
        try:
            n = self.web_socket.send(data)
            f(n, None)
            return n
        except Exception as e:
            print("send", e)
            f(0, e)
            return e

    def recv(self):
        f = self._fire('recv')
        try:
            data = self.web_socket.recv()
            f(len(data), None)
            return data
        except Exception as e:
            print("recv", e)
            f(0, e)
            return e

    @task(1)
    def send1(self):
        sign = str(random.randint(100000000, 1000000000-1))
        obj = {
                  "source": "call",
                  "messageType": "heart_beat",
                  "sign": sign
                }
        self.send(json.dumps(obj))
        self.recv()
