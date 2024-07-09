# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:14:57 2024

@author: JkSun
"""


import Evo_net_draw as ED
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import time



box=[]
for i in [0.3,0.35,0.4,0.45,0.5]:    
    y1,y2,y3=ED.evogame(pg=i)
    lines=[y1,y2,y3]
    box.append(lines)
data3=np.array(box)
np.save("data3.npy", data3)



c_string = ['#FD6D5A', '#FEB40B', '#6DC354', '#994487', '#518CD8', '#443295']
fig=plt.figure(1,figsize=(6,6))
#plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, hspace=0.4, wspace=0.3)
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(box[0][0],color=c_string[0],linestyle="-",linewidth=1)
ax1.plot(box[1][0],color=c_string[1],linestyle="-",linewidth=1)
ax1.plot(box[2][0],color=c_string[2],linestyle="-",linewidth=1)
ax1.plot(box[3][0],color=c_string[3],linestyle="-",linewidth=1)
ax1.plot(box[4][0],color=c_string[4],linestyle="-",linewidth=1)
ax1.set_xlabel("Time")
ax1.set_ylabel("Proportion")
ax1.legend(['REG,Pg=0.3','REG,Pg=0.35','REG,Pg=0.4','REG,Pg=0.45','REG,Pg=0.5'],fontsize=8)

ax2=fig.add_subplot(2, 2, 2)
ax2.plot(box[0][1],color=c_string[0],linestyle="-",linewidth=1)
ax2.plot(box[1][1],color=c_string[1],linestyle="-",linewidth=1)
ax2.plot(box[2][1],color=c_string[2],linestyle="-",linewidth=1)
ax2.plot(box[3][1],color=c_string[3],linestyle="-",linewidth=1)
ax2.plot(box[4][1],color=c_string[4],linestyle="-",linewidth=1)
ax2.set_xlabel("Time")
ax2.set_ylabel("Proportion")
ax2.legend(['HM,Pg=0.3','HM,Pg=0.35','HM,Pg=0.4','HM,Pg=0.45','HM,Pg=0.5'],fontsize=8)

ax3=fig.add_subplot(2, 2, 3)
ax3.plot(box[0][2],color=c_string[0],linestyle="-",linewidth=1)
ax3.plot(box[1][2],color=c_string[1],linestyle="-",linewidth=1)
ax3.plot(box[2][0],color=c_string[2],linestyle="-",linewidth=1)
ax3.plot(box[3][2],color=c_string[3],linestyle="-",linewidth=1)
ax3.plot(box[4][2],color=c_string[4],linestyle="-",linewidth=1)
ax3.set_xlabel("Time")
ax3.set_ylabel("Proportion")
ax3.legend(['HU,Pg=0.3','HU,Pg=0.35','HU,Pg=0.4','HU,Pg=0.45','HU,Pg=0.5'],fontsize=8)

ax4=fig.add_subplot(2, 2, 4,projection='3d')
ax4.set_zlim(0,1)
ax4.set_xlim(0,1)
ax4.set_ylim(0,1)
#ax.set_xlabel("x",size = 10)
ax4.tick_params( tickdir='in',labelsize=8)
ax4.plot(xs=box[0][0],ys=box[0][1],zs=box[0][2],color=c_string[0],linewidth=1.5,label='Pg=0.3')
ax4.plot(xs=box[1][0],ys=box[1][1],zs=box[1][2],color=c_string[1],linewidth=1.5,label='Pg=0.35')
ax4.plot(xs=box[2][0],ys=box[2][1],zs=box[2][2],color=c_string[2],linewidth=1.5,label='Pg=0.4')
ax4.plot(xs=box[3][0],ys=box[3][1],zs=box[3][2],color=c_string[3],linewidth=1.5,label='Pg=0.45')
ax4.plot(xs=box[4][0],ys=box[4][1],zs=box[4][2],color=c_string[4],linewidth=1.5,label='Pg=0.5')
ax4.legend(loc="upper left",fontsize=8)

fig.subplots_adjust(bottom=0.15, wspace=0.4, hspace=0.4)  
  
# 在每个子图的下方添加小标题  
fig.text(0.5, -0.3, '(a)Effect on REG', fontsize=10, ha='center', transform=ax1.transAxes)  
fig.text(0.5, -0.3, '(b)Effect on HM', fontsize=10, ha='center', transform=ax2.transAxes)  
fig.text(0.5, -0.3, '(c)Effect on HU', fontsize=10, ha='center', transform=ax3.transAxes)  
fig.text(0.5, -0.3, '(d)Evolutionary equilibrium result', fontsize=10, ha='center', transform=ax4.transAxes)


plt.show()





















