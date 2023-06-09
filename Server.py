import socket
import os
import json
import csv

# Function to send a file to a specific client
def send_file(file_path, client_socket):
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file data
        file_data = file.read()

    # Get the file size
    file_size = os.path.getsize(file_path)

    # Send the file size to the client
    client_socket.send(str(file_size).encode())

    # Wait for the client to acknowledge the file size
    client_socket.recv(1024)

    # Send the file data to the client
    client_socket.sendall(file_data)

    # Wait for the client to acknowledge the file receipt
    client_socket.recv(1024)

# Function to receive a file from a specific client
def receive_file(file_path, client_socket):
    # Receive the file size from the client
    file_size = int(client_socket.recv(1024).decode())

    # Acknowledge the file size receipt
    client_socket.send(b'OK')

    # Create a buffer to hold the file data
    file_data = b''

    # Keep receiving data until the entire file is received
    while len(file_data) < file_size:
        chunk = client_socket.recv(1024)
        file_data += chunk

    # Write the received data to a file
    with open(file_path, 'wb') as file:
        file.write(file_data)

    # Acknowledge the file receipt
    client_socket.send(b'OK')

# Function to send a file to multiple clients
def broadcast_file(file_path, client_sockets):
    # Iterate over all the client sockets
    for client_socket in client_sockets:
        # Send the file to each client
        send_file(file_path, client_socket)

# Function to handle the visualization of different file types
def visualize_file(file_path):
    # Check the file extension
    _, file_extension = os.path.splitext(file_path)

    # Image file
    if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
        # Use your preferred method to visualize the image file
        # Example: Use PIL library to open and display the image
        from PIL import Image
        img = Image.open(file_path)
        img.show()

    # CSV file
    elif file_extension.lower() == '.csv':
        # Read and display the CSV file using the csv module
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                print(row)

    # JSON file
    elif file_extension.lower() == '.json':
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)

        choice = input("Enter '1' to display full data or '2' to display data from a specific date: ")

        if choice == '1':
            # Display the full JSON data
            print(json_data)
        elif choice == '2':
            date = input("Enter the date (YYYY-MM-DD): ")
            # Display data from a specific date
            filtered_data = [entry for entry in json_data if entry.get('date') == date]
            print(filtered_data)
        else:
            print("Invalid choice. Please try again.")

    else:
        print("Unsupported file type.")

# Function to display the menu and handle user choice
def show_menu(client_sockets):
    print("1. Send a file to another client")
    print("2. Visualize an image, CSV, or JSON file")
    print("3. Broadcast a file to multiple clients")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        file_path = input("Enter the path of the file to send: ")
        # Call the function to send the file to another client

    elif choice == '2':
        file_path = input("Enter the path of the file to visualize: ")
        visualize_file(file_path)  # Call the function to visualize the file

    elif choice == '3':
        file_path = input("Enter the path of the file to broadcast: ")
        # Call the function to broadcast the file to multiple clients
        broadcast_file(file_path, client_sockets)
        print("File broadcasted successfully.")

    elif choice == '4':
        return

    else:
        print("Invalid choice. Please try again.")

    show_menu(client_sockets)

# Main function for the server
def server_main():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('127.0.0.1', 8006)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)
    print("Server is listening on {}:{}".format(server_address[0], server_address[1]))

    # List to hold connected client sockets
    client_sockets = []

    # Accept incoming connections
    while True:
        client_socket, client_address = server_socket.accept()
        print("New connection from {}:{}".format(client_address[0], client_address[1]))

        # Add the client socket to the list
        client_sockets.append(client_socket)

        # Call the menu function for the new client
        show_menu(client_sockets)

    # Close the server socket
    server_socket.close()

# Run the server main function
if __name__ == '__main__':
    server_main()
