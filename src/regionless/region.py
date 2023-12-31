from . import instance
import copy
from . import timecount
import json
import math

keylist = [
    "w1", "w2", "e1", "e2", "e3", "edw1", "edw2", "ede1", "ede2",
    "ede3"
]


# 定义资源节点的定义及其属性
class node(object):
    nodeID = ""
    C: int = 0
    S: int = 0
    PUE: float = 0
    EC: float = 0
    ES: float = 0
    PN: int = 0
    AD: list = None
    RP: float = 0
    ifEdge: int = 0

    r_C: int = 0
    r_S: int = 0

    insDict = {}
    Aglist = {}

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
            self.r_C = self.C
            self.r_S = self.S
            self.insDict = {}
            self.Aglist = {}
        pass

    @timecount.timefn
    def addInstance(self, ins: instance.Instance):
        self.r_C = self.r_C - ins.cpuRequest
        self.r_S = self.r_S - ins.diskRequest
        self.insDict[ins.instanceID] = ins

    def removeInstance(self, ins: instance.Instance):
        self.r_C = self.r_C + ins.cpuRequest
        self.r_S = self.r_S + ins.diskRequest
        self.insDict.pop(ins.instanceID)

    def getInstances(self):
        return self.insDict

    def accessDelay(self, location):
        # 计算站点到某一location的时延
        return

    @timecount.timefn
    def addAgi(self, Ag):
        temp = instance.Instance(Ag[3])
        temp.initValue(int(Ag[4]), int(Ag[5]), int(Ag[6]), Ag[7])
        self.addInstance(temp)
        return

    def addWholeAg(self, Ag):
        if self.r_C - Ag[3] < 0 or self.r_S - Ag[5] < 0:
            self.Aglist[Ag[1]] = Ag
            self.r_C = self.r_C - Ag[3]
            self.r_S = self.r_S - Ag[5]
            return False
        else:
            self.Aglist[Ag[1]] = Ag
            self.r_C = self.r_C - Ag[3]
            self.r_S = self.r_S - Ag[5]
            return True

    def removeAg(self, Ag):
        self.Aglist.pop(Ag[1])
        self.r_C = self.r_C + Ag[3]
        self.r_S = self.r_S + Ag[5]


