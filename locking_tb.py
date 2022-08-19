# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 11:29:44 2022

@author: Administrator
"""

import locking_driver
import matplotlib.pyplot as plt

ld = locking_driver.locking_driver()

ramp_t, v, y_min = ld.get_locking_pos(1)
print(ramp_t)

#a, b = ld.read_dc_val()

#time, ramp, sig = ld.get_traces()


#plt.plot(time, ramp)
#plt.plot(time, sig)
