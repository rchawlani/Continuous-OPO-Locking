# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 10:58:36 2022

@author: Administrator
"""

import pyvisa
import numpy
import time
import matplotlib.pyplot as plt
import scipy
from scipy.signal import find_peaks


OSC_ADDR = 'TCPIP0::131.215.138.209::INSTR'



class locking_driver:
    
    osc = None
    locked = 0
    
    def __init__(self):
        
        rm = pyvisa.ResourceManager()
        #while(1):
            #try:
        self.osc = rm.open_resource(OSC_ADDR)
            #    break
            #except:
                #print("Trying to open osc again")
        print(self.osc.query("*IDN?"))
        
        return
    
    def read_channel(self, cn):
        if (self.locked):
            return
        self.locked = 1
        self.osc.write(":WAV:SOUR CHAN" + str(int(cn)))
        self.osc.write(":WAV:MODE NORM")
        self.osc.write(":WAV:FORM ASC")
        
        while(1):
            try:
                rawdata = self.osc.query(":WAV:DATA?")
            
                rdl = rawdata.split(',')
                
                yvals = []
                for i in range(1, len(rdl)):
                    yvals.append(float(rdl[i]))
                
                
                timescale = float(self.osc.query(":TIM:SCAL?"))
                
                t_tot = 12*timescale
                
                t_vals = numpy.linspace(0,t_tot,len(yvals))
                self.locked = 0
                return t_vals, yvals
            except:
                print("IO error, trying again")
                continue
    
    #Returns the value of the highest peak
    #in units of 8ns since ramp bottom
    def read_dc_val(self):
        #self.osc.write(':CHAN2:COUP DC')
        #self.osc.write(':SING')
        time.sleep(.5)
        self.osc.write(':RUN')
        time.sleep(.5)
        #self.osc.write(':FORCetrig')
        #self.osc.write(':FORCetrig')
        time.sleep(.5)
        xval, yval = self.read_channel(2)
        #self.osc.write(':CHAN2:COUP AC')
        return xval, yval

    def get_locking_pos(self, plot = 0):
        
        #Trigger the oscilliscope
        self.osc.write(":SING")
        #time.sleep(1)
        rt = self.osc.query(":TRIG:STAT?")
        #print(rt)
        ntries = 0
        while(rt != "STOP\n"):
            time.sleep(0.1)
            rt = self.osc.query(":TRIG:STAT?")
            #print(rt)
            ntries += 1
            if(ntries > 10):
                self.osc.write(":STOP")
                self.osc.write(":RUN")
                return 0,0,0
        #time.sleep(1)
        
        ramp_t, ramp_v = self.read_channel(3)
        
        sig_t, sig_v = self.read_channel(2)
        #print('sig_t: ',str(sig_t))
        self.osc.write(":RUN")
        r_min = numpy.where(ramp_v == numpy.min(ramp_v))
        r_min = r_min[0][0]
        return ramp_t, sig_v, r_min
        '''#Determine the position of the bottom of the ramp
        r_min = numpy.where(ramp_v == numpy.min(ramp_v))
        r_min = r_min[0][0]
        
        #Starting from this position, search the voltage array to find the maximum voltage
        
        s_i = r_min
        sig_max = 0
        sig_pos = 0
        while(s_i < len(sig_v)):
            if(sig_v[s_i] > sig_max):
                sig_max = sig_v[s_i]
                sig_pos = s_i
            s_i += 1
        
        lock_delay = sig_t[sig_pos] - ramp_t[r_min] - 1.5e-3

        #Convert to 8ns bins
        lock_val = int(lock_delay * (1e9/8))
        
        
        if(plot):
            fig, ax1 = plt.subplots()
            ax1.plot(ramp_t, ramp_v, color='red', label = '1')
            ax2 = ax1.twinx()
            ax2.plot(sig_t, sig_v, color='blue', label = '2')
            ax2.plot([sig_t[sig_pos]], [sig_v[sig_pos]], '-o', color='green')
            fig.tight_layout()
            plt.show()
        print("Locking offset was " + str(lock_delay) + " seconds, lock val was " + str(lock_val))
            
        return lock_val, sig_max'''
    
    
    def return_peaks(self, height):
        tvals, yvals, r_min = self.get_locking_pos()
        #print('yvals: ',str(yvals))
        peaks, _ = find_peaks(yvals, height)
        xpeak_arr = []
        ypeak_arr = []
        for i in peaks:
            xpeak_arr.append(tvals[i])
            ypeak_arr.append(yvals[i])
        
        return xpeak_arr, ypeak_arr
    
    def find_max_peaks(self, height, ramp_min):
        xpeaks, ypeaks = self.return_peaks(height)
        for i in range(0, len(xpeaks)-1):
            if (xpeaks[0]<ramp_min):
                xpeaks.pop(0)
                ypeaks.pop(0)
        max_index = numpy.argmax(ypeaks)
        '''if xpeaks[max_index] < ramp_min:
            # This means we'll get a negative number
            ypeaks.pop(max_index)
            max_index = numpy.argmax(ypeaks)'''
        
        print('xpeaks, ypeaks: ',str(xpeaks), str(ypeaks))
        return xpeaks[max_index], ypeaks[max_index]
    def find_min(self, height):
        tvals, yvals = self.return_peaks(height)
        min_index = numpy.argmin(yvals)
        return tvals[min_index], yvals[min_index]
        
            

        
                