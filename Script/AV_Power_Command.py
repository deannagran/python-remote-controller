import socket   #for sockets
import sys  #for exit
import requests #for http requests on RPS nodes
import telnetlib #for more RPS node requests
import time #stops for no one
from tkinter import *
from threading import Thread
import functools #for error handling

#Encoded strings to be sent to the Crestron processors 
offenc = 'off'.encode()
onenc = 'on'.encode()

#Create a notification popup window
def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Warrington AV Power Command Notification")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()

#Prevent program from freezing when not on the correct AV LAN network
def timeout(seconds_before_timeout):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, seconds_before_timeout))]
            def newFunc():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=newFunc)
            t.daemon = True
            try:
                t.start()
                t.join(seconds_before_timeout)
            except Exception as e:
                print('error starting thread')
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

#Check current power statuses of Matherly's remote power switches via Telnet commands
def getPowerStatus(HOST):
    tn = telnetlib.Telnet(HOST)

    tn.read_until("Please input username and password!".encode('utf-8'))
    tn.write("admin:EHFP2020\r\n".encode('utf-8'))
    tn.write("getpower\r\n".encode('utf-8'))
    tn.write("exit\r\n".encode('utf-8'))

    log = (tn.read_all()) 
    status = log.find(b':')
    if log[status+2] == 48:
        print(HOST + " is turned off.")
        return 0
    else:
        print(HOST + " is turned on.")
        return 1

#Determine whether or not user's computer is connected to AV LAN/able to access MAT120 RPS Nodes
def verifyConnection():
    r = requests.get("http://10.247.76.221/set.cmd?cmd=getpower", auth=('admin', 'EHFP2020'))
    if (r.status_code == requests.codes.ok):
        print("connected")
    else:
        print("error")

try:
    func = timeout(2)(verifyConnection)
    func()
    connected = True
except:
    popupmsg('WARNING: You are unable to connect to one or all of the Matherly devices. Please confirm you are on the correct network and restart the program.')
    connected = False

#Create GUI labels
window = Tk()
window.title("Warrington AV Power Command")
window.geometry('490x400')
lbl = Label(window, text="Hough 140") #10.247.39.16
lbl.grid(column=0, row=0)
lbl1 = Label(window, text="Hough 150") #10.247.39.238 (REMOTE POWER SWITCH, NOT CRESTRON)
lbl1.grid(column=0, row=1)
lbl2 = Label(window, text="Hough 240") #10.247.39.28
lbl2.grid(column=0, row=2)
lbl3 = Label(window, text="Hough 250") #10.247.39.31
lbl3.grid(column=0, row=3)
lbl4 = Label(window, text="Hough 340") #10.247.39.34
lbl4.grid(column=0, row=4)

lbl5 = Label(window, text="Matherly 120 Team 1") #10.247.76.221
lbl5.grid(column=0, row=5)
lbl6 = Label(window, text="Matherly 120 Team 2") #10.247.76.222
lbl6.grid(column=0, row=6)
lbl7 = Label(window, text="Matherly 120 Team 3") #10.247.76.223
lbl7.grid(column=0, row=7)
lbl8 = Label(window, text="Matherly 120 Team 4") #10.247.76.224
lbl8.grid(column=0, row=8)
lbl9 = Label(window, text="Matherly 120 Team 5") #10.247.76.225
lbl9.grid(column=0, row=9)
lbl10 = Label(window, text="Matherly 120 Team 6") #10.247.76.226
lbl10.grid(column=0, row=10)
lbl11 = Label(window, text="Matherly 120 Team 7") #10.247.76.227
lbl11.grid(column=0, row=11)
lbl12 = Label(window, text="Matherly 120 Instructor PC") #10.247.76.228
lbl12.grid(column=0, row=12)

lbl1201 = Label(window, text=" ") #10.247.76.221
lbl1201.grid(column=3, row=5)
lbl1202 = Label(window, text=" ") #10.247.76.222
lbl1202.grid(column=3, row=6)
lbl1203 = Label(window, text=" ") #10.247.76.223
lbl1203.grid(column=3, row=7)
lbl1204 = Label(window, text=" ") #10.247.76.224
lbl1204.grid(column=3, row=8)
lbl1205 = Label(window, text=" ") #10.247.76.225
lbl1205.grid(column=3, row=9)
lbl1206 = Label(window, text=" ") #10.247.76.226
lbl1206.grid(column=3, row=10)
lbl1207 = Label(window, text=" ") #10.247.76.227
lbl1207.grid(column=3, row=11)
lbl1208 = Label(window, text=" ") #10.247.76.228
lbl1208.grid(column=3, row=12)
lblH150 = Label(window, text=" ") #10.247.39.238
lblH150.grid(column=3, row=1)

#Attempt to connect to desired Crestron processor and send encoded string
def openSocket(host, on):
    try:
        #Create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        sys.exit()

    print ('Socket Created')
    port = 1205 #This is the port specified in SIMPL programs TCP/IP Server symbol
    
    #Try to get hostname
    try:
        remote_ip = socket.gethostbyname( host )
    except:
        #Could not resolve
        print ('Hostname could not be resolved. ')
        sys.exit()

    #Connect to remote server
    try:
        s.connect((remote_ip , port))
    except:
        #Could not connect
        print ('Failed to connect. ')
        return False

    print ('Socket Connected to ' + host + ' on ip ' + remote_ip)
    #Send on/off strings
    if on:
        s.send(onenc)
        s.close()
    else:
        s.send(offenc)
        s.close()

    return True

