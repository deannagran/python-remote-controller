import socket   #for sockets
import sys  #for exit
import requests 
from tkinter import *

offenc = 'off'.encode()
onenc = 'on'.encode()

#Create GUI labels
window = Tk()
window.title("Warrington AV Power Command")
window.geometry('490x400')
lbl = Label(window, text="Hough 140") #10.247.39.16
lbl.grid(column=0, row=0)
lbl1 = Label(window, text="Hough 150") #10.247.39.23
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
hostnameCannotBeResolved = Label(window, text="Hostname could not be resolved.")
failedSocket = Label(window, text="Failed to create socket.")
turnedOffSuccess = Label(window, text="Successfully turned off.")
turnedOnSuccess = Label(window, text="Successfully turned on.")
attemptingConnection = Label(window, text="Attempting to connect...")
failedConnection = Label(window, text="Failed to connect.")


def openSocket(host, on):
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        failedSocket.grid(column=3, row=0)
        sys.exit()

    print ('Socket Created')
    port = 1205 #The port specified in Simpl programs TCP/IP Server symbol
    
    #Try to get hostname
    try:
        remote_ip = socket.gethostbyname( host )
    except:
        #Could not resolve
        print ('Hostname could not be resolved. ')
        attemptingConnection.grid_forget()
        hostnameCannotBeResolved.grid(column=3, row=0)
        sys.exit()

    #Connect to remote server
    try:
        s.connect((remote_ip , port))
    except:
        #Could not connect
        print ('Failed to connect. ')
        attemptingConnection.grid_forget()
        failedConnection.grid(column=3, row=0)
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

def clickedOn(host):
    #Display attempting to connect label
    attemptingConnection.grid(column=3, row=0)
    on = True
    if openSocket(host, on):
        print('Device turned on.')
        attemptingConnection.grid_forget()
        #Display device turned on label
        turnedOnSuccess.grid(column=3, row=0)
        

def clickedOff(host):
    #Display attempting to connect label
    attemptingConnection.grid(column=3, row=0)
    on = False
    if openSocket(host, on):
        print('Device turned off.')
        attemptingConnection.grid_forget()
        #Display device turned off label
        turnedOffSuccess.grid(column=3, row=0)

def clickedOnSwitch(host):
    try:
        requests.get("http://admin:EHFP2020@" + host + "/set.cmd?cmd=setpower+p61=1", auth=('admin', 'EHFP2020'))
    except:
        print("couldn't connect")
        attemptingConnection.grid_forget()
        #Display device turned on label
        failedConnection.grid(column=3, row=0)


def clickedOffSwitch(host):
    try:
        requests.get("http://admin:EHFP2020@" + host + "/set.cmd?cmd=setpower+p61=0", auth=('admin', 'EHFP2020'))
        attemptingConnection.grid_forget()
        #Display device turned on label
        turnedOffSuccess.grid(column=3, row=0)
    except:
        print("couldn't connect")
        attemptingConnection.grid_forget()
        #Display device turned on label
        failedConnection.grid(column=3, row=0)




#buttons
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



window.mainloop()


print('Exiting')