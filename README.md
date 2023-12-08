# Telemed-Project
This is the final project for Telemedicine (December, 2023)
In the folder apps the executables files for both the server and the client (admin, health professional and patient) can be found as well as the documentation of the project.
The code used to generate the excutables is located inside the folders Server and Client respectively. 
In the folder client there is also a folder called tests which contain the unittests performed. The library used to establish the connection with Bitalino is 
BITalino API found through Github as other options were tested without success (first we tried employing the library JPype to run the java class provided by the 
teacher from the python client, then we looked for and tried different libraries until reaching the final one).
The modules clientInterface, clientConnection and clientLogic are all used in the client.py which contains the main. clientInterface contains the functions that either read or write
information from and to the terminal. clientConnection includes the functions related to the sockets and sending and receiving messages from them. clientLogic contains the functions
needed to process the data obtained by the other functions.
In the folder Server, there are only two modules: server.py and databaseManager.py. The latter implements the database and manages the storing and retrieving information from it.
The module server.py contains the main and all the functions that are needed both for the logic of the server as well as the sockets managing.

