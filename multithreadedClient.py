#!/usr/bin/env python
"""
Multi-threaded TCP Client

multithreadedClient.py is a TCP client that maintains a maximum number of worker threads which continuously send a given
number of requests to multithreadedServer.py and print the server's response.

This is derived from an assignment for the Distributed Systems class at Bennington College
"""

from Queue import Queue
from argparse import ArgumentParser
from socket import SO_REUSEADDR, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET
from threading import Thread

# -------------------------------------#
########## ARGUMENT HANDLING ##########
#-------------------------------------#

# Initialize instance of an argument parser
parser = ArgumentParser(description='Multi-threaded TCP Client')

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
        self.s = socket(AF_INET, SOCK_STREAM)
        self.id = id
        self.address = address
        self.port = port
        self.message = str(message)

    def run(self):
        try:
            # Timeout if the no connection can be made in 5 seconds
            self.s.settimeout(5)
            # Allow socket address reuse
            self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # Connect to the ip over the given port
            self.s.connect((self.address, self.port))
            # Send the defined request message
            self.s.send(self.message)
            # Wait to receive data back from server
            data = self.s.recv(1024)
            # Notify that data has been received
            print self.id, ":  received: ", data
            # CLOSE THE SOCKET
            self.s.close()
        # If something went wrong, notify the user
        except error as e:
            print "\nERROR: Could not connect to ", self.address, " over port", self.port, "\n"
            raise e

#------------------------------------------------#
########## DEFINE QUEUE WORKER FUNCTION ##########
#------------------------------------------------#

# Create a queue to hold the tasks for the worker threads
q = Queue(maxsize=0)


# Function which generates a Client instance, getting the work item to be processed from the queue
def worker():
    message = "HELO"

    while True:
        # Get the task from teh work queue
        item = q.get()

        new_client = Client(item, args.ip, args.port, message)
        new_client.run()
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
    t = Thread(target=worker)
    t.daemon = True
    t.start()

# Do not exit the main thread until the sub-threads complete their work queue
q.join()
