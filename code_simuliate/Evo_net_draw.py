# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 15:52:42 2024

@author: 13419
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import time
 


"0.参数设置"
#博弈论次
# i_num=30
# #每个群体内的个体数量
# i1=50
# i2=150
# i3=450

# #小世界的邻居数量，随机重连概率
# Ws_n1=5
# Ws_n2=5
# Ws_n3=5
# Ws_p1=0.3
# Ws_p2=0.3
# Ws_p3=0.3

# #初始比例a，a为选择共创的比例

# a1=0.5
# a2=0.5
# a3=0.5

# #收益计算参数
# b1=300
# b2=50
# b3=10

# pg=0.4 #电价
# w=0.3   #上网电价 kwh 千瓦时
# wg=0.6  #电网售电电价
# sub1=0.05 #补贴电价 kwh 千瓦时
#         #售电量 kwh 兆瓦时，k个博弈对象选择买氢，再加上每个分别买的量
# c1=30   #策略成本

# ph=28     #氢价，元/每千克 按照每公斤氢气消耗45度电算，原材料成本约等于45*0.3=13.5元
# c_h=7.5   #制氢单位成本 制氢装备折旧+运营费  0.67*11.2=7.5
# sub2=0.1               #电价补贴
# vg_perh=50         #购电量  1kgH2约耗电50度
# c2=10     #策略成本 

# pother=30  #氢气市场价约为28元每千克，2024年5月
# vh_buy=50   #用氢量
# sub3=1   #每千克氢气补贴价格
# c3=1 #用氢设备费及人工费用等
# P_carbon=0.096 #每公斤碳额度的价格
# C_carbon=18  #传统方式每公斤排碳量


