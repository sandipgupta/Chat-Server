Chat Server

Introduction

This project implemented a basic Peer to Peer chat program.This is a multiuser program. Program supports text messages, voice messages and also support live voice calling. File transfer using FTP in secure as well as normal mode is also supported as a feature in the program.

Methodology

We have implemented this program in python using a number of libraries such as Tkinter for GUI, socket, pyaudio for voice support, and socket for network programming. Work flow of the Program:

Server program is started that create a socket with a port, ready to listen to a client.
Client program create a socket connection and send message to the advertise IP address of Server.
Server receive the Client message reply to the client.
Tkinter is used to make GUI of the program.
Voice message are recorded and converted in to MP3 format and sent to other peer.
File are sent using FTP. First they uploaded on a common server and message is sent regarding the same if other peer say yes for the download FTP connection is set up and file is downloaded.
Secure file transfer preceded by step exchanging Public key of RSA encryption. File is encrypted and then sent.
Result

We have full working program supporting all the feature discussed in Methodology. You need python installed on your computer. Project can be download from https://github.com/sandipgupta/Chat-Server
