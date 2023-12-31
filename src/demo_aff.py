from random import randint
from regionless import affinitygroup
import csv
import datetime
from tqdm import tqdm
import json
from regionless import instance
import os
# 以下参数控制数据集
# 控制具有GDPR约束的通信亲和组比例和地点比例
GDPR_Percent = 10
GDPR_Range = [20, 20, 20, 20, 20]
# 控制具有接入延迟约束的通信亲和组比例 和 亲和组比例
AD_PERCENT = 50
# 参数废弃
# AD_WorE=0.1
AD_Range = [5, 5, 30, 30, 30]
AD_W_Range = [[5, 15], [5, 15], [100, 300], [100, 300], [100, 300]]
AD_E_Range = [[100, 300], [100, 300], [5, 15], [5, 15], [5, 15]]

# 控制cpu比例
# cpu mem disk
instance.globalinsdefault = [50, 2000, 768]

# 控制AF随机比例
# 带宽 rtt
affinitygroup.globalaffdefault = [[90, 100], [50, 800]]

# 数量参数
wholeNumber = 20
instNumber = [10, 20]
affNumber = [3, 5]

now_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(now_time, '%Y%m%d%H%M%S')

aglist_a = []
agmap_a = []

pwd = os.getcwd()
url = os.path.join(pwd, "./dataset/csv")
AgMappath = os.path.join(url, "./AgMap" + time_str + ".csv")
AgListpath = os.path.join(url, "./AgList" + time_str + ".csv")
rglistcsv = os.path.join(pwd, "./dataset/regionlist.csv")

RegionList = []
agindex = [0]


def write_csv_file(path, head, data):
    try:
        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')

            if head is not None:
                writer.writerow(head)

            for row in data:
                writer.writerow(row)

            print("Write a CSV file to path %s Successful." % path)
    except Exception as e:
        print("Write an CSV file to path: %s, Case: %s" % (path, e))


try:
    with open(rglistcsv, encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        headers = next(reader)
        for row in reader:
            RegionList.append(json.loads(row[7]))
except Exception as e:
    print("read an CSV file to path: %s, Case: %s" % rglistcsv % (e))

try:
    with open(AgMappath, 'w', newline='') as csv_file_map:
        with open(AgListpath, 'w', newline='') as csv_file_list:
            writer_map = csv.writer(csv_file_map, dialect='excel')
            writer_list = csv.writer(csv_file_list, dialect='excel')

            writer_map.writerow(['userID', 'ag1', 'ag2', 'br', 'rtt'])
            writer_list.writerow([
                'userID', 'agID', 'gdpr', 'instanceID', 'cpu', 'mem', 'disk',
                'latencyGroup', 'region', 'latency'
            ])

            for i in tqdm(range(0, wholeNumber)):
                temp = affinitygroup.User(i)
                # 第一个参数是实例数量
                # wholeCPU表示总共的的CPU数量，不设定则随机
                temp.userRequest.newInstance(randint(instNumber[0],
                                                     instNumber[1]),
                                             wholeCPU=1000)
                temp.userRequest.newaffinityGroups(
                    agindex, randint(affNumber[0], affNumber[1]))
                temp.userRequest.initAttribute()
                temp.userRequest.randInitAttributewithADRange(
                    GDPR_Percent, GDPR_Range, AD_PERCENT, AD_Range, AD_W_Range,
                    AD_E_Range, RegionList)

                # # 控制gdpr数据比例
                # gdpr=randint(0,100)
                # gdpr_t=randint(0,50) % 10

                aglist = temp.getAgList()
                agmap = temp.getAgMap()

                for row in aglist:
                    writer_list.writerow(row)
                for row in agmap:
                    writer_map.writerow(row)

except Exception as e:
    print("Write an CSV file to path: %s, Case: %s" % (e))
