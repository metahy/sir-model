import pandas
import csv
import random
 
# node_df = pandas.read_csv('E:/data/节点.csv')
# all_nodes_list = node_df.values.tolist()  #获取文件中所有节点
all_nodes_list = ["老王", "老张", "老李", "小张", "小王", "老李"]  #获取文件中所有节点
 
edge = [("老王", "老张"), ("老王", "老李"), ("老李", "老王"), ("老张", "老王"), ("小张", "老张"), ("小王", "老王"), ("小李", "老李"), ("小张", "小王")]   #获取所有边
# with open('E:/data/边.csv','r',encoding='utf-8-sig') as f: 
#     data = f.readlines()  
#     for line in data: 
#         line = list(line.replace('\r','').replace('\n','').replace('\t','').split(','))
#         single_edge = tuple([line[1],line[4]])
#         edge.append(single_edge)

"""========================="""

import networkx as nx
ba = nx.Graph()
ba.add_edges_from(edge)
for node in ba.nodes():
    ba.nodes[node]["state"] = "S"

"""========================="""

import random
 
# 根据 SIR 模型，更新单一节点的状态
def updateNodeState(G,node, alpha, beta):
    if G.nodes[node]["state"] == "I": #感染者
        p = random.random() # 生成一个0到1的随机数
        if p < beta:   # gamma的概率恢复
            G.nodes[node]["state"] = "R" #将节点状态设置成“R”
    elif G.nodes[node]["state"] == "S": #易感者
        p = random.random() # 生成一个0到1的随机数
        k = 0  # 计算邻居中的感染者数量
        for neibor in G.adj[node]: # 查看所有邻居状态，遍历邻居用 G.adj[node]
            if G.nodes[neibor]["state"] == "I": #如果这个邻居是感染者，则k加1
                k = k + 1
        if p < 1 - (1 - alpha)**k:  # 易感者被感染
            G.nodes[node]["state"] = "I" 

"""========================="""

def updateNetworkState(G, alpha, beta):
    for node in G: #遍历图中节点，每一个节点状态进行更新
        updateNodeState(G,node, alpha, beta)

"""========================="""

# 计算三类人群的数量
def countSIR(G):
    S = 0;I = 0
    for node in G:
        if G.nodes[node]["state"] == "S":
            S = S + 1
        elif G.nodes[node]["state"] == "I":
            I = I + 1
    return S,I, len(G.nodes) - S - I    

"""========================="""

#随机选取一个节点为初始感染者  
ba.nodes["老张"]["state"] = "I" 
 
days = 50 #设置模拟的天数
# alpha = 0.0003 #感染率
# beta = 0.10 #恢复率
alpha = 0.2  # 感染率
beta = 0.10  # 恢复率
 
#设置不同人群的显示颜色，易感者为橘色，感染者为红色，恢复者为绿色
color_dict = {"S":"orange","I":"red","R":"green"}   

"""========================="""

# 模拟天数为days，更新节点状态
import matplotlib.pyplot as plt
#fig,ax = plt.subplots(111)
# %matplotlib inline
import time
SIR_list = []
for t in range(0,days):
    updateNetworkState(ba,alpha,beta) #对网络状态进行模拟更新
    SIR_list.append(list(countSIR(ba))) #计算更新后三种节点的数量

"""========================="""

df = pandas.DataFrame(SIR_list,columns=["S","I","R"])
df.plot(figsize=(9,6),color=[color_dict.get(x) for x in df.columns])
plt.show()

"""========================="""

#fig,ax = plt.subplots(111)
# %matplotlib inline
# 获得所有节点的属性

# def get_last_node_state(all_nodes_list,G):
#     SIR_result = []
#     for item in all_nodes_list:
#         node_attri = []
#         node_attri.extend(item)
#         try:
#             for node in G.nodes():
#                 G.nodes[node]["state"] = "S"   #将网络中所有节点设为健康者
#             G.nodes[str(item[0])]["state"] = "I"    #将某一节点设为感染者
#             for t in range(0,days):
#                 updateNetworkState(G,beta,gamma)  #对网络状态进行模拟更新
#             node_result = pandas.DataFrame([i[1] for i in G.nodes(data=True)], index=[i[0] for i in G.nodes(data=True)])
#             state_count = node_result.groupby('state')['label'].count().to_dict() #按感染情况分组
#             R_count = state_count['R']   #计算恢复者数量
#             node_attri.append(R_count)
#             SIR_result.append(node_attri)
#         except Exception as e:
#             print(e)              
#     return SIR_result   #返回结果形式为[节点id,节点接触到的人数（恢复者人数）]
 
# #执行函数
# SIR_result = get_last_node_state(all_nodes_list,ba)