import socket  # Importing the socket module for network communication
import os  # Importing the os module for operating system-related tasks
import json  # Importing the json module for working with JSON data
import csv  # Importing the csv module for reading and writing CSV files
import time  # Importing the time module for time-related functions

# Function to send a file or data to the server
def send_data(file_path, server_socket):
    # Check if the input is a file path
    if os.path.isfile(file_path):
        # Send file to the server
        with open(file_path, 'rb') as file:
            file_data = file.read()
        # Get the file size
        file_size = os.path.getsize(file_path)
        # Send the file size to the server
        server_socket.send(str(file_size).encode())
        # Wait for the server to acknowledge the file size
        server_socket.recv(1024)
        # Start measuring the time
        start_time = time.time()

        # Send the file data to the server
        server_socket.sendall(file_data)

        # Wait for the server to acknowledge the file receipt
        server_socket.recv(1024)

        # Calculate the end-to-end latency
        end_time = time.time()
        latency = end_time - start_time

        print("File sent successfully.")
        print(f"End-to-end latency: {latency:.6f} seconds")
    else:
        # Send data to the server
        # Convert the data to JSON format
        json_data = json.dumps(file_path)

        # Convert the JSON data to bytes
        data_bytes = json_data.encode()

        # Get the data size
        data_size = len(data_bytes)

        # Send the data size to the server
        server_socket.send(str(data_size).encode())

        # Wait for the server to acknowledge the data size
        server_socket.recv(1024)

        # Start measuring the time
        start_time = time.time()

        # Send the data to the server
        server_socket.sendall(data_bytes)

        # Wait for the server to acknowledge the data receipt
        server_socket.recv(1024)

        # Calculate the end-to-end latency
        end_time = time.time()
        latency = end_time - start_time

        print("Data sent successfully.")
        print(f"End-to-end latency: {latency:.6f} seconds.")

# Function to receive a file from the server
def receive_file(file_path, server_socket):
    # Receive the file size from the server
    file_size = int(server_socket.recv(4).decode())

    # Acknowledge the file size receipt
    server_socket.send(b'OK')

    # Create a buffer to hold the file data
    file_data = b''

    # Keep receiving data until the entire file is received
    while len(file_data) < file_size:
        chunk = server_socket.recv(1024)
        file_data += chunk

    # Write the received data to a file
    with open(file_path, 'wb') as file:
        file.write(file_data)

    # Acknowledge the file receipt
    server_socket.send(b'OK')

# Function to visualize a file received from the server
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
            choice = input(
                "Enter '1' to display full data or '2' to display data from a specific year and month (YYYY-MM): ")

            if choice == '1':
                # Display the full CSV data
                for row in csv_reader:
                    print(row)
            elif choice == '2':
                year_month = input("Enter the year and month (YYYY-MM): ")
                # Display data from a specific year and month
                for row in csv_reader:
                    if row[0].startswith(year_month):
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

# Function to display the menu and handle user choices
def show_menu(client_socket=None):
    print("1. Receive a file from the server")
    print("2. Visualize an image, CSV, or JSON file")
    print("3. Send a file or data to the server")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        if client_socket is None:
            print("Error: No client socket provided.")
            return

        file_path = input("Enter the path to save the received file: ")
        receive_file(file_path, client_socket)

    elif choice == '2':
        file_path = input("Enter the path of the file to visualize: ")
        visualize_file(file_path)

    elif choice == '3':
        if client_socket is None:
            print("Error: No client socket provided.")
            return

        file_path = input("Enter the file path or data to send: ")
        send_data(file_path, client_socket)

    elif choice == '4':
        return

    else:
        print("Invalid choice. Please try again.")

    show_menu(client_socket)

# Main function for the client
def client_main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set the timeout for sending a file (in seconds)
    SEND_TIMEOUT = 10

    # Connect to the server
    server_address = ('127.0.0.1', 8006)
    client_socket.connect(server_address)
    print("Connected to the server.")

    # Call the menu function for the client and pass the client_socket
    show_menu(client_socket)

    # Close the client socket
    client_socket.close()

# Run the client main function
if __name__ == '__main__':
    client_main()
