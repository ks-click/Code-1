# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 16:58:00 2024

@author: JkSun
"""

import Evo_net_draw as ED
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import time

box=[]
for i in np.around(np.arange(0.1,1,0.2),1):
    for j in np.around(np.arange(0.1,1,0.2),1):
        for k in np.around(np.arange(0.1,1,0.2),1):           
            y1,y2,y3=ED.evogame(a1=i,a2=j,a3=k)
            lines=[y1,y2,y3]        
            box.append(lines)    
data=np.array(box)
np.save("data.npy", data)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# c颜色，marker：样式*雪花
ax.set_zlim(0,1)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
#ax.set_xlabel("x",size = 10)
ax.tick_params( tickdir='in',labelsize=8)

for i in range(data.shape[0]):
    ax.plot(xs=data[i][0],ys=data[i][1],zs=data[i][2],linewidth=0.5)
plt.show()