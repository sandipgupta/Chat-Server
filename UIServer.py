from Tkinter import *
# from socket import *
from ftplib import FTP
import tkFileDialog
from tkMessageBox import *
import thread
import sys
import pyaudio
import wave
import threading
import socket
import time 
########### FILE UPLOAD ###########3

########### MODIFY ########################

USER = 'amitkmr'
PASS = '121258'

########### MODIFY IF YOU WANT ############
call_flag = True
SERVER = 'webhome.cc.iitk.ac.in'
PORT = 21
BINARY_STORE = True # if False then line store (not valid for binary files (videos, music, photos...))
CLIENT_ADDRESS = ('','')
###########################################

RECORD_SECONDS = 1
CALL = 1
connection_done = False  # to check if connection is established or not


def print_line(result):
    print(result)

def connect_ftp():
    #Connect to the server
    ftp = FTP()
    ftp.connect(SERVER, PORT)
    ftp.login(USER, PASS)

    return ftp

def upload_file(ftp_connetion, upload_file_path):

    #Open the file
    try:
        upload_file = open(upload_file_path, 'r')

        #get the name
        path_split = upload_file_path.split('/')
        final_file_name = path_split[len(path_split)-1]

        #transfer the file
        print('Uploading ' + final_file_name + '...')

        if BINARY_STORE:
            ftp_connetion.storbinary('STOR '+ final_file_name, upload_file)
        else:
            #ftp_connetion.storlines('STOR ' + final_file_name, upload_file, print_line)
            ftp_connetion.storlines('STOR '+ final_file_name, upload_file)

        print('Upload finished.')
        return

    except IOError:
        print ("No such file or directory... passing to next file")


#Take all the files and upload all
ftp_conn = connect_ftp()

def file_save():
    f = tkFileDialog.asksaveasfilename()
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    return f

def retrieveFile(list):
    Tk().withdraw()
    file_extension = list.split('.')
    if askyesno('Download File', 'Yes you really want to Download file'):
        ftp = FTP('webhome.cc.iitk.ac.in')
        ftp.login(user='amitkmr', passwd = '121258')
        filename =list
        save_path = ''
        if len(file_extension) == 1:
        	save_path = file_save()
        else:
        	save_path = file_save()+'.'+file_extension[1]
        localfile = open( save_path, 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        ftp.quit()
        showwarning('File downloaded', 'you have recieved a file')
    else:
        showinfo('File Download Cancel', 'Download quit')

def sendFile():
    Tk().withdraw()
    filePath =tkFileDialog.askopenfilename()
    #print filePath
    upload_file(ftp_conn,filePath)
    filename = filePath.split('/')
    message = "1^"+filename[-1]
    # print message
    conn.send(message)
    chatBox("File sent "+filename[-1])


def sendMessage(event):
    if connection_done :
        message = entry1.get()
        conn.send(message)
        chatBox("You: "+message)
    else :
        chatBox("Connection not yet established")

def recievedMessage():
    while 1:
        global CLIENT_ADDRESS
        if call_flag:
	        message = conn.recv(1024)
	        splitMessage = message.split('^')
	        if splitMessage[0]=="1":
	            fileName = splitMessage[1]
	            chatBox("Recieved file :" + fileName)
	            retrieveFile(fileName)
	        elif splitMessage[0]=="2":
	            chatBox(splitMessage[1])
	            global connection_done
	            connection_done = True
	            entry2.config(state=DISABLED)
	        elif splitMessage[0]=="3":
	            if askyesno('Incoming Call', 'Do you want to receive?'):
	            	message = "5^accept call"
	            	conn.send(message)
	                call1()
	            else:
	                message = "6^end call"
	                conn.send(message)
	        elif splitMessage[0]=="5":
	        	    call1()
	       	elif splitMessage[0]=="6":
	       		chatBox("Call Rejected")
	        else:
	        	if message != '':
	        		chatBox("He: " + message)

def chatBox(text):
    listbox.insert(END, text)
    listbox.pack(side=LEFT, fill=BOTH)
    listbox.yview(END)
    scrollbar.config(command=listbox.yview)
    entry1.delete(0, END)
    return

def setIP (event):
    ipaddress = entry2.get()
    global serverName
    global connection_done
    global CLIENT_ADDRESS
    serverName = ipaddress
    CLIENT_ADDRESS = (serverName,serverPort)
    try:
        conn.connect(CLIENT_ADDRESS)
        message = "2^Someone has connected to you"
        conn.send(message)
        connection_done = True
        chatBox("Connected to " + ipaddress)
    except Exception, e :
        chatBox("Unknown service")
    entry2.delete(0, END)

def start_record ():
    global RECORD_SECONDS
    RECORD_SECONDS=1
    try:
        thread.start_new_thread(record,())
    except:
        print "Error: unable to start thread"

def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    while RECORD_SECONDS==1:
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def stop_record():
    global RECORD_SECONDS
    RECORD_SECONDS = 0
    send_audio('output.wav')

def send_audio():
    upload_file(ftp_conn,audio_file)
    message = "1^"+audio_file
    conn.send(message)

def call():
    message = "3^incoming call"
    conn.send(message)
    
def call1():
	entry1.config(state=DISABLED)
	global call_flag
	call_flag = False
	global CALL
	CALL =1
	threading.Thread(target=call_send).start()
	threading.Thread(target=call_recv).start()

def end_call1():
    global CALL
    CALL = 0
    # time.sleep(2)
    chatBox("* call ended")
    global call_flag
    call_flag = True
    entry1.config(state="normal")
    # chatBox(call_flag)
def end_call():
	global CALL
	CALL = 0
	time.sleep(2)
	message="4^incoming call"
	conn.send(message)
	chatBox("* call ended")
	global call_flag
	call_flag = True
	entry1.config(state="normal")

def call_send():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 20

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
	                channels=CHANNELS,
	                rate=RATE,
	                input=True,
	                frames_per_buffer=CHUNK)

	chatBox("* call start")

	frames = []
	# chatBox(CALL)
	while CALL==1:
	 data  = stream.read(CHUNK)
	 frames.append(data)
	 conn.sendall(data)
	 if CALL == 0:
	 	return

	# chatBox("chat_end")
	stream.stop_stream()
	stream.close()
	p.terminate()

