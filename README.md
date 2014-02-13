Multithreaded Client & Server
=============================

To use, start the server in a terminal window, `python multithreadedServer.py`
In a second window, run the client, `python multithreadedClient.py`


### Multithreaded TCP Server 

usage: multithreadedServer.py [-h] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port over which to connect


### Multithreaded TCP Client 

usage: multithreadedClient.py [-h] [-r REQUESTS] [-w WORKERTHREADS] [-i IP] [-p PORT]

optional arguments:
  -h, --help            							show this help message and exit
  -r REQUESTS, --requests REQUESTS 					Total number of requests to send to server
  -w WORKERTHREADS, --workerThreads WORKERTHREADS 	Max number of worker threads to be created
  -i IP, --ip IP        							IP address to connect over
  -p PORT, --port PORT  							Port over which to connect








This project was part of an assignment for the Distributed Systems class at Bennington College