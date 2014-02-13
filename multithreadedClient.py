#!/usr/bin/env python


#################################################################################
#################################################################################
#                                                                               #
#               Multithreaded TCP Client                                        #
#_______________________________________________________________________________#
#                                                                               #
# Author:       Erick Daniszewski                                               #
# Date:         10 October 2013                                                 #
# File:         multithreadedClient.py                                          #
#                                                                               #
# Summary:                                                                      #
#               multithreadedClient.py is a TCP client that maintains a maximum #
#               number of worker threads which continuously send a given number #
#               of requests to multithreadedServer.pu and print the server's    #
#		response.                                                       #
#                                                                               #
#               This is part of an assignment for the Distributed Systems class #
#               at Bennington College                                           #
#                                                                               #
#								                #
# Resources:	QUEUE:                             		                #
#		http://docs.python.org/2/library/queue.html                     #
#               ARGPARSE                                                        #
#               http://docs.python.org/2/library/argparse.html                  #
#                                                                               #
#################################################################################
################################################################################# 



import threading, socket, Queue, argparse




#-------------------------------------------#
########## DEFINE GLOBAL VARIABLES ##########
#-------------------------------------------#

requestMessage = "HELO"

# Create a queue to hold the tasks for the worker threads
q = Queue.Queue(maxsize=0)



#-------------------------------------#
########## ARGUMENT HANDLING ##########
#-------------------------------------#

# Initialize instance of an argument parser
parser = argparse.ArgumentParser(description='Multithreaded TCP Client')

# Add optional arguments, with given default values if user gives no args
parser.add_argument('-r', '--requests', default=10, type=int, help='Total number of requests to send to server')
parser.add_argument('-w', '--workerThreads', default=5, type=int, help='Max number of worker threads to be created')
parser.add_argument('-i', '--ip', default='127.0.0.1', help='IP address to connect over')
parser.add_argument('-p', '--port', default=9000, type=int, help='Port over which to connect')

# Get the arguments
args = parser.parse_args()



#--------------------------------------#
########## CLIENT CONSTRUCTOR ##########
#--------------------------------------#

class Client:
	def __init__(self, id, address, port, message):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.Id = id
		self.Address = address
		self.Port = port
		self.Message = message

	def run(self):
		try:
                        # Timeout if the no connection can be made in 5 seconds
                        self.s.settimeout(5)
                        # Allow socket address reuse
                        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        # Connect to the ip over the given port
			self.s.connect((self.Address, self.Port))
                        # Send the defined request message
			self.s.send(self.Message)
                        # Wait to recieve data back from server
	                data = self.s.recv(1024)
                        # Notify that data has been received
        	        print self.Id, ":  received: ", data
                        # CLOSE THE SOCKET
                	self.s.close()
                # If something went wrong, notify the user
		except socket.error:
			print "\nERROR: Could not connect to ", self.Address, " over port", self.Port, "\n"



#------------------------------------------------#
########## DEFINE QUEUE WORKER FUNCTION ##########
#------------------------------------------------#

# Function which generates a Client instance, getting the work item to be processed from the queue
def worker():
        while True:
                # Get the task from teh work queue
                item = q.get()
                newClient = Client(item, args.ip, args.port, args.requests)
                newClient.run()
		# Mark this task item done, thus removing it from the work queue
                q.task_done()



#--------------------------------------------------#
########## INITIATE CLIENT WORKER THREADS ##########
#--------------------------------------------------#

# Populate the work queue with a list of numbers as long as the total number of requests wished to be sent.
# These queue items can be thought of as decrementing counters for the client thread workers.
for item in range(args.requests):
	q.put(item)

# Create a number of threads, given by the maxWorkerThread variable, to initiate clients and begin sending requests.
for i in range(args.workerThreads):
	t = threading.Thread(target=worker)
	t.daemon = True
	t.start()

# Do not exit the main thread until the subthreads complete their work queue
q.join()


print "Complete!"
