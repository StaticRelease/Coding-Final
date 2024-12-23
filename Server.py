import socket

# Constants
HOST = "localhost"
PORT = 5000
BUFFSIZE = 1024
FORMAT = "utf-8"

# File paths
SAIYAN_SAGA_FILE = "DBZ.txt"
KSaiyan_SAGA_CHOICES = ["KrillinOption.txt", "KrillenOP3.txt", "KrillinOP4.txt"]

# Server setup
ADDRESS = (HOST, PORT)
server = socket.socket()
server.bind(ADDRESS)
server.listen(3)


# Function to send file content to the client
def send_file_content(client, filename):
    """Send file content to the connected client."""
    try:
        with open(filename, 'r') as file:
            content = file.read()
            client.send(content.encode(FORMAT))
    except FileNotFoundError:
        client.send(f"Error: {filename} not found.".encode(FORMAT))


# Function to handle client connection and interaction
def handle_client(client, address):
    """Handle communication with the connected client."""
    print(f"Connected to {address}")

    try:
        # Send welcome message
        client.send("Welcome to the server".encode())
        client.send("Choose your saga".encode(FORMAT))
        client.send(bytes("\nFor Saiyan saga put 1: ".encode()))

        # Read the Saiyan Saga content
        with open(SAIYAN_SAGA_FILE, 'r') as file:
            content_saiyan_saga = file.read()

        while True:
            # Wait for the client's response to choose a saga
            message = int(client.recv(BUFFSIZE).decode(FORMAT))  # Receive client choice

            if message == 1:  # If the choice is 1, send Saiyan saga content
                client.send(content_saiyan_saga.encode(FORMAT))
            else:
                # Invalid choice, break out of the loop
                break

            # Handle further choices for saga options
            next_choice = int(client.recv(BUFFSIZE).decode(FORMAT))
            while next_choice >= 2:
                if 2 <= next_choice <= len(KSaiyan_SAGA_CHOICES) + 1:
                    # Send the corresponding saga choice based on user input
                    send_file_content(client, KSaiyan_SAGA_CHOICES[next_choice - 2])
                    next_choice = int(client.recv(BUFFSIZE).decode())
                else:
                    break  # If an invalid choice is given, exit the loop

            # Close the client socket once the saga selection process is over
            client.close()
            break

    except Exception as e:
        print(f"Error: {e}")
        client.send(f"An error occurred: {e}".encode(FORMAT))
        client.close()


# Main server loop
def start_server():
    """Start the server and wait for client connections."""
    print("Server is waiting for a connection...")

    while True:
        # Accept a new client connection
        client, address = server.accept()
        handle_client(client, address)


if __name__ == "__main__":
    start_server()