#Turn Crestron processor on
def clickedOn(host):
    on = True
    if openSocket(host, on):
        print('Device turned on.')

#Turn Crestron processor off
def clickedOff(host):
    on = False
    if openSocket(host, on):
        print('Device turned off.')

#Turn RPS Node on
def clickedOnSwitch(host):
    if connected:
        try:
            requests.get("http://admin:EHFP2020@" + host + "/set.cmd?cmd=setpower+p61=1", auth=('admin', 'EHFP2020'))
        except:
            print("Couldn't connect")
    else:
        popupmsg('You are not connected to the same network as the Matherly devices. Please check your network settings and restart the program.')

#Turn RPS Node off
def clickedOffSwitch(host):
    if connected:
        try:
            requests.get("http://admin:EHFP2020@" + host + "/set.cmd?cmd=setpower+p61=0", auth=('admin', 'EHFP2020'))
        except:
            print("Couldn't connect")
    else:
        popupmsg('You are not connected to the same network as the Matherly devices. Please check your network settings and restart the program.')


def checkPowerStatus():
    if connected:
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.221")
            if getpwr == 1:
                lbl1201.config(text="1")
            else:
                lbl1201.config(text="0")
        except Exception as e:
            print(e)
            lbl1201.config(text="CANNOT CONNECT")
 
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.222")
            if getpwr == 1:
                lbl1202.config(text="1")
            else:
                lbl1202.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1202.config(text="CANNOT CONNECT")
        
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.223")
            if getpwr == 1:
                lbl1203.config(text="1")
            else:
                lbl1203.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1203.config(text="CANNOT CONNECT")
        
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.224")
            if getpwr == 1:
                lbl1204.config(text="1")
            else:
                lbl1204.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1204.config(text="CANNOT CONNECT")
         
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.225")
            if getpwr == 1:
                lbl1205.config(text="1")
            else:
                lbl1205.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1205.config(text="CANNOT CONNECT")

        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.226")    
            if getpwr == 1:
                lbl1206.config(text="1")
            else:
                lbl1206.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1206.config(text="CANNOT CONNECT")
         
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.227")
            if getpwr == 1:
                lbl1207.config(text="1")
            else:
                lbl1207.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1207.config(text="CANNOT CONNECT")
        
        try:
            getpwr = timeout(3)(getPowerStatus)("10.247.76.228")
            if getpwr == 1:
                lbl1208.config(text="1")
            else:
                lbl1208.config(text="0")
        except:
            print("Timeout -- can't connect")
            lbl1208.config(text="CANNOT CONNECT")
        
        try:
            getpwr = timeout(2)(getPowerStatus)("10.247.39.238")
            if getpwr == 1:
                lblH150.config(text="1")
            else:
                lblH150.config(text="0")
        except:
            print("Timeout -- can't connect")
            lblH150.config(text="CANNOT CONNECT")

    else:
        popupmsg('You are not connected to the same network as the Matherly or Hough devices. Please check your network settings and restart the program.')

    

#Creat GUI buttons
btn = Button(window, text="ON", command= lambda: clickedOn('10.247.39.16'))
btn.grid(column=1, row=0)

btn2 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.16'))
btn2.grid(column=2, row=0)

btn1 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.39.23'))
btn1.grid(column=1, row=1)

btnx = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.39.23'))
btnx.grid(column=2, row=1)

btn3 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.28'))
btn3.grid(column=1, row=2)

btn4 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.28'))
btn4.grid(column=2, row=2)

btn5 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.31'))
btn5.grid(column=1, row=3)

btn6 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.31'))
btn6.grid(column=2, row=3)

btn7 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.34'))
btn7.grid(column=1, row=4)

btn8 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.34'))
btn8.grid(column=2, row=4)

btn9 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.221'))
btn9.grid(column=1, row=5)

btn10 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.221'))
btn10.grid(column=2, row=5)

btn11 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.222'))
btn11.grid(column=1, row=6)

btn12 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.222'))
btn12.grid(column=2, row=6)

btn13 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.223'))
btn13.grid(column=1, row=7)

btn14 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.223'))
btn14.grid(column=2, row=7)

btn15 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.224'))
btn15.grid(column=1, row=8)

btn16 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.224'))
btn16.grid(column=2, row=8)

btn17 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.225'))
btn17.grid(column=1, row=9)

btn18 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.225'))
btn18.grid(column=2, row=9)

btn19 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.226'))
btn19.grid(column=1, row=10)

btn20 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.226'))
btn20.grid(column=2, row=10)

btn21 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.227'))
btn21.grid(column=1, row=11)

btn22 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.227'))
btn22.grid(column=2, row=11)

btn23 = Button(window, text="ON", command= lambda: clickedOnSwitch('10.247.76.228'))
btn23.grid(column=1, row=12)

btn24 = Button(window, text="OFF", command= lambda: clickedOffSwitch('10.247.76.228'))
btn24.grid(column=2, row=12)

btn25 = Button(window, text="UPDATE POWER STATUSES", command= checkPowerStatus)
btn25.grid(column=1, row=13)



window.mainloop()

print('Exiting')