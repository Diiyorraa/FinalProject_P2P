# FinalProject_P2P
#Ruzimatova Diyorakhon 


                                                 P2P system using TCP protocol 
The proposed project aims to develop a peer-to-peer (P2P) system using Python 3 and the TCP protocol. The system will allow clients to send and visualize image, CSV, and JSON files on other client sides. It will also provide the capability to broadcast any file to multiple clients. The system will be implemented with a menu-based interface for selecting different choices. The project will be well-commented to ensure clarity and understanding of the code. Additionally, experimental results and analysis will be conducted using Wireshark to measure end-to-end latency for each scenario, and a timeout mechanism will be implemented for sending files


#SERVER#

1. `send_file(file_path, client_socket)`: This function sends a file to a specific client. It reads the file data in binary mode, gets the file size using `os.path.getsize()`, and sends the file size to the client. After receiving the acknowledgment from the client, it sends the file data using `client_socket.sendall()`. Finally, it waits for the client to acknowledge the file receipt.

2. `receive_file(file_path, client_socket)`: This function receives a file from a specific client. It first receives the file size from the client and acknowledges the receipt. Then, it creates a buffer to hold the file data and keeps receiving data until the entire file is received. It writes the received data to the specified file path and acknowledges the file receipt.

3. `broadcast_file(file_path, client_sockets)`: This function broadcasts a file to multiple clients. It iterates over each client socket in the `client_sockets` list and calls the `send_file()` function to send the file to each client.

4. `visualize_file(file_path)`: This function handles the visualization of different file types. It checks the file extension to determine the file type. For image files (extensions: `.jpg`, `.jpeg`, `.png`, `.gif`), it uses the PIL library to open and display the image. For CSV files (extension: `.csv`), it reads and displays the CSV data using the csv module. For JSON files (extension: `.json`), it loads the JSON data and prompts the user to choose between displaying the full data or filtering data by a specific date.

5. `show_menu(client_sockets)`: This function displays the menu options and handles user choices. It takes the list of connected client sockets as input. The user can choose to send a file to another client (calls `send_file()`), visualize an image/CSV/JSON file (calls `visualize_file()`), broadcast a file to multiple clients (calls `broadcast_file()`), or exit the program.

6. `server_main()`: This is the main function for the server. It creates a TCP socket, binds it to a specific address and port, and starts listening for incoming connections. When a new client connects, it adds the client socket to the `client_sockets` list and calls the menu function (`show_menu()`) for the new client. This allows each client to interact with the server independently. The server continues to accept incoming connections and handle client interactions until it is manually closed.

Overall, the modified code adds functionality to send files to specific clients, receive files from clients, and broadcast files to multiple clients. It also handles the visualization of different file types. The server can handle multiple clients simultaneously, allowing each client to perform operations independently.

#CLIENT# 

1. `send_data(file_path, server_socket)`: This function sends a file or data to the server. It first checks if the input is a file path using `os.path.isfile()`. If it is a file, the function reads the file data in binary mode, gets the file size using `os.path.getsize()`, and sends the file size to the server. After receiving the acknowledgment from the server, it sends the file data using `server_socket.sendall()`. If the input is not a file, it treats it as data. The data is converted to JSON format using `json.dumps()`, and then encoded to bytes. The size of the data is sent to the server, and after receiving acknowledgment, the data is sent using `server_socket.sendall()`. The function measures the end-to-end latency by calculating the time taken for the operation.

2. `receive_file(file_path, server_socket)`: This function receives a file from the server. It first receives the file size from the server and acknowledges the receipt. Then, it creates a buffer to hold the file data and keeps receiving data until the entire file is received. It writes the received data to the specified file path and acknowledges the receipt.

3. `visualize_file(file_path)`: This function handles the visualization of different file types. It checks the file extension to determine the file type. For image files (extensions: `.jpg`, `.jpeg`, `.png`, `.gif`), it uses the PIL library to open and display the image. For CSV files (extension: `.csv`), it reads and displays the CSV data using the csv module. For JSON files (extension: `.json`), it loads the JSON data and prompts the user to choose between displaying the full data or filtering data by a specific date.

4. `show_menu(client_socket=None)`: This function displays the menu options and handles user choices. It takes an optional client socket as input. The user can choose to receive a file from the server (calls `receive_file()`), visualize an image/CSV/JSON file (calls `visualize_file()`), send a file or data to the server (calls `send_data()`), or exit the program.

5. `client_main()`: This is the main function for the client. It creates a TCP socket, sets a timeout for sending a file, and connects to the server. It then calls the menu function (`show_menu()`) for the client, passing the client socket. This allows the client to interact with the server and perform operations based on user choices. After the menu function returns, the client socket is closed.

Overall, the modified code provides functionality for the client to send files or data to the server, receive files from the server, and visualize different file types. The client can interact with the server through a menu-based system. The code also includes latency measurement for file/data transfer operations.

Using a menu in both the server and client allows for a more interactive and user-friendly experience. Here's an explanation of why a menu is used in both the server and client:

Server Menu:
The server menu provides options for the server to perform various actions or operations. It allows the server administrator or operator to choose what actions the server should take. Some common options in a server menu could be starting or stopping certain services, configuring settings, managing connected clients, or performing specific tasks.
By presenting a menu, the server operator can easily select the desired action without needing to remember or type complex commands or parameters. It simplifies the interaction with the server and makes it more intuitive.

Client Menu:
The client menu serves as a user interface for the client to interact with the server. It provides options for the client to perform actions or request services from the server. The menu presents a set of choices that the client can select based on their requirements.
For example, in the given code, the client menu offers options to receive a file from the server, visualize an image/CSV/JSON file, or send a file or data to the server. These options allow the client to interact with the server for file transfer, data visualization, and other operations. The menu simplifies the client's interaction with the server and makes it easier to initiate specific tasks.

By utilizing a menu-based system, both the server and client can provide a more intuitive and user-friendly interface, reducing the complexity of manual command entry and allowing users to choose desired actions from a list of options.


