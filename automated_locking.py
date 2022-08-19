# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 14:04:49 2022

@author: Rahul Chawlani, James Williams, @ Caltech
"""
import time

import locking_driver
# Using Chrome to access web

import numpy as np
from tkinter import *
from numpy import *
import matplotlib
from random import randint
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
#from matplotlib.text import Text

import requests
from PIL import ImageTk, Image
import threading

# Create new device instance
device = locking_driver.locking_driver()
# Below, define the url to which send post commands to
url = 'http://131.215.138.174/data'
# Define Global Variables for use
P = 200
I=200
D=0
Phase=50
trigx = 0
trigy = 0
peak1x = 0
peak1y = 0
peak2x = 0
peak2y = 0
peak3x = 0
peak3y = 0
peak4x = 0
peak4y = 0
peak5x = 0
peak5y = 0
boo1 = 1
is_ramped = 0
peak_cutoff = 1.20

def send_data(time_trig, ramp, trig_lock):
    # General purpose post command template, we send the what value to trigger at,
    # and whether to click ramp or trig lock.
    global P, I, D, Phase
    #print('P: '+ str(P)+ ',I: '+str(I)+', D: '+str(D)+' ,Phase: '+str(Phase))
    config ={"datasets":{"params":{"xmin":177.90757515643915,"xmax":181.3137290963873,"trig_mode":1,"trig_source":2,"trig_edge":0,"trig_delay":0.100221,"trig_level":0,"time_range":3,"time_units":1,"en_avg_at_dec":0,"min_y":0,"max_y":0,"prb_att_ch1":0,"gain_ch1":1,"prb_att_ch2":0,"gain_ch2":0,"gui_xmin":100.226105,"gui_xmax":120.226105,"lock_oscA_sw":1,"lock_oscB_sw":5,"lock_osc1_filt_off":1,"lock_osc2_filt_off":1,"lock_osc_raw_mode":0,"lock_osc_lockin_mode":0,"lock_trig_sw":2,"lock_out1_sw":4,"lock_out2_sw":13,"lock_slow_out1_sw":0,"lock_slow_out2_sw":0,"lock_slow_out3_sw":0,"lock_slow_out4_sw":0,"lock_lock_trig_val":1980,"lock_lock_trig_time_val":time_trig,"lock_lock_trig_sw":0,"lock_rl_error_threshold":0,"lock_rl_signal_sw":0,"lock_rl_signal_threshold":0,"lock_rl_error_enable":0,"lock_rl_signal_enable":0,"lock_rl_reset":0,"lock_sf_jumpA":0,"lock_sf_jumpB":0,"lock_sf_start":0,"lock_sf_AfrzO":0,"lock_sf_AfrzI":0,"lock_sf_BfrzO":0,"lock_sf_BfrzI":0,"lock_signal_sw":0,"lock_sg_amp1":0,"lock_sg_amp2":0,"lock_sg_amp3":0,"lock_sg_amp_sq":0,"lock_lpf_F1_tau":5,"lock_lpf_F1_order":1,"lock_lpf_F2_tau":0,"lock_lpf_F2_order":2,"lock_lpf_F3_tau":0,"lock_lpf_F3_order":2,"lock_lpf_sq_tau":0,"lock_lpf_sq_order":2,"lock_error_sw":3,"lock_error_offset":0,"lock_gen_mod_phase":Phase,"lock_gen_mod_phase_sq":0,"lock_gen_mod_hp":49,"lock_gen_mod_sqp":0,"lock_ramp_step":2000,"lock_ramp_low_lim":-8032,"lock_ramp_hig_lim":7000,"lock_ramp_reset":0,"lock_ramp_enable":ramp,"lock_ramp_direction":0,"lock_ramp_B_factor":4096,"lock_read_ctrl":0,"lock_pidA_sw":0,"lock_pidA_PSR":3,"lock_pidA_ISR":8,"lock_pidA_DSR":0,"lock_pidA_SAT":13,"lock_pidA_sp":0,"lock_pidA_kp":0,"lock_pidA_ki":0,"lock_pidA_kd":0,"lock_pidA_irst":0,"lock_pidA_freeze":0,"lock_pidA_ifreeze":0,"lock_pidB_sw":0,"lock_pidB_PSR":3,"lock_pidB_ISR":8,"lock_pidB_DSR":0,"lock_pidB_SAT":13,"lock_pidB_sp":0,"lock_pidB_kp":P,"lock_pidB_ki":I,"lock_pidB_kd":D,"lock_pidB_irst":0,"lock_pidB_freeze":0,"lock_pidB_ifreeze":0,"lock_aux_A":0,"lock_aux_B":0,"lock_ctrl_aux_lock_now":0,"lock_ctrl_aux_launch_lock_trig":trig_lock,"lock_ctrl_aux_pidB_enable_ctrl":0,"lock_ctrl_aux_pidA_enable_ctrl":0,"lock_ctrl_aux_ramp_enable_ctrl":1,"lock_ctrl_aux_set_pidB_enable":1,"lock_ctrl_aux_set_pidA_enable":0,"lock_ctrl_aux_set_ramp_enable":0,"lock_ctrl_aux_trig_type":1,"lock_ctrl_aux_lock_trig_rise":1,"lock_mod_sq_on":0,"lock_mod_harmonic_on":1,"meas_min_ch1":-2.758877,"meas_max_ch1":-2.461094,"meas_amp_ch1":0.297784,"meas_avg_ch1":-2.606576,"meas_freq_ch1":0,"meas_per_ch1":0,"meas_min_ch2":-1.743041,"meas_max_ch2":-1.482329,"meas_amp_ch2":0.260711,"meas_avg_ch2":-1.608514,"meas_freq_ch2":0,"meas_per_ch2":0,"single_btn":0}}}
    #print(config.get("lock_lock_trig_time_val"))
    session = requests.session()
    y = requests.post(url, json = config)
    #x = requests.post(url, json=myobj)
    

def is_float(s, name):
    # Simple checker
    try:
        float(s)
        return True
    except ValueError:
        messagebox.showwarning("showwarning", "Please Enter a Valid Number\nProblem with "+name)
        return False
def start_locking(xdata, ydata):
    # Get Oscilliscope Data
    #y_vals = ydata # Should be oscilloscope data
    global trigx, trigy
    
    xpeaks = []
    xlen = len(xdata)
    
    if 1:  # picking with a custom hit test function
    # you can define custom pickers by setting picker to a callable
    # function.  The function has the signature
    #
    #  hit, props = func(artist, mouseevent)
    #
    # to determine the hit test.  if the mouse event is over the artist,
    # return hit=True and props is a dictionary of
    # properties you want added to the PickEvent attributes

        def line_picker(line, mouseevent):
            """
            find the points within a certain distance from the mouseclick in
            data coords and attach some extra attributes, pickx and picky
            which are the data points that were picked
            """
            global trigx, trigy
            if mouseevent.xdata is None:
                return False, dict()
            xdata = line.get_xdata() #THIS IS OUR CSV DATA
            ydata = line.get_ydata()
            print('click successful')
            maxd = 0.01 #Radius for how far away to click.
            d = sqrt((xdata - mouseevent.xdata)**2. + (ydata - mouseevent.ydata)**2.)
            
            ind = nonzero(less_equal(d, maxd))
            if len(ind):
                pickx = take(xdata, ind)
                picky = take(ydata, ind)
                trig1x = pickx[0]
                trig1y = picky[0]
                trigx = trig1x[0]
                trigy = trig1y[0]
                props = dict(ind=ind, pickx=pickx, picky=picky)
                
                messagebox.showinfo("showinfo", "Successfully Locked")
                    
                return True, props
                
            else:
                return False, dict()

    def onpick2(event):
        print('onpick2 line:', event.pickx, event.picky) #When doing this irl, make sure to see if an int is checked. Otherwise, do not do anything and ask user to click again.
    def coolpick(event):
        if len(event.pickx[0]) >0 :
            return 1
    fig, ax = plt.subplots()
    ax.set_title('Pick your desired peak')
    line, = ax.plot(xdata, ydata, 'o', picker=line_picker)
    fig.canvas.mpl_connect('pick_event', onpick2)
    
def show_five_peaks(device):
    global img1, img2, img3, img4, img5, is_ramped, peak_cutoff
    global peak1x, peak1y, peak2x, peak2y, peak3x, peak3y, peak4x, peak4y, peak5x, peak5y
    plt.ioff()
    plt.cla()
    is_ramped = 1
    send_data(0,1,0)
   
    try:
        xpeaks, ypeaks = device.return_peaks(1.2)
    except:
        messagebox.showinfo("showwarning", "Problem receiving data, please consult user guide or check the status of the laser source.")
        return 
    xdata, ydata, r_min = device.get_locking_pos()
    print(xpeaks)
    ramp_min = xdata[r_min]
    print(ramp_min)
    print(len(xpeaks))
    if len(xpeaks)>5:
            
        for i in range(0, len(xpeaks)-1):
            if (xpeaks[0] < ramp_min):
                idc_about_num= xpeaks.pop(0)
                idc_about_num2 = ypeaks.pop(0)
        messagebox.showinfo("showinfo", "Some Peaks Have Been Cut")
    print(ypeaks)
    print(len(xpeaks))
    try:
        distance = abs((xpeaks[1])-(xpeaks[0]))/2
    except:
        messagebox.showinfo("showwarning", "We have receieved no data, please check laser")

    plt.xlim(xpeaks[0]-distance, xpeaks[0]+distance)
    
    plt.xlabel('time')
    plt.ylabel('Voltage')
    plt.title('Peak 1', fontsize = 20)
    plt.plot(xdata, ydata)   
    plt.savefig('Peak1.jpg')
    plt.cla()
    plt.xlim(xpeaks[1]-distance, xpeaks[1]+distance)
    plt.title('Peak 2', fontsize = 20)
    plt.plot(xdata, ydata)   
    plt.savefig('Peak2.jpg')
    plt.cla()
    plt.xlim(xpeaks[2]-distance, xpeaks[2]+distance)
    plt.title('Peak 3', fontsize = 20)
    plt.plot(xdata, ydata)   
    plt.savefig('Peak3.jpg')
    plt.cla()
    plt.xlim(xpeaks[3]-distance, xpeaks[3]+distance)
    plt.title('Peak 4', fontsize = 20)
    plt.plot(xdata, ydata)   
    plt.savefig('Peak4.jpg')
    plt.cla()
    if len(xpeaks)>4:
        plt.xlim(xpeaks[4]-distance, xpeaks[4]+distance)
        plt.title('Peak 5', fontsize = 20)
        plt.plot(xdata, ydata)   
        plt.savefig('Peak5.jpg')
        peak5x, peak5y = xpeaks[4], xpeaks[4]
    peak1x, peak1y = xpeaks[0], ypeaks[0]
    peak2x, peak2y = xpeaks[1], ypeaks[1]
    peak3x, peak3y = xpeaks[2], ypeaks[2]
    peak4x, peak4y = xpeaks[3], ypeaks[3]
    
    
    #time.sleep(2)
    frame1 = Frame(ws, width=100, height=66)
    frame1.pack()
    frame1.place(anchor='center', relx=.1, rely=0.75)
    img1 = ImageTk.PhotoImage(Image.open("Peak1.jpg"))

# Create a Label Widget to display the text or Image
    label1 = Label(frame1, image = img1)
    label1.pack()
    
    frame2 = Frame(ws, width=100, height=66)
    frame2.pack()
    frame2.place(anchor='center', relx=.3, rely=0.75)
    img2 = ImageTk.PhotoImage(Image.open("Peak2.jpg"))

# Create a Label Widget to display the text or Image
    label2 = Label(frame2, image = img2)
    label2.pack()
    
    frame3 = Frame(ws, width=100, height=66)
    frame3.pack()
    frame3.place(anchor='center', relx=.5, rely=0.75)
    img3 = ImageTk.PhotoImage(Image.open("Peak3.jpg"))

# Create a Label Widget to display the text or Image
    label3 = Label(frame3, image = img3)
    label3.pack()
    
    frame4 = Frame(ws, width=100, height=66)
    frame4.pack()
    frame4.place(anchor='center', relx=.7, rely=0.75)
    img4 = ImageTk.PhotoImage(Image.open("Peak4.jpg"))

# Create a Label Widget to display the text or Image
    label4 = Label(frame4, image = img4)
    label4.pack()
    
    button7 = Button(ws, text="Choose Peak 1", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=custom_lock, args = [device, peak1x, peak1y]).start())
    button7.place(relx = .1, rely = .55, anchor = CENTER)

    button8 = Button(ws, text="Choose Peak 2", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=custom_lock, args = [device, peak2x, peak2y]).start())
    button8.place(relx = .3, rely = .55, anchor = CENTER)
    button9 = Button(ws, text="Choose Peak 3", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=custom_lock, args = [device, peak3x, peak3y]).start())
    button9.place(relx = .5, rely = .55, anchor = CENTER)
    button10 = Button(ws, text="Choose Peak 4", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=custom_lock, args = [device, peak4x, peak4y]).start())
    button10.place(relx = .7, rely = .55, anchor = CENTER)
    if len(xpeaks)>4:
        frame5 = Frame(ws, width=100, height=66)
        frame5.pack()
        frame5.place(anchor='center', relx=.9, rely=0.75)
        img5 = ImageTk.PhotoImage(Image.open("Peak5.jpg"))

# Create a Label Widget to display the text or Image
        label5 = Label(frame5, image = img5)
        label5.pack()
        button11 = Button(ws, text="Choose Peak 5", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=custom_lock, args = [device, peak5x, peak5y]).start())
        button11.place(relx = .9, rely = .55, anchor = CENTER)
    
    

def custom_lock(device, current_val, peak_y_val):
    datax, datay, r_min = device.get_locking_pos()
    
    ramp_min = datax[r_min]
    ramp_min/=8E-9
    new_val = current_val
    current_val /= 8E-9
    current_val -= 1.5E-3/8E-9
    current_val -=ramp_min
    print('Ramp_min:'+str(ramp_min))
    print('Current_val: '+str(current_val))
    send_data(current_val, 1,0)
    send_data(current_val, 1, 1)
    is_ramped = 0
    messagebox.showinfo("showinfo", "Successfully Locked with a Peak Voltage of "+str(peak_y_val))
    time.sleep(1)
    dc_vals['text'] = 'Locked at: time = '+str(new_val)+' and voltage of: '+str(peak_y_val)

    #write_to_csv()
    time.sleep(4)
    while(boo1):
        datax, datay = device.read_channel(2)
        time.sleep(1)
        if (np.mean(datay)< (peak_y_val * .925)):
            print('mean of datay:'+str(np.mean(datay)))
            check_pos(1, current_val, device)


def Success(device):
    global boo1, is_ramped, peak_cutoff
    
    is_ramped = 1
    send_data(0, 1,0)
    
    datax, datay, r_min = device.get_locking_pos()
    ramp_min = datax[r_min]

    

    try:
        current_val, peak_y_val = device.find_max_peaks(1.2, ramp_min)
    except:
        messagebox.showinfo("showwarning", "We have receieved no data, please check laser or consult user guide")
        send_data(0,0,0)
        return
    
    print('Current_val: '+str(current_val))
    ramp_min = datax[r_min]
    print('Ramp_min:'+str(ramp_min))
    ramp_min/=8E-9
    new_val = current_val
    current_val /= 8E-9
    current_val -= 1.5E-3/8E-9
    current_val -=ramp_min
    print('Ramp_min:'+str(ramp_min))
    print('Current_val: '+str(current_val))
    print('peak_y_val: '+str(peak_y_val))
    send_data(current_val, 1,0)
    send_data(current_val, 1, 1)
    is_ramped = 0
    dc_vals['text'] = 'Locked at: time = '+str(new_val)+' and voltage of: '+str(peak_y_val)
    time.sleep(5)
    

    while(boo1):
        try:
            datax, datay = device.read_channel(2)
        except:
            messagebox.showinfo("showwarning", "We have received no data, check laser or consult user guide")       
            send_data(0,0,0)
            break
        time.sleep(1)
        if (len(datay) < 1):
            messagebox.showinfo("showwarning", "We have received no data, check laser or consult user guide")       
            send_data(0,0,0)
            break
        if (np.mean(datay)< (peak_y_val * .925)):
            print('mean of datay:'+str(np.mean(datay)))
            check_pos(0, 0, device)


def check_pos(boo, for_choose_lock, device):
    is_ramped = 1
    send_data(0, 1, 0)
    try:
        datax, datay, r_min = device.get_locking_pos()
    except:
        messagebox.showinfo("showwarning", "We have received no data, check laser or consult user guide")
        return
    if (boo == 0):
        ramp_min = datax[r_min]
        current_val, peak_y_val = device.find_max_peaks(1.2, ramp_min)
        new_val = current_val
        ramp_min = datax[r_min]
        ramp_min/=8E-9
        current_val /= 8E-9
        current_val -= 1.5E-3/8E-9
        current_val -=ramp_min
    elif (boo == 1):
        current_val = for_choose_lock
        new_val = current_val
    send_data(current_val, 1,0)
    send_data(current_val, 1, 1)
    is_ramped = 0
    dc_vals['text'] = 'Locked at: time = '+str(new_val)+' and voltage of: '+str(peak_y_val)
    time.sleep(5)
    
    


def close_window():
    
    ws.withdraw()
def stop():
    global boo1, is_ramped
    send_data(0, 0, 0)
    is_ramped = 0
    boo1 = 0
    messagebox.showinfo("showinfo", "Quit Locking")
    ws.destroy()
###############################################################################
def apply_data(my_text_boxP, my_text_boxI, my_text_boxD, my_text_boxPhase):
   global P, I, D, Phase
   valP=my_text_boxP.get("1.0","end-1c")
   valI=my_text_boxI.get("1.0","end-1c")
   valD=my_text_boxD.get("1.0","end-1c")
   valPhase=my_text_boxPhase.get("1.0","end-1c")
   if (is_float(valP, "P") & is_float(valD, "I") & is_float(valI, "D") & is_float(valPhase, "Phase")):
       P = float(valP)
       I = float(valI)
       D = float(valD)
       Phase = float(valPhase)
       
       messagebox.showinfo("showinfo", "Changes Applied Successfully!")


def stop_locking():
    global boo1, is_ramped
    boo1 = 0
    send_data(0, 0, 0)
    is_ramped = 0
    messagebox.showinfo("showinfo", "Succcessfully unlocked!")
   
    
    
def New_Window2():
    Window = Toplevel()
    canvas = Canvas(Window, height=100, width=500)
    canvas.pack()
   
    
    my_title= Label(Window, text= "Please Enter your Desired PID Settings Below.", font=('Helvetica bold', 16))
    my_title.pack(side = TOP)
  
    
    my_p = Label(Window, text= "Please Enter your Desired P Value:", font=('Helvetica bold', 8))
    my_p.pack(pady = 10, anchor="w")
    
    my_i = Label(Window, text= "Please Enter your Desired I Value:", font=('Helvetica bold', 8))
    my_i.pack(pady = 10, anchor="w")
    
    my_d = Label(Window, text= "Please Enter your Desired D Value:", font=('Helvetica bold', 8))
    my_d.pack(pady = 10, anchor="w")
    
    my_phase = Label(Window, text= "Please Enter your Desired Lock In Phase Value:", font=('Helvetica bold', 8))
    my_phase.pack(pady = 10, anchor="w")
   
    
    my_text_boxP=Text(Window, height=1, width=20)
    my_text_boxP.place(relx=1, rely=0.425, anchor='e')
    
    my_text_boxI=Text(Window, height=1, width=20)
    my_text_boxI.place(relx=1, rely=0.53, anchor='e')
    
    my_text_boxD=Text(Window, height=1, width=20)
    my_text_boxD.place(relx=1, rely=0.65, anchor='e')
    
    my_text_boxPhase=Text(Window, height = 1, width=20)
    my_text_boxPhase.place(relx=1, rely=0.77, anchor='e')
    
    Button(Window, text = "Apply", bg = "White", fg = "Black", command = lambda: apply_data(my_text_boxP, my_text_boxI, my_text_boxD, my_text_boxPhase)).pack(side = BOTTOM)








#click_ramp()

HEIGHT = 1800 # Declare dimensions of the GUI
WIDTH = 3000
ws = Tk() # Create tkinter GUI object

ws.title("RedPitaya 125-10 Locking")
canvas = Canvas(ws, height=HEIGHT, width=WIDTH)
canvas.pack() # Creates the object to pack so we can actually 'see' the GUI
 # Below, we declare the buttons for the 'main menu'
button1 = Button(ws, text="Lock with Max Peaks", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=Success, args = [device]).start())# Lock with the max peaks, threading included.
button2 = Button(ws, text="PID Settings", bg='White', fg='Black',
                              command=lambda: New_Window2())
button1.place(relx=0.5, rely=.1, anchor=CENTER)
button2.place(relx = 0.1, rely = 0.1, anchor=CENTER)

button4 = Button(ws, text="Quit/Stop Locking", bg='White', fg='Black',
                              command=lambda: stop())
button4.pack(side = BOTTOM)
# Button 5 will be find peaks and show them
button5 = Button(ws, text="Show Peaks", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=show_five_peaks, args = [device]).start())
button5.place(relx = .5, rely=.3, anchor=CENTER)

button6 = Button(ws, text="Stop Locking", bg='White', fg='Black',
                              command=lambda: stop_locking())
button6.place(relx = .85, rely=.3, anchor=CENTER)
# This button below, is used because once we lock onto a peak
button12 = Button(ws, text="Relock User Selected Peaks", bg='White', fg='Black',
                              command=lambda: threading.Thread(target=show_five_peaks, args = [device]).start())
button12.place(relx = .1, rely=.3, anchor=CENTER)

# Create an object of tkinter ImageTk
frame5 = Frame(ws, width=100, height=66)
frame5.pack()
frame5.place(anchor='center', relx=.9, rely=0.1)
img5 = ImageTk.PhotoImage(Image.open("caltech.jpg"))

# Create a Label Widget to display the text or Image
label5 = Label(frame5, image = img5)
label5.pack()

authors = Label(ws, text= "Created by Rahul Chawlani and James Williams @ Caltech", font=('Helvetica bold', 6))
authors.pack()
authors.place(relx = .80, rely = .95)



def update():
    print(is_ramped)
    print(boo1)
    while(boo1):
        if (is_ramped == 0):
            numt, numy = device.read_channel(2)
            num = numy[len(numy)-1]
            dc_vals['text'] = 'Current DC Value: '+str(num)
        else:
            dc_vals['text'] = 'Waiting for Ramp to End'
            break
        time.sleep(.5)
def write_to_csv():
    if (is_ramped == 0):
        numt, numy = device.read_channel(2)
    
    
        f = open("test.csv", "w")
        f.write("time, voltage")
        for i in range(0,len(numt)):
            f.write(str(numt[i]) + "," + str(numy[i]) + "\n")
    

#update()
dc_vals = Label(ws)
dc_vals.pack(side = TOP)
dc_vals['text'] = 'Waiting for Locking'
#threading.Thread(target=update).start()

    
#plt.show()
ws.mainloop()









'''Add a Photo to GUI Code for later:
    
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("forest.jpg"))

# Create a Label Widget to display the text or Image
label = Label(frame, image = img)
label.pack()'''



