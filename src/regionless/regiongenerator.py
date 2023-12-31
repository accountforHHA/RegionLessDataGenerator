import json


class node(object):
    nodeID = ""
    C: int = 0
    S: int = 0
    PUE: float = 0
    EC: float = 0
    ES: float = 0
    PN: int = 0
    RP: float = 0
    AD: list = None
    ifEdge: int = 0

    def __init__(self, initlist=None) -> None:
        if initlist:
            self.nodeID = str(initlist[0])
            self.C = int(initlist[1])
            self.S = int(initlist[2])
            self.PUE = float(initlist[3])
            self.EC = float(initlist[4])
            self.ES = float(initlist[5])

            self.PN = int(initlist[6])
            self.AD = json.loads(initlist[7])
            self.RP = float(initlist[8])
            self.ifEdge: int(initlist[9])
        pass

    def accessDelay(self, location):
        return


class Provider(object):
    nodeList = None
    C = None
    S = None
    PUE = None
    EC = None
    ES = None
    PN = None
    RP = None
    BW = None
    RTT = None
    DIS = None
    BWP = None

    def __init__(self) -> None:
        self.nodeList = list()

    def getNodeList(self):
        pass

    def getNodeMap(self):
        pass