def call_recv():

	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	RECORD_SECONDS = 20
	WAVE_OUTPUT_FILENAME = "server_output.wav"
	WIDTH = 2
	frames = []

	p = pyaudio.PyAudio()
	stream = p.open(format=p.get_format_from_width(WIDTH),
	                channels=CHANNELS,
	                rate=RATE,
	                output=True,
	                frames_per_buffer=CHUNK)

	data = conn.recv(1024)

	while CALL==1:
	    stream.write(data)
	    data = conn.recv(1024)
	    splitMessage = data.split('^')
	    if splitMessage[0]=="4":
	    	 # chatBox("please call end")
	         end_call1()
	         return 
	    frames.append(data)
	    if CALL ==0:
	    	return

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	stream.stop_stream()
	stream.close()
	p.terminate()

########## Socket Connection ###############
serverName = ''
serverPort = 12011

# s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('', serverPort))
# s.listen(1)
# conn, addr = s.accept()
# conn, addr = s.accept()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', serverPort))
s.listen(1)
conn, addr = s.accept()

window = Tk()
window.title("chatWindow")
window.geometry("400x500")
frame = Frame(window)
frame.pack(side = TOP, fill = X)

frame1 = Frame(window)
frame1.pack(side = BOTTOM, fill = X)

button = Button(window, text ="Send File",command= sendFile)
button.pack(side=BOTTOM)

button1 = Button(frame1, text ="record",command= start_record)
button1.pack(side=LEFT)

button2 = Button(frame1, text ="stop & send",command= stop_record)
button2.pack(side=LEFT)

button3 = Button(frame1, text ="Call",command= call, bg = '#29ab22')
button3.pack(side=RIGHT)

button4 = Button(frame1, text ="End",command= end_call,bg = '#df2620')
button4.pack(side=RIGHT)


message = StringVar()
entry1 = Entry(window,text = message)
entry1.pack(side=BOTTOM,fill=X)
entry1.bind("<Return>", sendMessage)

scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(window, width = 50,yscrollcommand=scrollbar.set)




label1 = Label( frame, text="Connect to IP address : " , bg = "#a3dfdd" )
label1.pack(fill = X, side = LEFT, ipadx=20)

ipaddress = StringVar()
entry2 = Entry(frame,text = ipaddress,width=30)
entry2.pack(side=LEFT)
entry2.bind("<Return>", setIP)

############### Start recieved message as thread ########3
try:
   thread.start_new_thread(recievedMessage,())
except:
   print "Error: unable to start thread"
frame.pack()

window.mainloop()

