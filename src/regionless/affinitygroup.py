from random import randint, shuffle
from uuid import uuid4
from . import instance
import math

globalaffdefault = [[0, 200], [100, 1000], [0, 10]]


class affinityGroup(object):  # 创建Circle类
    affinityGroupID = ""
    instanceList = None

    gdpr = None  # gdpr约束
    loca = None  # 通信亲和组位置

    accessDelay: int = math.inf

    def __init__(self, ID):
        self.instanceList = list()
        self.affinityGroupID = str(ID)
        self.gdpr = list()

    # def initAttribute(self):
    #     self.gdpr=[[0]* 1 for i in range(len(self.affinityGroups))]
    #     self.loca=[[0]* 1 for i in range(len(self.affinityGroups))]


class UserRequest(object):
    instances = None
    affinityGroups = None

    br = None  # 带宽约束
    rtt = None  # 时延约束
    location: int = 0

    default = globalaffdefault

    def __init__(self):
        self.instances = list()
        self.affinityGroups = list()

    def initAttribute(self):
        self.rtt = [[0] * len(self.affinityGroups)
                    for i in range(len(self.affinityGroups))]
        self.br = [[0] * len(self.affinityGroups)
                   for i in range(len(self.affinityGroups))]
        self.gdpr = [[0] * 1 for i in range(len(self.affinityGroups))]
        self.loca = [[0] * 1 for i in range(len(self.affinityGroups))]

    def randintp(self, GDPR_Range):
        max = 0
        for r in GDPR_Range:
            max += r
        result = randint(0, max)
        last = 0
        now = 0
        for i in range(0, len(GDPR_Range)):
            now += GDPR_Range[i]
            if (now >= result and last < result):
                return i
            else:
                last = now

    def randintlist(self, range_rand):
        r = []
        for rr in range_rand:
            r.append(randint(rr[0], rr[1]))
        return r

    def checkIfReal(self, Adlist, regionlist):
        for region in regionlist:
            AD_ag = Adlist
            AD_FLAG = 1

            for i in range(0, len(AD_ag)):
                if (AD_ag[i] < region[i]):
                    AD_FLAG = 0
                    break
            if (AD_FLAG == 1):
                return True
        return False

    def checkIfRealSingle(self, Adlist, regionlist, target):

        for region in regionlist:
            AD_ag = Adlist
            if (AD_ag[target] >= region[target]):
                return True
        return False

    def randInitAttribute(self, GDPR_Percent, GDPR_Range, AD_PERCENT, AD_WorE,
                          AD_W_Range, AD_E_Range, regionlist):

        for i in range(0, len(self.affinityGroups)):
            for j in range(0, len(self.affinityGroups)):
                if (i == j):
                    continue
                if (self.br[i][j] == 0):
                    self.br[i][j] = randint(self.default[0][0],
                                            self.default[0][1])  # 随机带宽
                    self.br[j][i] = self.br[i][j]  # 随机带宽
                if (self.rtt[i][j] == 0):
                    self.rtt[i][j] = randint(self.default[1][0],
                                             self.default[1][1])  # 随机rtt
                    self.rtt[j][i] = self.rtt[i][j]
            self.gdpr[i] = None  # 随机gdpr请求

        # 修改gdpr
        gdpr_r = randint(0, 100)
        if (gdpr_r < GDPR_Percent):
            index = randint(0, len(self.affinityGroups) - 1)
            for i in range(0, len(GDPR_Range)):
                temp = randint(0, 100)
                if (temp < GDPR_Range[i]):
                    self.affinityGroups[index].gdpr.append(i)
        else:
            # 修改接入时延约束
            ad_r = randint(0, 100)
            if (ad_r < AD_PERCENT):
                index = randint(0, len(self.affinityGroups) - 1)
                r = []
                ad_WorE = randint(0, 100)
                if (ad_WorE < AD_WorE):
                    r = self.randintlist(AD_W_Range)
                    while (self.checkIfReal(r, regionlist) is not True):
                        r = self.randintlist(AD_W_Range)
                    for ri in range(2, 5):
                        if (randint(0, 100) < 50):
                            r[ri] = math.inf
                else:
                    r = self.randintlist(AD_E_Range)
                    while (self.checkIfReal(r, regionlist) is not True):
                        r = self.randintlist(AD_E_Range)
                    for ri in range(0, 2):
                        if (randint(0, 100) < 50):
                            r[ri] = math.inf
                for ins in self.affinityGroups[index].instanceList:
                    ins.latencyRequest = list(r)

    def randInitAttributewithADRange(self, GDPR_Percent, GDPR_Range,
                                     AD_PERCENT, AD_Range, AD_W_Range,
                                     AD_E_Range, regionlist):

        for i in range(0, len(self.affinityGroups)):
            for j in range(0, len(self.affinityGroups)):
                if (i == j):
                    continue
                if (self.br[i][j] == 0):
                    self.br[i][j] = randint(self.default[0][0],
                                            self.default[0][1])  # 随机带宽
                    self.br[j][i] = self.br[i][j]  # 随机带宽
                if (self.rtt[i][j] == 0):
                    self.rtt[i][j] = randint(self.default[1][0],
                                             self.default[1][1])  # 随机rtt
                    self.rtt[j][i] = self.rtt[i][j]
            self.gdpr[i] = None  # 随机gdpr请求

        # 修改gdpr
        gdpr_r = randint(0, 100)
        if (gdpr_r < GDPR_Percent):
            index = randint(0, len(self.affinityGroups) - 1)
            for i in range(0, len(GDPR_Range)):
                temp = randint(0, 100)
                if (temp < GDPR_Range[i]):
                    self.affinityGroups[index].gdpr.append(i)
        else:
            # 修改接入时延约束
            ad_r = randint(0, 100)
            if (ad_r < AD_PERCENT):
                index = randint(0, len(self.affinityGroups) - 1)
                r = []
                ad_WorE = randint(0, 100)
                sum = 0
                target = 0
                for p_index in range(len(AD_Range)):
                    if (ad_WorE >= sum) and (ad_WorE <
                                             sum + AD_Range[p_index]):
                        target = p_index
                        break
                    sum += AD_Range[p_index]

                if (target == 0 or target == 1):
                    r = self.randintlist(AD_W_Range)
                    while (self.checkIfRealSingle(r, regionlist, target)
                           is not True):
                        r = self.randintlist(AD_W_Range)
                    for ri in range(0, len(r)):
                        if (ri != target):
                            r[ri] = math.inf
                else:
                    r = self.randintlist(AD_E_Range)
                    while (self.checkIfRealSingle(r, regionlist, target)
                           is not True):
                        r = self.randintlist(AD_E_Range)
                    for ri in range(0, len(r)):
                        if (ri != target):
                            r[ri] = math.inf
                self.location = target
                self.affinityGroups[index].accessDelay = r[target]

                for ins in self.affinityGroups[index].instanceList:
                    ins.latencyRequest = list(r)

    def newInstance(self, instancenum, wholeCPU=None):
        uuidset = set()

        while (len(uuidset) < instancenum):
            uuidset.add(uuid4())
        if (wholeCPU is None):
            for i in range(0, instancenum):
                temp = instance.Instance(list(uuidset)[i])
                temp.randValue()
                self.instances.append(temp)
        else:
            randset = set()
            while (len(randset) < instancenum - 1):
                randset.add(randint(1, wholeCPU - 1))

            randlist = list(randset)
            randlist.sort()
            last = 0
            index = 0
            for r in randlist:
                num = r - last
                last = r
                temp = instance.Instance(list(uuidset)[index])
                temp.randValue()
                temp.cpuRequest = num
                self.instances.append(temp)
                index = index + 1
            num = wholeCPU - last
            temp = instance.Instance(list(uuidset)[index])
            temp.randValue()
            temp.cpuRequest = num
            self.instances.append(temp)

    def newaffinityGroups(self, agindex, gnum=3):

        uuidset = set()
        while (len(uuidset) < gnum):
            uuidset.add(agindex[0])
            agindex[0] += 1

        randset = set()
        while (len(randset) < gnum - 1):
            randset.add(randint(1, len(self.instances) - 1))

        numlist = list(range(0, len(self.instances)))
        shuffle(numlist)
        randlist = list(randset)
        randlist.sort()

        # print(randlist)

        last = 0
        index = 0
        for r in randlist:
            temp = affinityGroup(list(uuidset)[index])
            ll = list()
            ll = numlist[last:r]
            last = r
            for num in ll:
                temp.instanceList.append(self.instances[num])
            self.affinityGroups.append(temp)
            index = index + 1

        temp = affinityGroup(list(uuidset)[index])
        ll = list()
        ll = numlist[last:]
        for num in ll:
            temp.instanceList.append(self.instances[num])
        self.affinityGroups.append(temp)

        # for a in self.affinityGroups:
        #     print(len(a.instanceList))
        # print(len(self.instances))

    # def __str__(self):
    #     return "instances:"+self.instances.__str__()


class User(object):
    userID = None
    userRequest: UserRequest = None

    def getAgList(self):
        csvlist = list()

        for ag in self.userRequest.affinityGroups:
            if (len(ag.instanceList) == 0):
                print("!!!!!!!!!!!!!!!!")
            for ins in ag.instanceList:
                insvalue = ins.getValue()
                csvlist.append([self.userID, ag.affinityGroupID, ag.gdpr] +
                               insvalue +
                               [self.userRequest.location, ag.accessDelay])

        return csvlist

    def getAgMap(self):
        csvmap = list()

        for i in range(0, len(self.userRequest.affinityGroups)):
            for j in range(0, len(self.userRequest.affinityGroups)):
                # csvmap.append()
                agi = self.userRequest.affinityGroups[i]
                agj = self.userRequest.affinityGroups[j]

                csvmap.append([
                    self.userID, agi.affinityGroupID, agj.affinityGroupID,
                    self.userRequest.rtt[i][j], self.userRequest.br[i][j]
                ])
        return csvmap

    def __init__(self, ID):
        self.userID = ID
        self.userRequest = UserRequest()

    def __str__(self):
        return str(self.userID)

    def __repr__(self):
        return str(self.userID)