class Provider(object):
    nodeDict = None
    nodeMap = None
    C = None
    S = None
    PUE = None
    EC = None
    ES = None
    PN = None
    RP = None
    BW = {}
    RTT = {}
    DIS = {}
    BWP = {}
    BWPDIS = {}

    r_C = {}
    r_S = {}
    r_BW = {}

    AgMap = None

    user = {}

    RTTLIST = []

    error_list = []

    def __init__(self) -> None:
        self.nodeDict = {}
        self.nodeMap = {}

    def addRegion(self, n: node):
        self.nodeDict[n.nodeID] = n

    def removeRegion(self, n: node):
        self.nodeDict.pop(n.nodeID)

    def addRegionMap(self, n1: node, n2: node, value):
        self.nodeMap[(n1.nodeID, n2.nodeID)] = value
        self.nodeMap[(n2.nodeID, n1.nodeID)] = value
        pass

    def removeRegionMap(self, n1: node, n2: node, value):
        self.nodeMap.pop((n1.nodeID, n2.nodeID))
        pass

    # 进行数据的更新和初始化
    def init(self):
        for m in self.nodeMap:
            self.BW[m] = int(self.nodeMap[m][2])
            self.RTT[m] = int(self.nodeMap[m][3])
            self.DIS[m] = float(self.nodeMap[m][4])
            self.BWP[m] = int(self.nodeMap[m][5])
            self.BWPDIS[m] = float(self.nodeMap[m][4]) * int(
                self.nodeMap[m][5])
        self.r_BW = copy.deepcopy(self.BW)
        for m in self.nodeDict:
            self.r_C[m] = self.nodeDict[m].r_C
            self.r_S[m] = self.nodeDict[m].r_S
        self.C = copy.deepcopy(self.r_C)
        self.S = copy.deepcopy(self.r_S)
        pass

    def getNodeList(self):
        pass

    def getNodeMap(self):
        pass

    # 计算TCO,直接使用参数
    def TCO(self):
        score = 0
        EC = 0
        RC = 0
        BC = 0
        for k in self.nodeDict:
            n = self.nodeDict[k]
            s_EC = (n.C - n.r_C) * n.EC + (n.S - n.r_S) * n.ES
            s_RC = math.ceil((n.C - n.r_C) / n.PN) * n.RP
            EC += s_EC
            RC += s_RC
            score = score + s_EC + s_RC
        s_BC = 0
        for key in self.nodeMap:
            s_BC = s_BC + (self.BW[key] -
                           self.r_BW[key]) * self.BWP[key] * self.DIS[key]
        BC = s_BC / 2
        return score + s_BC / 2, EC, RC, BC

    # 计算TCO,直接使用参数
    def TCOfromAG(self):
        score = 0
        EC = 0
        RC = 0
        BC = 0
        for k in self.nodeDict:
            n = self.nodeDict[k]
            s_EC = (n.C - n.r_C) * n.EC + (n.S - n.r_S) * n.ES
            s_RC = (n.C - n.r_C) / n.PN * n.RP
            EC += s_EC
            RC += s_RC
            score = score + s_EC + s_RC
        s_BC = 0
        for key in self.nodeMap:
            s_BC = s_BC + (self.BW[key] -
                           self.r_BW[key]) * self.BWP[key] * self.DIS[key]
        BC = s_BC / 2
        return score + s_BC / 2, EC, RC, BC

    # @timecount.do_cprofile("./mkm_run.prof")
    def addAg(self, Ag: list, targetnode: node):
        # 首先，给对应的node加入这个Ag
        self.nodeDict[targetnode.nodeID].addAgi(Ag)

        # 更新当前的剩余资源量
        self.r_C[targetnode.nodeID] = self.nodeDict[targetnode.nodeID].r_C
        self.r_S[targetnode.nodeID] = self.nodeDict[targetnode.nodeID].r_S
        # 检查这个用户的其他Ag放在了哪里
        # 更新r_bW
        # if(Ag[0] in self.user):
        #     # for oldAg in self.user[Ag[0]]:
        #     #     oldAgID=oldAg[0]
        #     #     targetID=oldAg[1]
        #     #     # 找到对于所需要的BW
        #     #     bw_r=self.AgMap[(oldAgID,Ag[1])][3]
        #     #     if(targetID!=targetnode.nodeID):
        #     #         # 减去对于需要的BW
        #     #         self.r_BW[(targetID,targetnode.nodeID)]=self.r_BW[(targetID,targetnode.nodeID)]-bw_r
        #     #         self.r_BW[(targetnode.nodeID,targetID)]=self.r_BW[(targetnode.nodeID,targetID)]-bw_r
        #     self.user[Ag[0]].append([Ag[1],targetnode.nodeID])
        # else:
        #     self.user[Ag[0]]=[[Ag[1],targetnode.nodeID]]

    @timecount.timefn
    def addWholeAg(self, Ag: list, targetnode: node):
        # 首先，给对应的node加入这个Ag
        # 检查gdpr冲突和接入时延冲突
        if len(Ag[2]) == 0 or (keylist.index(targetnode.nodeID) in Ag[2] or keylist.index(targetnode.nodeID)-5 in Ag[2]):
            pass
        else:
            self.error_list.append([Ag,targetnode.nodeID,"gdpr run out!", Ag, targetnode.nodeID])

        if len(Ag[6]) != 0:
            for i in range(len(Ag[6])):
                if Ag[6][i] < targetnode.AD[i]:
                    self.error_list.append([Ag,targetnode.nodeID,"AD run out!", Ag, targetnode.AD])
                    break

        # 检查资源冲突
        if self.nodeDict[targetnode.nodeID].addWholeAg(Ag) is False:
            self.error_list.append([Ag,targetnode.nodeID,"resource run out!", Ag, targetnode.r_C, targetnode.r_S])

        # 更新当前的剩余资源量
        self.r_C[targetnode.nodeID] = self.nodeDict[targetnode.nodeID].r_C
        self.r_S[targetnode.nodeID] = self.nodeDict[targetnode.nodeID].r_S
        flag_BW = 0
        flag_RTT = 0
        if Ag[0] in self.user:
            self.user[Ag[0]].append([Ag[1], targetnode.nodeID, Ag])
            for oldAg in self.user[Ag[0]]:
                oldAgID = oldAg[0]
                targetID = oldAg[1]
                # 找到对于所需要的BW
                bw_r = self.AgMap[Ag[0]][(oldAgID, Ag[1])][3]
                if targetID != targetnode.nodeID:
                    if flag_BW == 0 and self.r_BW[(targetID, targetnode.nodeID)] - bw_r < 0:
                        self.error_list.append([Ag, targetnode.nodeID,"bw run out!", Ag, self.r_BW[(targetID, targetnode.nodeID)]])
                        flag_BW = 1
                    if flag_RTT == 0 and self.RTT[(targetID, targetnode.nodeID)] > self.AgMap[Ag[0]][(oldAgID, Ag[1])][4]:
                        self.error_list.append([Ag, targetnode.nodeID, "rtt run out!", self.AgMap[Ag[0]][(oldAgID, Ag[1])][4], self.RTT[(targetID, targetnode.nodeID)]])
                        flag_RTT = 1

                    self.r_BW[(targetID, targetnode.nodeID)] = self.r_BW[(targetID, targetnode.nodeID)] - bw_r
                    self.r_BW[(targetnode.nodeID, targetID)] = self.r_BW[(targetnode.nodeID, targetID)] - bw_r
        else:
            self.user[Ag[0]] = [[Ag[1], targetnode.nodeID, Ag]]

    @timecount.timefn
    def remove(self, reAg: list):
        _nodeID = reAg[1]
        self.nodeDict[_nodeID].removeAg(reAg[2])

        self.r_C[_nodeID] = self.nodeDict[_nodeID].r_C
        self.r_S[_nodeID] = self.nodeDict[_nodeID].r_S
        if reAg[2][0] in self.user:
            index = 0
            target = 0
            for oldAg in self.user[reAg[2][0]]:
                oldAgID = oldAg[0]
                if (oldAgID != reAg[2][1]):
                    targetID = oldAg[1]
                    # 找到对于所需要的BW
                    bw_r = self.AgMap[reAg[2][0]][(oldAgID, reAg[2][1])][3]
                    if targetID != _nodeID:
                        self.r_BW[(
                            targetID,
                            _nodeID)] = self.r_BW[(targetID, _nodeID)] + bw_r
                        self.r_BW[(
                            _nodeID,
                            targetID)] = self.r_BW[(_nodeID, targetID)] + bw_r
                else:
                    target = index
                index += 1
            self.user[reAg[2][0]].pop(target)
            if (len(self.user[reAg[2][0]]) == 0):
                self.user.pop(reAg[2][0])
        else:
            pass

    def show(self):
        print(self.r_C)
        print("link:\t", "Used:\t", "Remain:\t")
        for key in self.r_BW:
            print(key,
                  int(self.BW[key]) - int(self.r_BW[key]), int(self.r_BW[key]))
        # for key in self.user:
        #     for Ag in self.user[key]:
        #         print(Ag)
        print("CPU")
        for key in self.nodeDict:
            print(key, ":",
                  (self.C[key] - self.r_C[key]) * 1.0 / self.C[key] * 100, "%",
                  "Ag:", len(self.nodeDict[key].Aglist))

        print("Storage")
        for key in self.r_S:
            5
            print(key, ":",
                  (self.S[key] - self.r_S[key]) * 1.0 / self.S[key] * 100, "%")

        keylist = [
            "w1", "w2", "e1", "e2", "e3", "edw1", "edw2", "ede1", "ede2",
            "ede3"
        ]
        print(keylist)
        for key1 in keylist:
            s = key1
            for key2 in keylist:
                key = (key1, key2)
                if (key1 == key2):
                    s = s + "," + "-1"
                else:
                    s = s + "," + str(int(self.BW[key]) - int(self.r_BW[key]))
            print(s)
        print(keylist)
        for key1 in keylist:
            s = key1
            for key2 in keylist:
                key = (key1, key2)
                if (key1 == key2):
                    s = s + "," + "-1"
                else:
                    s = s + "," + str(int(self.r_BW[key]))
            print(s)
        for key1 in keylist:
            s = '['
            for key2 in keylist:
                key = (key1, key2)
                if (key1 == key2):
                    s = s + "0" + ","
                else:
                    s = s + str(int(self.BWP[key] * self.DIS[key])) + ","
            print(s+'],')
