from random import randint

globalinsdefault = [10, 2000, 256]


class Instance(object):  # 创建Circle类
    instanceID = ""
    cpuRequest: int = 0
    memRequest: int = 0
    diskRequest: int = 0
    latencyRequest = None
    location = None

    default = globalinsdefault

    def __init__(self, instanceID):
        self.instanceID = str(instanceID)
        return

    def initValue(self, c, m, s, la):
        self.cpuRequest = c
        self.memRequest = m
        self.diskRequest = s
        self.latencyRequest = la

    def getValue(self):
        return [
            self.instanceID, self.cpuRequest, self.memRequest,
            self.diskRequest, self.latencyRequest
        ]

    def randValue(self):
        self.cpuRequest = randint(0, self.default[0])
        self.memRequest = randint(0, self.default[1])
        self.diskRequest = randint(0, self.default[2])
        self.latencyRequest = list()

    def config(self, dl):
        self.default = dl
