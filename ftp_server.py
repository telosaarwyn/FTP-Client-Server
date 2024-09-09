from socket import *
import os
import sys
import random

PORT = 21
list_users = ["john", "jane", "joe"]
list_pass = ["1234", "5678", "qwerty"]
REPLY_501 = '501 Syntax error in parameters or arguments (Refer to HELP for more information)\r\n'

# directory
stor_dir = 'home\server_site'
if not os.path.exists(stor_dir):
    os.makedirs(stor_dir)


class NewErrorFound(Exception):
    pass

def banner_message():
    print("============================================================")
    print("|              Welcome to NSCOM01 FTP Server!              |")
    print("|                  by Telosa and Chua :3                   |")
    print("============================================================")

def port_avail(num, addr):
    try:
        random_socket = socket(AF_INET, SOCK_STREAM) #create socket
        random_socket.bind((addr, num)) #bind socket
        print(f"Available port {num} at {addr}")
        return random_socket #if successful, return the socket
    except:
        print(f"Not available port {num} at {addr}")
        return None


def listen_client(socket, address):
    currentUser = None #index for the user being logged in
    loggedIn = None #is user already logged in?
    new_socket = None #for data connection client side
    data_socket = None #for data connection establishment
    list_of_commands = ["USER", "PASS", "PWD", "CWD", "CDUP", "MKD", "RMD",
                        "PASV", "LIST", "RETR", "DELE", "STOR", "HELP", "QUIT"]
    no_user_commands = ["USER", "PASS", "QUIT", "HELP"]
    request = "placeholder"

    while True:
        if not "TYPE" in request and not "MODE" in request and not "STRU" in request:
            print("Listening for commands...")

        request_n = socket.recv(1024).decode() # receive command from client
        request = request_n.strip()

        if not "TYPE" in request and not "MODE" in request and not "STRU" in request:
            print("COMMAND RECEIVED FROM CLIENT:", request)
        
        
        #check command's structure
        if len(request.split(" ")) > 1: #more than one word
            split_req = request.split() #each word is stored in an list
            command = split_req[0].upper() #transformed into uppercase for easy comparison
        else:
            command = request.upper()
            split_req = [] #no list

        #check username of client
        if command == "USER": 
            currentUser = None
            response = None
            if len(split_req) == 0 or len(split_req) > 2: #either USER or USER with two or more parameters
                response = REPLY_501 #error response
            else: #should only be USER <username>
                user = False #checker if username exists
                for index, x in enumerate(list_users): #list of users
                    if x == split_req[1]: #split_req[0] is the command
                        user = True #user exists
                        currentUser = index #for password
                        loggedIn = False #user isn't done logging in
                        break
                if user: #username exists
                    response = '331 Password Required\r\n'
                else:
                    response = '430 Invalid Username\r\n'
            socket.sendall(response.encode()) #send to client
            print(f"Sent to client USER - {response}") #print to server the response

        #check password of client based on user
        elif command == "PASS":
            data = None
            if len(split_req) == 0 or len(split_req) > 2: #either PASS or PASS with two or more parameters
                data = REPLY_501
            else: #should only be PASS <password>
                if currentUser is not None and loggedIn is False: #user should be implemented first
                    if list_pass[currentUser] == split_req[1]: #based on username
                        data = f'230 User {list_users[currentUser]} Logged In\r\n'
                        loggedIn = True
                    else:
                        data = '430 Invalid Password\r\n'
                elif loggedIn is True: #user has already logged in and they input PASS
                    data = '503 User is already logged in\r\n'
                else: #user hasn't input USER yet
                    data = '503 Bad sequence of commands -- USER first before PASS\r\n'

            socket.sendall(data.encode()) #send to client
            print(f"Sent to client PASS - {data}") #remove

        elif command == "HELP":
            response = None
            if len(split_req) > 2: #HELP with two or more parameters
                response = '501 Syntax error in parameters or arguments (Either type HELP or HELP <command>)\r\n'
            else: #should only be HELP or HELP <command>
                help_response = '214 Help message\n'
                help = [
                'Available commands (Note: [optional] <required>):\n',
                '   USER <username>\n', 
                '   PASS <password>\n',
                '   PWD                   - prints working directory\n',
                '   CWD <pathname>        - change working directory\n',
                '   CDUP                  - change working directory to parent directory\n',
                '   MKD <pathname>        - make directory\n',
                '   RMD <pathname>        - remove directory\n',
                '   PASV                  - open data connection\n',
                '   LIST [pathname]       - print current list of files\n',
                '   RETR <pathname>       - retrieve/get file\n',
                '   DELE <pathname>       - delete files\n',
                '   STOR <pathname>       - store file at server site\n',
                '   TYPE <type-code>      - ASCII/Binary mode\n',
                '   MODE <mode-code>      - Stream, Block or Compressed\n',
                '   STRU <structure-code> - set file transfer structure\n',
                '   HELP [<command>]      - specific command help\n',
                '   QUIT                  - close socket\n']
                if len(split_req) == 2: #if HELP <command> so with parameter
                    index = -1 
                    for i, x in enumerate(help): #iterate through the help array
                        if split_req[1] in x:
                            index = i #index of the command
                            break
                    if index == -1: #this means command does not exists
                        new_help = f'502 Unknown command: {split_req[1]}'
                    else:
                        new_help = help[index] #print the help
                    response = help_response + new_help #add the FTP reply and the HELP command to the response
                else:
                    response = help_response #add the FTP reply
                    for x in help:
                        response += x #add all the HELP commands

            socket.sendall(response.encode()) #send to client
            print(f"Sent to client HELP - {help_response if help_response else response}")
                                        #help_response is success, response is not --in this case

        #close socket
        elif command == "QUIT": #param checker
            response = "Unknown"
            print(f"Client {list_users[currentUser] if loggedIn else response} has disconnected") #print into server that server quit
            socket.sendall(b'221 Service closing control connection\r\n') #inform client its response
            break
        
        #checks first if user logs in already --- otherwise send error message
        if loggedIn or command in no_user_commands: 
            #print working directory
            if command == "PWD":
                if len(split_req) != 0: #PWD with parameters
                    response = REPLY_501
                else:
                    try:
                        current_directory = os.getcwd() #get current directory
                        response = f'250 "{current_directory}" is the current directory\r\n' #250 is Requested file action okay, completed.
                    except Exception as e:
                        response = f'550 Failed to get current directory: {str(e)}\r\n' #550 means Requested action not taken
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client PWD - {response}")

            #change working directory
            elif command == "CWD":
                if len(split_req) == 0 or len(split_req) > 2: #Either CWD or CWD with two or more parameters
                    response = REPLY_501
                else: 
                    try:
                        os.chdir(split_req[1])  #split_req[1] is the new directory path
                        response = f'250 Directory successfully changed.\r\n'
                    except Exception as e:
                        response = f'550 Failed to change directory. Error: {str(e)}\r\n'
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client CWD - {response}")
            
            #change the client’s current working directory to the immediate parent directory of the current working directory
            elif command == "CDUP":
                if len(split_req) != 0: #CDUP with parameters
                    response = REPLY_501
                else: 
                    try:
                        os.chdir('..')  # Change the current working directory to the parent directory
                        response = '250 Directory successfully changed to parent directory.\r\n'
                    except Exception as e:
                        response = f'550 Failed to change directory. Error: {str(e)}\r\n'
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client CDUP - {response}")

            #make directory
            elif command == "MKD":
                if len(split_req) == 0 or len(split_req) > 2: #Either MKD or MKD with two or more parameters
                    response = REPLY_501
                else: 
                    try:
                        os.mkdir(split_req[1])  # split_req[1] is the directory name
                        response = f'257 Directory ({split_req[1]}) created.\r\n'
                    except Exception as e:
                        response = f'550 Failed to create directory. Error: {str(e)}\r\n'
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client MKD - {response}")

            #remove directory
            elif command == "RMD":
                if len(split_req) == 0 or len(split_req) > 2: #Either RMD or RMD with two or more parameters
                    response = REPLY_501
                else:
                    try:
                        os.rmdir(split_req[1])  # split_req[1] is the directory name
                        response = f'250 Directory ({split_req[1]}) removed.\r\n'
                    except Exception as e:
                        response = f'550 Failed to remove directory. Error: {str(e)}\r\n'
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client RMD - {response}")

            #
            elif command == "PASV":
                if len(split_req) != 0:
                    response = REPLY_501
                    socket.sendall(response.encode()) #send to client
                    print(f"Sent to client PASV - {response}")
                else:
                    while data_socket is None:
                        port_num = random.randint(1000, 65535) #get random number
                        data_socket = port_avail(port_num, HOST) #creates the socket for data connection

                    if data_socket:
                        #('192.168.1.14', 51444)
                        addr, _ = address
                        #IP address = (a1.a2.a3.a4)
                        a1, a2, a3, a4 = addr.split(".")
                        #Port number = p1*256+p2 -- (port_num-p2)/256 = p1 -- p2 is excess
                        p1, p2 = divmod(port_num, 256)
                        #create the message to be sent to client with address and port number
                        response = f"227 Entering Passive Mode ({a1},{a2},{a3},{a4},{p1},{p2}).\r\n"
                        #listen for incoming connections
                        data_socket.listen(1)
                        #send formatted successful PASV message of 227 to client
                        socket.sendall(response.encode()) #send to client
                        print(f"Sent to client PASV - {response.strip()}") #show to server -- strip() removes the \r\n

                        conn, addr = data_socket.accept() #wait for client to connect
                        print(f"Data connection accepted from {addr}\n") #show that client has connected to the data connection
                        new_socket = conn #set the new socket to this connection
            
            #print current list of files
            elif command == "LIST":
                if len(split_req) > 2: #LIST with two or more parameters
                    response = REPLY_501
                    socket.sendall(response.encode()) #send to client
                    print(f"Sent to client LIST - {response}")
                else:
                    try:
                        if len(split_req) == 0:
                            dir = os.getcwd() #get current directory
                        else: 
                            dir = split_req[1] #get given directory

                        if new_socket:
                            files = os.listdir(dir) #check if directory exists
                            data = '125 Data connection already open. Starting transfer.\r\n'
                            socket.sendall(data.encode()) #send that it will use data connection
                            print("SENDING LIST TO CLIENT", files)
                            if not files:
                                new_socket.sendall("  Empty Folder...\r\n".encode()) #empty
                            count = 0
                            for x in files:    
                                if os.path.isfile(x): #add file names
                                    count = 1
                                    new_socket.sendall(x.encode()) #send each file names
                            if count == 0:
                                new_socket.sendall('No files but it has folders'.encode()) 
                            else:
                                new_socket.sendall(''.encode()) 

                            new_socket.close() #end data connection since it is done
                            new_socket = None #indicate that is it close
                            data_socket = None #for reset

                            socket.sendall(b'226 Transfer complete.\r\n') #send file confirmation to the server that it is done
                            print(f"Done transferring!\n")
                                                     
                        else:
                            socket.sendall(b'425 Can\'t open data connection. Activate PASV first!\r\n') #there is no data connection
                    except Exception as e:
                        socket.sendall(b'550 Transfer failed. Closing the socket\r\n') 
                        print(f"Error during file transfer: {e}\n")
                        new_socket.close() #end data connection since error
                        new_socket = None #indicate that is it close
                        data_socket = None #for reset

            #upload data at the server site
            elif command == "STOR":
                if len(split_req) == 0 or len(split_req) > 2: #Either RETR or RETR with two or more parameters
                    response = REPLY_501
                    socket.sendall(response.encode())  #send to client
                    print(f"Sent to client STOR - {response}") #show in server side the response to be sent
                else:
                    filename = split_req[1]  
                    if new_socket:
                        received_data = False #indicator if there is data being received
                        try:
                            if os.path.isfile(filename): #check if file is file
                                filePath = os.path.basename(filename) #only get the end of the directory since that is the file itself
                            else:
                                raise NewErrorFound("Error!! That is not a file! Try again\n")

                            current_directory = os.getcwd() #get current directory
                            directories = current_directory.split(os.sep) # split the directory path into its components
                                                            #os.sep refers to the separator (either '\' or '/')
                            new_directory = None
                            for index, component in enumerate(directories): #iterate over the whole directory since they are separated
                                if "home" in component: #find "home"
                                    break
                                new_directory = os.sep.join(directories[:index + 1]) #combine the following until home is found

                            if new_directory is None: #this means "home" is not found, which means the file is outside the home folder
                                raise NewErrorFound("Error!! Image is not in home folder.\n")
                            else:
                                server_directory = os.path.join(new_directory, "home", "server_site") #set the directory to ..\home\server_site
                            
                            newfile = os.path.join(server_directory, filePath) #set to default server site for uploading or storage
                            with open(newfile, 'wb') as file:
                                response = '125 Data connection already open. Storing file.\r\n' #there is data connection
                                socket.sendall(response.encode()) #send that to client first
                                print(f"Starting storing file {filePath} in server site folder.") #indicate that server will start uploading the file
                                while True:
                                    data = new_socket.recv(4096) #receive that data from the new socket established (data connection)
                                    if not data: #no more data to write
                                        break
                                    received_data = True #indicate that there is data received
                                    file.write(data) #write the data

                            if received_data: #indicates if server received data
                                print("File transfer complete.\n")
                                socket.sendall(b'226 Transfer complete.\r\n') #send success message
                            else:
                                print("No data received.\n") 
                                socket.sendall(b'550 Transfer failed. No data received. Closing the socket\r\n') #send error

                        except NewErrorFound as e:
                            socket.sendall(f'550 Transfer failed. File not found. Closing the socket\r\n'.encode()) 
                            print(e) #show in server side the response to be sent

                        except Exception as e:
                            socket.sendall(f'550 Transfer failed. Closing the socket\r\n'.encode()) 
                            print(f"Error during file transfer: {e}\n") #show in server side the response to be sent
                        
                        new_socket.close() #end data connection even if error
                        new_socket = None #indicate that is it close
                        data_socket = None #for reset when activating PASV

                    else:
                        response = '425 Can\'t open data connection. Activate PASV first!\r\n' #there is no data connection
                        socket.sendall(response.encode()) #send to client
                        print(f"Sent to client STOR - {response}") #show in server side the response to be sent

            #retrieve/get file(s)
            elif command == "RETR":
                if len(split_req) == 0 or len(split_req) > 2: #Either RETR or RETR with two or more parameters
                    response = REPLY_501 #error message
                    socket.sendall(response.encode()) #send to client
                    print(f"Sent to client RETR - {response}") #show in server side the response to be sent
                else:
                    filename = split_req[1] 
                    try:
                        if data_socket: #check if there is data connection
                            with open(filename, 'rb') as file: #check if file exists
                                print("Starting transfer of file") #indicate start of transfer since file exists
                                socket.sendall(b'125 Data connection already open. transfer starting.\r\n') #send to client that transfer will begin
                                while True:
                                    data = file.read(4096) #read the file by 4096 bytes
                                    if not data:
                                        break  # End of file
                                    new_socket.sendall(data) #send that file data to the data connection
                        
                            socket.sendall(b'226 Transfer complete.\r\n') #send to client
                            print("File transfer complete.\n") 
                            
                        else:
                            response = '425 Can\'t open data connection. Activate PASV first!\r\n' #there is no data connection
                            socket.sendall(response.encode()) #send to client
                            print("ERROR: No data connection.\n")
                       
                    except FileNotFoundError as e:
                        socket.sendall(b'451 File not found. Closing the socket\r\n') 
                        print(f"Error: {e}\n")
                    except Exception as e:
                        socket.sendall(b'550 Transfer failed. Closing the socket\r\n') 
                        print(f"Error during file transfer: {e}\n")
                    
                    if new_socket:
                        new_socket.close() #end data connection since it is done
                        new_socket = None #indicate that is it close
                        data_socket = None #for reset

            #delete files
            elif command == "DELE":
                if len(split_req) == 0 or len(split_req) > 2: #Either DELE or DELE with two or more parameters
                    response = REPLY_501
                else:
                    try:
                        os.remove(split_req[1])  # split_req[1] is the file name
                        response = f'250 File {split_req[1]} deleted.\r\n'
                    except Exception as e:
                        response = f'550 Failed to delete file. Error: {str(e)}\r\n'
                socket.sendall(response.encode()) #send to client
                print(f"Sent to client DELE - {response}") #remove

            #transfer mode (ASCII/Binary)
            elif command == "TYPE":
                type_mode = split_req[1]
                if type_mode.upper() == "I": # Set to 8-bit binary data mode
                    response = '200 Switching to Binary mode.\r\n'
                else:
                    response = '504 Command not implemented for that parameter.\r\n'
                socket.sendall(response.encode()) #send to client

            #sets the transfer mode (Stream, Block, or Compressed)
            elif command == "MODE":
                mode = split_req[1]
                if mode.upper() == "S":  # only Stream mode is implemented
                    response = '200 Setting Transfer mode to Stream.\r\n'
                else:
                    response = '502 Command not implemented.\r\n'
                socket.sendall(response.encode()) #send to client

            #set file transfer structure
            elif command == "STRU":
                structure = split_req[1]
                if structure.upper() == "F":  # only File structure is supported
                    response = '200 File structure set.\r\n'
                else:
                    response = '504 Command not implemented for that parameter.\r\n'
                socket.sendall(response.encode())

        elif command in list_of_commands:
            socket.sendall('530 Need to log in first before accessing the other commands.\r\n'.encode()) #send to client
            print(f"Not logged in. Sent to client - 530") #remove
            
        else:
            socket.sendall('500 Command does not exist!'.encode()) #send to client
            print(f"Unknown Command. Sent to client - 500") #remove

    socket.close() # close the client socket
    return "done"


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <IP Address>")
    sys.exit(1)

HOST = sys.argv[1]
server_socket = socket(AF_INET, SOCK_STREAM)

def main():
    server_socket.bind((HOST, PORT)) #server will listen in this port
    server_socket.listen(5)
    print(f"Server listening on port {PORT}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection accepted from {client_address}!")
            client_socket.sendall(b'220 FTP Server Ready\r\n') #send that server is ready
            banner_message() #welcome message
            message = listen_client(client_socket, client_address) #client requests will be handled here
            if message == "done": #if client quits, end the server
                break
    except KeyboardInterrupt:
        print("Server is shutting down")
    except ConnectionAbortedError as e:
        print(f"Connection Aborted Error: {e}")
    except OSError as e:
        print(f"Unexpected error: {e}")
    finally:
        server_socket.close()
        sys.exit(1)

main()