def evogame(i_num=30,#每个群体内的个体数量
i1=50,
i2=150,
i3=450,

#小世界的邻居数量，随机重连概率
Ws_n1=5,
Ws_n2=5,
Ws_n3=5,
Ws_p1=0.3,
Ws_p2=0.3,
Ws_p3=0.3,

#初始比例a，a为选择共创的比例

a1=0.5,
a2=0.5,
a3=0.5,

#收益计算参数
b1=300,
b2=50,
b3=10,

pg=0.4, #电价
w=0.3,  #上网电价 kwh 千瓦时
wg=0.6,  #电网售电电价
sub1=0.05, #补贴电价 kwh 千瓦时
        #售电量 kwh 兆瓦时，k个博弈对象选择买氢，再加上每个分别买的量
c1=30,   #策略成本

ph=28,     #氢价，元/每千克 按照每公斤氢气消耗45度电算，原材料成本约等于45*0.3=13.5元
c_h=7.5,   #制氢单位成本 制氢装备折旧+运营费  0.67*11.2=7.5
sub2=0.1,               #电价补贴
vg_perh=50,         #购电量  1kgH2约耗电50度
c2=300,     #策略成本 

pother=30,  #氢气市场价约为28元每千克，2024年5月
vh_buy=50,   #用氢量
sub3=1,   #每千克氢气补贴价格
c3=1, #用氢设备费及人工费用等
P_carbon=0.096, #每公斤碳额度的价格
C_carbon=18,  #传统方式每公斤排碳量
        ):
    "1.生成层内邻接矩阵"
    #上层G1，中层G2，下层G3均为NW或者WS小世界网络
    # 生成一个含有20个节点、每个节点有4个邻居、以概率p=0.3随机化重连边的WS小世界网络
    G1 = nx.random_graphs.watts_strogatz_graph(i1, Ws_n1, Ws_p1)
    G2 = nx.random_graphs.watts_strogatz_graph(i2, Ws_n2, Ws_p2)
    G3 = nx.random_graphs.watts_strogatz_graph(i3, Ws_n3, Ws_p3)
    
    As1 = nx.adjacency_matrix(G1)
    As2 = nx.adjacency_matrix(G2)
    As3 = nx.adjacency_matrix(G3)
    
    # 转化成二维数组形式的矩阵
    A1 = As1.todense()
    A2 = As2.todense()
    A3 = As3.todense()
    
    
    "2.生成层内节点状态"
    #节点状态为S1，S2，S3
    
    
    s1=np.zeros((1,i1))
    indices1=np.random.choice(np.arange(s1.size),replace=False,size=int(s1.size*a1))
    s1[0][indices1]=1
    
    s2=np.zeros((1,i2))
    indices2=np.random.choice(np.arange(s2.size),replace=False,size=int(s2.size*a2))
    s2[0][indices2]=1
    
    s3=np.zeros((1,i3))
    indices3=np.random.choice(np.arange(s3.size),replace=False,size=int(s3.size*a3))
    s3[0][indices3]=1
    
    
    
    "3.博弈关系矩阵的生成"
    
    def gamerelation(i1,i2,i3):
        #层间博弈规则矩阵p1，p2,即博弈规则的变更
        p1 = np.zeros((i1,i2),int)
        p2 = np.zeros((i2,i3),int)    
        box1=[]
        for i in range(i2):
            p2[i,3*i+1]=1
            box1.append(3*i+1)
        for j in range(i3):
            if j not in box1:
                x = j//3
                if j%3<1:
                    x1=np.random.choice([x,x-1],p=[0.5,0.5])
                elif j%3>1:
                    if x==i2-1:
                        temp=0
                        x1=np.random.choice([x,temp],p=[0.5,0.5])
                    else:
                        x1=np.random.choice([x,x+1],p=[0.5,0.5])
                p2[x1,j]=1
        
        box2=[]
        for i in range(i1):
            p1[i,3*i+1]=1
            box2.append(3*i+1)
        for j in range(i2):
            if j not in box2:
                xx = j//3
                if j%3<1:
                    x11=np.random.choice([xx,xx-1],p=[0.5,0.5])
                elif j%3>1:
                    if xx==i1-1:
                        temp1=0
                        x11=np.random.choice([xx,temp1],p=[0.5,0.5])
                    else:
                        x11=np.random.choice([xx,xx+1],p=[0.5,0.5])
                p1[x11,j]=1 
                
    
        return p1,p2
        
    
    
    
    "5.收益值计算"
    #收益值的计算，收益值的计算与现博弈方的状态有关，基本可以分为现策略收益以及新策略收益，现策略收益计算=f(x1,x2) x1为己方策略，x2为对方策略
    #定义函数,都是选择策略1时候的收益
    def clcfit(i1,i2,i3,s1,s2,s3):
    
        p1,p2=gamerelation(i1,i2,i3)
        
        #计算前的参数构成
        k1=np.matmul(p1,(s2.T))          #k1为50*1,50个节点中每个节点邻居选1的数量
        k2=np.matmul((p1.T),(s1.T))      #k2表为150*1，表示中层的上游节点中有多少节点选1
        k3=np.matmul(p2,(s3.T))          #k3表示150*1，表示中层的下游节点中有多少节点选1
        k4=np.matmul((p2.T),(s2.T))      #k4表示450*1,表示下层的上游节点中有多少节点选1
        
        #开始计算
         
        vh_sell=k3*vh_buy      #150*1,表示150家制氢商的用氢气量
        vg_buy = vh_sell*vg_perh
        "收益的计算需要从下层开始，逐渐到上层，因为涉及到购氢量，售氢量，售电量等"
    
        f3=b3+(np.minimum(k4,np.ones((k4.shape)))*(pother-ph+sub3)*vh_buy-c3)*(s3.T)  #用户只考虑有没有卖绿氢的，没有就是基本收益,c3为氢燃料汽车购置成本
        
        
        #f2的收益量=下游节点购氢量*（氢价-单位成本）-购电量*电价-决策成本   购电量=下游节点购氢量*每千克氢气的电能消耗量
        #f2=下游节点购氢量*（氢价-单位成本）-（下游节点购氢量*每千克氢气的电能消耗量）*电价-决策成本
        #下游节点购氢量=k3*vh_buy
    
        L_carbon=P_carbon*C_carbon
        
        f2=b2+(vh_sell*(ph-c_h+L_carbon)-(vg_buy)*(pg-sub2)-c2)*(s2.T)  #r如果该制氢商上游节点没有绿电供应，则其受到亏损，需要买电网低谷电
         
        for i in range(s2.shape[1]):
            if s2[0,i]==1:
                if k2[i]==0:
                    tz=(vh_sell*(ph-c_h+L_carbon)-(vg_buy)*(wg-sub2)-c2)*(s2.T)
                    f2[i]=b2+tz[i]
                
        vg_sell=np.matmul(p1,vg_buy*(s2.T))            #应该为50*1，vg_sell应该为 vg_buy*(s2.T)    
        f1=b1+(pg-w+sub1)*vg_sell-c1
    
        for i in range(s1.shape[1]):
            if s1[0][i]==0:
                f1[i]=b1
            else:
                if k1[i]==0:
                    f1[i]=b1-c1
      
        return f1,f2,f3
    
    
    
    "6.状态变更规则"
    #状态变更由同层邻居影响以及自身博弈对象的影响共同决定
    #假设i点有n个邻居，k个邻居采用了与自身不同的策略，如果经过计算后该策略盈利更多，则i节点将以k/n的概率采用新策略。
    #状态变更的规则，状态的变更应该依据利益的大小，利益越高，选择该策略的概率应该会越大，所以，首先应该是比较收益大小，其次，选择更换策略的概率
    #基本思路，
    #判断邻居节点的策略与自身是否一致，
    #如果邻居中出现新的策略，那么该节点在目前的上下游状态下判断选择邻居策略后收益，
    #如果收益增大，则按照一定概率变异为新策略，概率p=0.1+差值百分比*(0.5-0.1)，
    #如果邻居节点没有新策略或者新策略没有提升收益，则保持原策略不变
    
    def gameplay(itrations):
        schange_1=[]
        schange_2=[]
        schange_3=[]
        #itrations = 3
        schange_1=np.zeros((itrations,i1))
        schange_2=np.zeros((itrations,i2))
        schange_3=np.zeros((itrations,i3))
    
        schange_1[0,]=s1
    
        k=0.1  #费米更新系数
        for i in range(itrations):
            schange_1[i,]=s1
            for j in range(i1):
                nei_index1=np.argwhere(A1[j]==1)  #邻居位置
                for p in nei_index1:
                    if s1[0,j]!=s1[0,p]:
                        s1_new=copy.deepcopy(s1)  #选择新策略后的s1_new
                        s1_new[0,j]=s1[0,p[0]] 
                        fit1,fit2,fit3=clcfit(i1,i2,i3,s1_new,s2,s3)
                        f_1,f_2,f_3=clcfit(i1,i2,i3,s1,s2,s3)
                        if fit1[j]>f_1[j]:
                            p11 = 1/(1+math.exp((f_1[j,0]-fit1[j,0])/k))  #费米更新
                            if np.random.rand(1,1)>1-p11:
                                s1[0,j]=s1[0,p[0]]
                            
            schange_2[i,]=s2
            for j in range(i2):
                nei_index2=np.argwhere(A2[j]==1)  #邻居位置
                for p in nei_index2:
                    if s2[0,j]!=s2[0,p]:
                        s2_new=copy.deepcopy(s2)  #选择新策略后的s1_new
                        s2_new[0,j]=s2[0,p[0]] 
                        fit1,fit2,fit3=clcfit(i1,i2,i3,s1,s2_new,s3)
                        f_1,f_2,f_3=clcfit(i1,i2,i3,s1,s2,s3)
                        if fit2[j]>f_2[j]:
                            p22 = 1/(1+math.exp((f_2[j,0]-fit2[j,0])/k))  #费米更新
                            if np.random.rand(1,1)>1-p22:
                                s2[0,j]=s2[0,p[0]]
            
            schange_3[i,]=s3
            for j in range(i3):
                nei_index3=np.argwhere(A3[j]==1)  #邻居位置
                for p in nei_index3:
                    if s3[0,j]!=s3[0,p]:
                        s3_new=copy.deepcopy(s3)  #选择新策略后的s1_new
                        s3_new[0,j]=s3[0,p[0]] 
                        fit1,fit2,fit3=clcfit(i1,i2,i3,s1,s2,s3_new)
                        f_1,f_2,f_3=clcfit(i1,i2,i3,s1,s2,s3)
                        if fit3[j]>f_3[j]:
                            p33 = 1/(1+math.exp((f_3[j,0]-fit3[j,0])/k))  #费米更新
                            if np.random.rand(1,1)>1-p33:
                                s3[0,j]=s3[0,p[0]]
            print("迭代中，次数：",i+1)
        
        game1=schange_1
        game2=schange_2
        game3=schange_3
        
        return game1,game2,game3
    


    schange_1,schange_2,schange_3=gameplay(i_num)     

    prob_1=(np.sum(schange_1,axis=1)).T/i1 
    prob_2=(np.sum(schange_2,axis=1)).T/i2
    prob_3=(np.sum(schange_3,axis=1)).T/i3
    return prob_1,prob_2,prob_3      

