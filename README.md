# FTP-Client-Server

NSCOM01 FTP CLIENT & SERVER This project provides a basic implementation of an FTP client and server, allowing for file transfers between a client and a server over a network. The implementation is done in Python and offers essential FTP commands.

AUTHORS Chua, Judy Telosa, Arwyn

FEATURES - Basic FTP commands (USER, PASS, LIST, RETR, STOR, QUIT, and more) - Passive mode for data transfer - Server-side file management (MKD, RMD, DELE) - Client-side login and file transfer operations - Wireshark friendly

REQUIREMENTS - Python 3.x - Network access between the client and server machines

SETUP To run the FTP client or server, you must have Python installed on your machine. No external libraries are required, as the scripts use the built-in socket module for network communication.

RUNNING THE SERVER 
1. Open a terminal.
2.  Navigate to the directory containing the ftp_server.py script.
3.  Run the script with your machine's IP address as the argument: python ftp_server.py or py ftp_server.py

RUNNING THE CLIENT 
1. Open a terminal.
2. Navigate to the directory containing the ftp_client.py script.
3. Run the script with your machine's IP address as the argument: python ftp_client.py or py ftp_client.py

USAGE After running the client script, you will be prompted to enter FTP commands to interact with the server. 
Available commands include: 
USER : Authenticate with the server using a username. 
PASS : Authenticate with a password. 
LIST: List files in the current directory on the server. 
RETR : Retrieve (download) a file from the server. 
STOR : Store (upload) a file to the server. 
QUIT: Terminate the session and disconnect from the server. However, most FTP commands require the client to log in first before attempting to use the server. The following commands are available without logging in: USER PASS HELP [] QUIT

For detailed command usage, type HELP at the client prompt.

COMMANDS 
USER : Specify the username for authentication. 
PASS : Specify the password for authentication. 
PASV: Enter passive mode for data transfer. 
RETR : Retrieve a file from the server. 
STOR : Upload a file to the server. 
LIST: List files in the current directory on the server. 
HELP []: Display help information about commands. PWD: Print the current working directory on the server. 
CWD : Change the current working directory on the server. 
CDUP: Change the current directory to the parent directory on the server. 
MKD : Create a new directory on the server. 
RMD : Remove a directory on the server. 
DELE : Delete a file on the server. 
QUIT: Quit and close the connection.

ADDITIONAL NOTES - This project is for educational purposes and may not cover all aspects of a fully-featured FTP server or client. - Ensure that the server and client scripts are run on machines that can reach each other over the network. - The default FTP port (21) is used. Make sure it is open and not blocked by firewalls on both the client and server machines.
