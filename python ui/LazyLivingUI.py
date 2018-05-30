import warnings
import serial
import serial.tools.list_ports
import time
import tkinter as tk
from tkinter import *

def connect_arduino(baudrate=9600): # a more civilized way to connect to arduino
    def is_arduino(p):
        # need more comprehensive test
        # print('cu.wchusbserial14' in p.device)
        return 'cu.wchusbserial14' in p.device

    ports = serial.tools.list_ports.comports()
    arduino_ports = [p for p in ports if is_arduino(p)]

    def port2str(p):
        return "%s - %s (%s)" % (p.device, p.description, p.manufacturer)

    if not arduino_ports:
        portlist = "\n".join([port2str(p) for p in ports])
        raise IOError("No Arduino found\n" + portlist)

    if len(arduino_ports) > 1:
        portlist = "\n".join([port2str(p) for p in ports])
        warnings.warn('Multiple Arduinos found - using the first\n' + portlist)

    selected_port = arduino_ports[0]
    print("Using %s" % port2str(selected_port))
    ser = serial.Serial(selected_port.device, baudrate)
    time.sleep(2)  # this is important it takes time to handshake
    return ser


class Messenger:
    def __init__(self, ser):
        self.ser = ser

    def send_rec(self, msg):
        self.ser.write((msg + "\n").encode())
        return self.ser.read_until(b"\n", 255)#.encode()

    def send_message(self,message):
        print(message)
        self.send_rec(message)

    def get_status(self):
        self.send_rec('status')

class TextBoxUI:

    # def get_entry(self):
    #    return self.e1.get()+ self.e2.get()
    def constructMessage(self):
        return self.ssid.get()+':'+self.password.get()+ ':' + self.host.get()+':'+self.username.get()+ ':' +self.mpass.get()+';'

    def __init__(self,master,hermes):
        self.frame = tk.Frame(master)
        Label(self.frame, text="ssid").grid(row=0)
        Label(self.frame, text="password").grid(row=1)
        Label(self.frame,text="MQTThost").grid(row=2)
        Label(self.frame,text="MQTTUsername").grid(row=3)
        Label(self.frame,text="MQTTPassword").grid(row=4)

        self.ssid = Entry(self.frame)
        self.password = Entry(self.frame,show="*")
        self.host = Entry(self.frame)
        self.username = Entry(self.frame)
        self.mpass = Entry(self.frame,show="*")

        self.ssid.grid(row=0, column=1)
        self.password.grid(row=1, column=1)
        self.host.grid(row=2, column=1)
        self.username.grid(row=3, column=1)
        self.mpass.grid(row=4,column=1)

        Button(self.frame, text='Quit', command=self.frame.quit).grid(row=6, column=0, sticky=W, pady=4)
        Button(self.frame, text='Send', command=lambda: hermes.send_message(self.constructMessage()) ).grid(row=6, column=1, sticky=W, pady=4)
        self.frame.pack()

def main():
    with connect_arduino() as ser:
        hermes = Messenger(ser)
        root = tk.Tk()
        ui = TextBoxUI(root,hermes)
        root.mainloop()


if __name__ == '__main__':
    main()