# =============================================================================
# box=[]
# for i in [0.3,0.4,0.5]:
#     pg=i
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(1)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,Pg=0.3','HM,Pg=0.3','HU,Pg=0.3','REG,Pg=0.4','HM,Pg=0.4','HU,Pg=0.4','REG,Pg=0.5','HM,Pg=0.5','HU,Pg=0.5'],fontsize=8)
# pg=0.4
# 
# box=[]
# for j in [25,28,31]:
#     ph=j
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(2)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,Ph=25','HM,Ph=25','HU,Ph=25','REG,Ph=28','HM,Ph=28','HU,Ph=28','REG,Ph=31','HM,Ph=31','HU,Ph=31'],fontsize=8)
# ph=28
# 
# box=[]
# for j in [40,50,60]:
#     vg_perh=j
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(3)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,Vg_per=40','HM,Vg_per=40','HU,Vg_per=40','REG,Vg_per=50','HM,Vg_per=50','HU,Vg_per=50','REG,Vg_per=60','HM,Vg_per=60','HU,Vg_per=60'],fontsize=8)
# vg_perh=50
# 
# box=[]
# for j in [[0,0,0],[0.05,0.1,1],[0.1,0.2,2]]:
#     sub1,sub2,sub3=j
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(4)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,S=0','HM,S=0','HU,S=0','REG,S=base','HM,S=base','HU,S=base','REG,S=high','HM,S=high','HU,S=high'],fontsize=8)
# sub1,sub2,sub3=[0.05,0.1,1]
# 
# box=[]
# for j in [0.067,0.096,0.125]:
#     P_carbon=j
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(5)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,P_carbon=0.067','HM,P_carbon=0.067','HU,P_carbon=0.067','REG,P_carbon=0.096','HM,P_carbon=0.096','HU,P_carbon=0.096','REG,P_carbon=0.125','HM,P_carbon=0.125','HU,P_carbon=0.125'],fontsize=8)
# P_carbon=0.096
# 
# box=[]
# for j in [25,30,35]:
#     pother=j
#     y1,y2,y3=evogame()
#     lines=[y1,y2,y3]
#     box.append(lines)
# plt.figure(6)
# plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
# plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
# plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
# 
# plt.plot(box[1][0],color="r",linestyle="--",linewidth=1)
# plt.plot(box[1][1],color="g",linestyle="--",linewidth=1)
# plt.plot(box[1][2],color="b",linestyle="--",linewidth=1)
# 
# plt.plot(box[2][0],color="r",linestyle="-.",linewidth=1)
# plt.plot(box[2][1],color="g",linestyle="-.",linewidth=1)
# plt.plot(box[2][2],color="b",linestyle="-.",linewidth=1)
# 
# plt.xlabel("Time")
# plt.ylabel("Proportion")
# plt.legend(['REG,pother=25','HM,pother=25','HU,pother=25','REG,pother=30','HM,pother=30','HU,pother=30','REG,pother=35','HM,pother=35','HU,pother=35'],fontsize=8)
# pother=30
# 
# =============================================================================


