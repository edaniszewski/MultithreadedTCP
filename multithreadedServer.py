#!/usr/bin/env python


#################################################################################
#################################################################################
#                                                                               #
#               Multithreaded TCP Server                                        #
#_______________________________________________________________________________#
#                                                                               #
# Author:       Erick Daniszewski                                               #
# Date:         10 October 2013                                                 #
# File:         multithreadedServer.py                                          #
#                                                                               #
# Summary:                                                                      #
#               multithreadedServer.py acts as a standard TCP server, with		#
#               multithreaded integration, spawning a new thread for each 		#
#               client request it receives. 									#
#																				#
#               This is part of an assignment for the Distributed Systems class #
#               at Bennington College                                           #
#                                                                               #
#################################################################################
################################################################################# 



import socket, threading, argparse





#-------------------------------------------#
########## DEFINE GLOBAL VARIABLES ##########
#-------------------------------------------#

counter = 0
responseMessage = "Now serving, number: "
threadLock = threading.Lock()

# Create a server TCP socket and allow address re-use
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Create a list in which threads will be stored in order to be joined later
threads = []



#---------------------------------------#
########## USER INPUT HANDLING ##########
#---------------------------------------#

# Initialize instance of an argument parser
parser = argparse.ArgumentParser(description='Multithreaded TCP Server')

# Add optional argument, with given default values if user gives no arg
parser.add_argument('-p', '--port', default=9000, type=int, help='Port over which to connect')

# Get the arguments
args = parser.parse_args()



#---------------------------------------------------------#
########## THREADED CLIENT HANDLER  CONSTRUCTION ##########
#---------------------------------------------------------#

class clientHandler(threading.Thread):

	def __init__(self, address, port, socket, responseMessage, lock):
		threading.Thread.__init__(self)
		self.Address = address
		self.Port = port
		self.Socket = socket
		self.ResponseMessage = responseMessage
		self.Lock = lock
	
	# Define the actions the thread will execute when called.	
	def run(self):
		global counter
		self.Socket.send(self.ResponseMessage + str(counter))
		# Lock the changing of the shared counter value to prevent erratic multithread changing behavior
		self.Lock.acquire()
		counter += 1
		# Release the lock so others can use counter
		self.Lock.release()
		self.Socket.close()



#-----------------------------------------------#
########## MAIN-THREAD SERVER INSTANCE ##########
#-----------------------------------------------#

# Continuously listen for a client request and spawn a new thread to handle every request
while 1:

	try:
		# Listen for a request
		s.listen()
		# Accept the request
		sock, addr = s.accept()
		# Spawn a new thread for the given request
		newThread = clientHandler(addr[0], addr[1], sock, responseMessage, threadLock)
		newThread.start()
		threads.append(newThread)
	except KeyboardInterrupt:
		print "\nExiting Server\n"
		break

# When server ends gracefully (through user keyboard interrupt), wait until remaining threads finish
for item in threads:
	item.join()
