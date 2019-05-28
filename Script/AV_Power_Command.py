import socket   #for sockets
import sys  #for exit
from tkinter import *

offenc = 'off'.encode()
onenc = 'on'.encode()

#Create GUI labels
window = Tk()
window.title("Warrington AV Power Command")
window.geometry('350x200')
lbl = Label(window, text="Hough 140") #10.247.39.16
lbl.grid(column=0, row=0)
lbl2 = Label(window, text="Hough 240") #10.247.39.28
lbl2.grid(column=0, row=1)
lbl3 = Label(window, text="Hough 250") #10.247.39.31
lbl3.grid(column=0, row=2)
lbl4 = Label(window, text="Hough 340") #10.247.39.34
lbl4.grid(column=0, row=3)
lbl5 = Label(window, text="Hostname could not be resolved.")
lbl6 = Label(window, text="Failed to create socket.")
lbl7 = Label(window, text="Successfully turned off.")
lbl8 = Label(window, text="Successfully turned on.")
lbl9 = Label(window, text="Attempting to connect...")
lbl10 = Label(window, text="Failed to connect.")

def openSocket(host, on):
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        lbl6.grid(column=3, row=0)
        sys.exit()

    print ('Socket Created')
    port = 1205 #The port specified in Simpl programs TCP/IP Server symbol
    
    #Try to get hostname
    try:
        remote_ip = socket.gethostbyname( host )
    except:
        #Could not resolve
        print ('Hostname could not be resolved. ')
        lbl9.grid_forget()
        lbl5.grid(column=3, row=0)
        sys.exit()

    #Connect to remote server
    try:
        s.connect((remote_ip , port))
    except:
        #Could not connect
        print ('Failed to connect. ')
        lbl9.grid_forget()
        lbl10.grid(column=3, row=0)
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
    lbl9.grid(column=3, row=0)
    on = True
    if openSocket(host, on):
        print('Device turned on.')
        lbl9.grid_forget()
        #Display device turned on label
        lbl8.grid(column=3, row=0)
        

def clickedOff(host):
    #Display attempting to connect label
    lbl9.grid(column=3, row=0)
    on = False
    if openSocket(host, on):
        print('Device turned off.')
        lbl9.grid_forget()
        #Display device turned off label
        lbl7.grid(column=3, row=0)


#buttons
btn = Button(window, text="ON", command= lambda: clickedOn('10.247.39.16'))
btn.grid(column=1, row=0)
btn2 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.16'))
btn2.grid(column=2, row=0)
btn3 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.28'))
btn3.grid(column=1, row=1)
btn4 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.28'))
btn4.grid(column=2, row=1)
btn5 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.31'))
btn5.grid(column=1, row=2)
btn6 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.31'))
btn6.grid(column=2, row=2)
btn7 = Button(window, text="ON", command= lambda: clickedOn('10.247.39.34'))
btn7.grid(column=1, row=3)
btn8 = Button(window, text="OFF", command= lambda: clickedOff('10.247.39.34'))
btn8.grid(column=2, row=3)


window.mainloop()


print('Exiting')