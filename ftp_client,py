from socket import *
import os
import sys

PORT = 21
current_dir = os.getcwd()
current_dir = os.path.join(current_dir, "home")
current_dir = os.path.dirname(current_dir)

retr_dir = 'home\downloads'
if not os.path.exists(retr_dir):
    os.makedirs(retr_dir)

class NewErrorFound(Exception):
    pass

def banner_message(name):
    print("------------------------------------------------------------")
    print("              Welcome to NSCOM01 FTP Client!")
    print("                         ", name)
    print("------------------------------------------------------------")

def username(response):
    if "331" in response:
        print("Valid Username! Kindly input your password through the PASS command.\n")
    else:
        print(" >>ERROR: ", response[4:])

def password(response, client_socket):
    if "230" in response:
        find_name = response.split()
        banner_message(find_name[2])
        print() #new line

        try: #set transfer mode and structures in the background
            client_socket.sendall("TYPE I\r\n".encode())
            res_type = client_socket.recv(1024).decode()
            if "200" not in res_type: #200 is The requested action has been successfully completed.
                raise NewErrorFound("Error in setting transfer mode to binary\n")
            
            client_socket.sendall("MODE S\r\n".encode()) # Set the transfer mode to stream. This is for handling data streams.
            res_mode = client_socket.recv(1024).decode()
            if "200" not in res_mode: # Check if the server responded with "200", indicating success
                raise NewErrorFound("Error in setting transfer mode to stream\n")
            
            client_socket.sendall("STRU F\r\n".encode()) # Set the transfer structure to file. This is for handling file transfers.
            res_stru = client_socket.recv(1024).decode()
            if "200" not in res_stru:
                raise NewErrorFound("Error in setting tranfer structure to file\n")
            
        except NewErrorFound as e:
            print(" >>ERROR: ", e)

    elif "430" in response:
        print(" >>ERROR: Incorrect password. You can try again.\n")
    elif "501" in response:
        print(" >>ERROR: ", response[4:])
    else:
        print(" >>ERROR: Kindly use the USER command first before this command. Refer to HELP command for more information.\n")

def passive_mode(response):
    if "227" in response:
        # format: CODE CODE_MESSAGE (A1, A2, A3, A4, P1, P2)
        start = response.find("(")
        end = response.find(")")

        details = response[start+1 : end].split(',') # A1, A2, A3, A4, P1, P2

        ip_address = ".".join(details[:4]) #A1, A2, A3, A4 = A1.A2.A3.A4
        port_numbers = int(details[4]) * 256 + int(details[5]) #p1*256+p2

        data_socket = socket(AF_INET, SOCK_STREAM)

        print(response[4:].strip())
        try:
            data_socket.connect((ip_address, port_numbers))
            print("Data connection established.\n")
        except Exception as e:
            print(f"Failed to establish data connection: {e}\n")
            return None

        return data_socket
    else:
        print(" >>ERROR: PASV command failed: " + response)
        return None

def retrieve_file(data_socket, filename):
    try:
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
            server_directory = os.path.join(new_directory, "home", "downloads") #set the directory to ..\home\downloads

        newfile = os.path.join(server_directory, filename) #add file name
        with open(newfile, 'wb') as file: 
            print("Downloading.", end='', flush=True)
            while True: 
                file_data = data_socket.recv(4096)
                if not file_data: 
                    break 
                file.write(file_data)
                print(".", end='', flush=True)  #prints in the same line as File downloading print
        print()
    except Exception as e: 
        print(f"Error downloading file: {e}\n") 

def send_file(data_socket, filePath):
    try:
        newFilePath = os.path.join(current_dir, filePath) # Construct the full file path using the current directory and the provided file path
        if os.path.isfile(newFilePath):
            filename = os.path.basename(newFilePath) # Extract the filename from the full file path
            print(f"Sending file: {filename}")
            with open(newFilePath, 'rb') as file: # Open the file in binary read mode
                print("File opened for sending.", end='', flush=True)
                while True:
                    file_data = file.read(4096)
                    if not file_data: # Break the loop if no more data is read (end of file)
                        break                     
                    data_socket.sendall(file_data)
                    print(".", end='', flush=True)  #prints in the same line as File opened print
            print()
        else:
            print(f"The specified path is not a file: {newFilePath}")
    except Exception as e:
        print(f"Error sending file: {e}")

