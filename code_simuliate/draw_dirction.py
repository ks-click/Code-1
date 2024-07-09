# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 23:50:27 2024

@author: JkSun
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
i1=10
i2=30
i3=90

def plot_ellipse(a, b):
    theta = np.linspace(0, 2 * np.pi, i3)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    #plt.plot(x, y)
    return x,y

# 椭圆的长半轴和短半轴
a = 7
b = 2

def plot_ellipse1(a, b):
    theta = np.linspace(0, 2 * np.pi, i2)
    x = a * np.cos(theta)
    y = b * np.sin(theta)+4
    #plt.plot(x, y)
    return x,y

def plot_ellipse2(a, b):
    theta = np.linspace(0, 2 * np.pi, i1)
    x = a * np.cos(theta)
    y = b * np.sin(theta)+8
    #plt.plot(x, y)
    return x,y


x,y=plot_ellipse(a, b)
x1,y1=plot_ellipse1(5, 1)
x2,y2=plot_ellipse2(3, 0.5)
# #plt.title('Ellipse')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.axis('equal')  # Equal scaling ensures that the plot is a circle.
# plt.grid(True)
# plt.axis("on")
# plt.xlim([-10,10])
# plt.show()

i1=10
i2=30
i3=90
Ws_n1=5
Ws_n2=5
Ws_n3=5
Ws_p1=0.3
Ws_p2=0.3
Ws_p3=0.3
G1 = nx.random_graphs.watts_strogatz_graph(i1, Ws_n1, Ws_p1)
G2 = nx.random_graphs.watts_strogatz_graph(i2, Ws_n2, Ws_p2)
G3 = nx.random_graphs.watts_strogatz_graph(i3, Ws_n3, Ws_p3)

G = nx.disjoint_union(G1, G2)
G = nx.disjoint_union(G,G3)

for u,v in G.edges():
    G[u][v]["color"]="#67180E"


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

p1,p2= gamerelation(i1, i2, i3)
list=[]
for i in range(i1):
    for j in range(i2):
        if p1[i,j] == 1:
            list.append((i,j+i1))

for i in range(i2):
    for j in range(i3):
        if p2[i,j] == 1:
            list.append((i+i1,j+i1+i2))

G.add_edges_from(list)

for j,k in list:
    G[j][k]["color"]="#0E5D67"

pos={}
for i in range(i1+i2+i3):
    if i <i1 :
        pos[i]=[x2[i],y2[i]]
    elif i < i1+i2:
        pos[i]=[x1[i-i1],y1[i-i1]]
    elif i < i1+i2+i3:
        pos[i]=[x[i-i1-i2],y[i-i1-i2]]


for i in range(i1+i2+i3):
    if i < i1:
        G.nodes[i]['color'] = '#9C1C1E'
    elif i< i1+i2:
        G.nodes[i]['color'] = '#1E9C1C'
    elif i < i1+i2+i3:
        G.nodes[i]['color'] = '#1C1E9C'

colors = nx.get_node_attributes(G, 'color').values()
edge_colors = [G[u][v]['color'] for u,v in G.edges()]
plt.figure(1)
plt.rcParams['figure.figsize']= (4, 4)      # 设置画布大小
plt.xlim([-8,8])
#plt.ylim([-8,8])
            
nx.draw(G,node_size=20,with_labels = 0,pos=pos,edge_color=edge_colors,node_color=colors,width=0.5)        
