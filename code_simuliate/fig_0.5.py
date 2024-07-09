# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 23:48:46 2024

@author: JkSun
"""
import Evo_net_draw as ED
import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import time

  
box=[]
y1,y2,y3=ED.evogame(a1=0.5,a2=0.5,a3=0.5)
lines=[y1,y2,y3]
box.append(lines)
plt.figure(1)
plt.plot(box[0][0],color="r",linestyle="-",linewidth=1)
plt.plot(box[0][1],color="g",linestyle="-",linewidth=1)
plt.plot(box[0][2],color="b",linestyle="-",linewidth=1)
plt.xlabel("Time")
plt.ylabel("Proportion")
plt.legend(['REG','HM','HU'],fontsize=8)