if len(sys.argv) != 2: # Check if the number of command-line arguments is exactly 2 (script name and IP address)
    print(f"Usage: {sys.argv[0]} <IP Address>")
    sys.exit(1)

HOST = sys.argv[1]
client_socket = socket(AF_INET, SOCK_STREAM)

def main():
    global current_dir
    try:
        client_socket.connect((HOST, PORT)) #connect to the socket
        ready = client_socket.recv(4096).decode()
        command = "placeholder"
        if ready.split()[0] == "220":
            print("Server ready to use! Log in first using the command \"USER\"")
            while command.strip() != "QUIT": 
                command = input("COMMAND: ").strip()
                command = command + "\r\n"
                client_socket.sendall(command.encode()) #send the command to the server
                response = client_socket.recv(4096).decode() #check what the server said

                if command.startswith("USER"): # Check if the command is USER to handle user authentication
                    username(response)

                elif command.startswith("PASS"): # Check if the command is PASS to handle the password 
                    password(response, client_socket)

                elif command.startswith("PASV"): # Check if the command is PASV for entering passive mode
                    data_socket = passive_mode(response)
                        
                elif command.startswith("LIST"):
                    print(response[4:])
                    if response.startswith("125"):
                        print("Server found: ")
                        new_response = data_socket.recv(4096).decode()  
                        print(new_response)
                        while new_response != '':
                            new_response = data_socket.recv(4096).decode()  
                            print(new_response) #print each filename being sent

                        data_socket.close() #close socket since it is done
                        data_socket = None

                        new_response2 = client_socket.recv(4096).decode() 
                        print(new_response2[4:]) #print server's response

                elif command.startswith("HELP"):
                    if response.startswith("214"):
                        message = response.split('214 Help message\n', 1) #split them into two parts, one part is 214 then the other is the rest
                        print(message[1]) #print the other part since the [0] is the FTP reply
                    else:
                        print(response[4:]) #print the error, no need for the FTP reply code

                elif command.startswith("PWD") or command.startswith("MKD") or command.startswith("RMD") or command.startswith("DELE"):
                    print(response[4:]) # Check for different FTP commands and handle responses accordingly

                elif command.startswith("CWD"):
                    if "250" in response:
                        current_dir = os.path.join(current_dir, command.split()[1]) # Update the current directory path based on the command argument
                    print(response[4:])

                elif command.startswith("CDUP"):
                    if "250" in response:
                        current_dir = os.path.dirname(current_dir) # Change the current directory to its parent
                    print(response[4:])

                elif command.startswith("QUIT"):
                    print(response[4:].strip())
                    print("Thank you for using FTP client! Ending session.\n")
                    break

                elif command.startswith("RETR"):  
                    print(response[4:].strip())
                    if data_socket and "125" in response: # Data connection open; transfer starting
                        filename = os.path.basename(command.split()[1])
                        retrieve_file(data_socket, filename)   # Call function to retrieve the file
                        data_socket.close()  
                        new_response = client_socket.recv(4096).decode() 
                        if "226" in new_response:
                            print("File download completed.\n") 
                        else:
                            print(new_response[4:])
                    
                elif command.startswith("STOR"):   
                    print(response[4:].strip())
                    if data_socket and "125" in response:    # Data connection open; transfer starting
                        send_file(data_socket, command.split()[1])   # Call function to retrieve the file
                        data_socket.close()  
                        new_response = client_socket.recv(4096).decode()
                        if "226" in new_response:
                            print("File upload completed.\n")
                        else:
                            print("File upload failed. No data received from server.\n")

                else:
                    print(" >>ERROR: ", response[4:])
        else:
            print("Server not ready")
        client_socket.close()
    except KeyboardInterrupt:
        print("Client is shutting down")
    except Exception as e:
        print("Unknown Error..." + str(e))

main()
