import socket


server_ip = input("Enter the server IP address: ")
server_port = int(input("Enter the server port: "))

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.connect((server_ip, server_port))


while True: # Start infinite loop to send queries
    print("\nChoose a query:")
    print("1) What is the average moisture inside my kitchen fridge in the past 3 hours?")
    print("2) What is the average water consumption per cycle in my smart dishwasher?")
    print("3) Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?)")
    print("Type 'quit' to exit.")

    user_input = input("Enter your choice (1, 2, 3 or 'quit'): ")   # Get user choice

    if user_input in ["1", "2", "3", "quit"]:   # Check for valid input
        myTCPSocket.send(user_input.encode('utf-8'))    # Send input (query) to server

        if user_input == "quit":    # Exit loop if 'quit' is entered
            break

        response = myTCPSocket.recv(1024).decode('utf-8')
        print("Server says:", response)
    else:
        print("Invalid choice. Please type 1, 2, 3, or 'quit'.")    # Handle invalid input

myTCPSocket.close()
print("Disconnected from server.")
